"""
Library Management System API
A CRUD REST API using FastAPI and MySQL.
"""

from datetime import date
from typing import List, Optional

import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date, Boolean, func
from sqlalchemy.orm import sessionmaker, declarative_base, relationship, Session

# DATABASE SETUP
DATABASE_URL = "mysql+pymysql://root:password@localhost/library_db"

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

# MODELS 
class BookModel(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255))
    author = Column(String(255))
    isbn = Column(String(13), unique=True)
    publication_year = Column(Integer)
    genre = Column(String(100))
    available = Column(Boolean, default=True)
    loans = relationship("LoanModel", back_populates="book")


class PatronModel(Base):
    __tablename__ = "patrons"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    email = Column(String(255), unique=True)
    phone = Column(String(20))
    address = Column(String(255))
    registered_date = Column(Date, default=func.current_date())
    loans = relationship("LoanModel", back_populates="patron")


class LoanModel(Base):
    __tablename__ = "loans"
    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"))
    patron_id = Column(Integer, ForeignKey("patrons.id"))
    loan_date = Column(Date, default=func.current_date())
    due_date = Column(Date)
    return_date = Column(Date, nullable=True)
    book = relationship("BookModel", back_populates="loans")
    patron = relationship("PatronModel", back_populates="loans")


# === SCHEMAS ===
class BookBase(BaseModel):
    title: str
    author: str
    isbn: str
    publication_year: int
    genre: str

class BookCreate(BookBase):
    pass

class Book(BookBase):
    id: int
    available: bool
    class Config:
        orm_mode = True

class PatronBase(BaseModel):
    name: str
    email: EmailStr
    phone: str
    address: str

class PatronCreate(PatronBase):
    pass

class Patron(PatronBase):
    id: int
    registered_date: date
    class Config:
        orm_mode = True

class LoanBase(BaseModel):
    book_id: int
    patron_id: int
    due_date: date

class LoanCreate(LoanBase):
    pass

class LoanUpdate(BaseModel):
    return_date: date

class Loan(LoanBase):
    id: int
    loan_date: date
    return_date: Optional[date] = None
    class Config:
        orm_mode = True

class LoanWithDetails(Loan):
    book: Book
    patron: Patron

# === DATABASE DEPENDENCY ===
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# === INIT ===
app = FastAPI(
    title="Library Management API",
    version="1.0.0"
)

Base.metadata.create_all(bind=engine)

# === ROUTES ===

@app.get("/", tags=["Welcome"])
def root():
    return {"message": "📚 Welcome to the Library Management API!"}


# --- BOOK ROUTES ---
@app.post("/books/", response_model=Book)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    db_book = BookModel(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

@app.get("/books/", response_model=List[Book])
def read_books(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(BookModel).offset(skip).limit(limit).all()

@app.get("/books/{book_id}", response_model=Book)
def read_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(BookModel).get(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@app.put("/books/{book_id}", response_model=Book)
def update_book(book_id: int, book: BookCreate, db: Session = Depends(get_db)):
    db_book = db.query(BookModel).get(book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    for key, value in book.dict().items():
        setattr(db_book, key, value)
    db.commit()
    db.refresh(db_book)
    return db_book

@app.delete("/books/{book_id}", status_code=204)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    db_book = db.query(BookModel).get(book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(db_book)
    db.commit()
    return


# --- PATRON ROUTES ---
@app.post("/patrons/", response_model=Patron)
def create_patron(patron: PatronCreate, db: Session = Depends(get_db)):
    db_patron = PatronModel(**patron.dict())
    db.add(db_patron)
    db.commit()
    db.refresh(db_patron)
    return db_patron

@app.get("/patrons/", response_model=List[Patron])
def read_patrons(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(PatronModel).offset(skip).limit(limit).all()

@app.get("/patrons/{patron_id}", response_model=Patron)
def read_patron(patron_id: int, db: Session = Depends(get_db)):
    patron = db.query(PatronModel).get(patron_id)
    if not patron:
        raise HTTPException(status_code=404, detail="Patron not found")
    return patron

@app.put("/patrons/{patron_id}", response_model=Patron)
def update_patron(patron_id: int, patron: PatronCreate, db: Session = Depends(get_db)):
    db_patron = db.query(PatronModel).get(patron_id)
    if not db_patron:
        raise HTTPException(status_code=404, detail="Patron not found")
    for key, value in patron.dict().items():
        setattr(db_patron, key, value)
    db.commit()
    db.refresh(db_patron)
    return db_patron

@app.delete("/patrons/{patron_id}", status_code=204)
def delete_patron(patron_id: int, db: Session = Depends(get_db)):
    db_patron = db.query(PatronModel).get(patron_id)
    if not db_patron:
        raise HTTPException(status_code=404, detail="Patron not found")
    db.delete(db_patron)
    db.commit()
    return


# --- LOAN ROUTES ---
@app.post("/loans/", response_model=Loan)
def create_loan(loan: LoanCreate, db: Session = Depends(get_db)):
    book = db.query(BookModel).get(loan.book_id)
    if not book or not book.available:
        raise HTTPException(status_code=400, detail="Book not available")
    book.available = False
    db_loan = LoanModel(**loan.dict())
    db.add(db_loan)
    db.commit()
    db.refresh(db_loan)
    return db_loan

@app.get("/loans/", response_model=List[Loan])
def read_loans(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(LoanModel).offset(skip).limit(limit).all()

@app.get("/loans/{loan_id}", response_model=LoanWithDetails)
def get_loan_details(loan_id: int, db: Session = Depends(get_db)):
    loan = db.query(LoanModel).get(loan_id)
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    return loan

@app.put("/loans/{loan_id}/return", response_model=Loan)
def return_book(loan_id: int, update: LoanUpdate, db: Session = Depends(get_db)):
    loan = db.query(LoanModel).get(loan_id)
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    loan.return_date = update.return_date
    book = db.query(BookModel).get(loan.book_id)
    book.available = True
    db.commit()
    db.refresh(loan)
    return loan
