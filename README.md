# SAMUEL EMMANUEL KIMARO 
# WEEK_8_DATABASE_PLP

# QUESTION ONE
## Build a Complete Database Management System
**Objective**

Design and implement a full-featured database using only MySQL.

**What to do**

1. Choose a real-world use case (e.g., Library Management, Student Records, Clinic Booking System, Inventory Tracking, etc.)
2. Create a well-structured relational database using SQL.

**Use SQL to create the following**

1. Tables with proper constraints (PK, FK, NOT NULL, UNIQUE)
2. Relationships (1-1, 1-M, M-M where needed)

**Deliverables**

A single .sql file containing your:

1. CREATE TABLE statements
2. Sample  data



# QUESTION TWO
## Create a Simple CRUD API Using MySQL + Programming

**Objective**
Combine your MySQL skills with a programming language (Python or JavaScript) to create a working CRUD API.

**What to do**

Choose any use case (e.g., Task Manager, Contact Book, Student Portal)

Design your database schema in MySQL (at least 2–3 tables)

**Build an API using**

1. Node.js + Express (if using JavaScript)
2. FastAPI (if using Python)
3. Implement all CRUD operations (Create, Read, Update, Delete)
4. Connect your API to the MySQL database

# QUESTION TWO RESPONSE
## Library Management System API

A RESTful API for managing library operations including books, patrons, and loans.

## Features

- Complete CRUD operations for books, patrons, and loans
- Validation for creating and updating resources
- Business logic implementation (e.g., book availability tracking)
- MySQL database integration
- FastAPI with automatic OpenAPI documentation

## Database Schema

The system uses three main tables:

1. **Books**
   - id (Primary Key)
   - title
   - author
   - isbn (Unique)
   - publication_year
   - genre
   - available (Boolean)

2. **Patrons**
   - id (Primary Key)
   - name
   - email (Unique)
   - phone
   - address
   - registered_date

3. **Loans**
   - id (Primary Key)
   - book_id (Foreign Key)
   - patron_id (Foreign Key)
   - loan_date
   - due_date
   - return_date (Nullable)

## Project Structure

```
library-management-api/
├── app/
│   ├── __init__.py
│   ├── main.py           # FastAPI application entry point
│   ├── database.py       # Database connection setup
│   ├── models.py         # SQLAlchemy models
│   ├── schemas.py        # Pydantic schemas
│   └── routers/
│       ├── __init__.py
│       ├── books.py      # Book endpoints
│       ├── patrons.py    # Patron endpoints
│       └── loans.py      # Loan endpoints
├── init_database.sql     # SQL initialization script
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation
```

## Setup Instructions

### Prerequisites

- Python 3.7+
- MySQL 5.7+

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/GDIAMEL/WEEK_8_DATABASE.git
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up the MySQL database:
   - Create a MySQL database named `library_db`
   - Run the SQL initialization script:
     ```
     mysql -u root -p < init_database.sql
     ```
   - Update the database connection string in `app/database.py` with your credentials:
     ```python
     DATABASE_URL = "mysql+pymysql://username:password@localhost/library_db"
     ```

5. Start the application:
   ```
   uvicorn app.main:app --reload
   ```

6. Access the API documentation:
   - Open your browser and navigate to http://127.0.0.1:8000/docs

## API Endpoints

### Books

- `POST /books/` - Create a new book
- `GET /books/` - Get all books
- `GET /books/{book_id}` - Get a specific book
- `PUT /books/{book_id}` - Update a book
- `DELETE /books/{book_id}` - Delete a book

### Patrons

- `POST /patrons/` - Register a new patron
- `GET /patrons/` - Get all patrons
- `GET /patrons/{patron_id}` - Get a specific patron
- `PUT /patrons/{patron_id}` - Update a patron
- `DELETE /patrons/{patron_id}` - Delete a patron

### Loans

- `POST /loans/` - Create a new loan
- `GET /loans/` - Get all loans
- `GET /loans/{loan_id}` - Get a specific loan
- `PUT /loans/{loan_id}/return` - Return a book
- `DELETE /loans/{loan_id}` - Delete a loan record

## Testing API Endpoints

You can test the API using the FastAPI Swagger UI or with tools like curl or Postman:

### Example: Creating a new book

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/books/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "title": "The Lord of the Rings",
  "author": "J.R.R. Tolkien",
  "isbn": "9780544003415",
  "publication_year": 1954,
  "genre": "Fantasy",
  "available": true
}'
```

### Example: Creating a new loan

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/loans/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "book_id": 1,
  "patron_id": 1,
  "due_date": "2023-06-30"
}'
```
