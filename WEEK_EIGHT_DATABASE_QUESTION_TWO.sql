-- Create database
CREATE DATABASE IF NOT EXISTS library_db;
USE library_db;

-- Create tables based on our models
CREATE TABLE IF NOT EXISTS books (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(255) NOT NULL,
    isbn VARCHAR(13) NOT NULL UNIQUE,
    publication_year INT NOT NULL,
    genre VARCHAR(100) NOT NULL,
    available BOOLEAN DEFAULT TRUE,
    INDEX idx_title (title),
    INDEX idx_author (author),
    INDEX idx_isbn (isbn)
);

CREATE TABLE IF NOT EXISTS patrons (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    phone VARCHAR(20) NOT NULL,
    address VARCHAR(255) NOT NULL,
    registered_date DATE DEFAULT (CURRENT_DATE),
    INDEX idx_email (email)
);

CREATE TABLE IF NOT EXISTS loans (
    id INT AUTO_INCREMENT PRIMARY KEY,
    book_id INT NOT NULL,
    patron_id INT NOT NULL,
    loan_date DATE DEFAULT (CURRENT_DATE),
    due_date DATE NOT NULL,
    return_date DATE NULL,
    FOREIGN KEY (book_id) REFERENCES books(id),
    FOREIGN KEY (patron_id) REFERENCES patrons(id)
);

-- Add sample data
INSERT INTO books (title, author, isbn, publication_year, genre, available)
VALUES 
('The Great Gatsby', 'F. Scott Fitzgerald', '9780743273565', 1925, 'Classic', TRUE),
('To Kill a Mockingbird', 'Harper Lee', '9780061120084', 1960, 'Fiction', TRUE),
('1984', 'George Orwell', '9780451524935', 1949, 'Dystopian', TRUE),
('Pride and Prejudice', 'Jane Austen', '9780141439518', 1813, 'Romance', TRUE),
('The Hobbit', 'J.R.R. Tolkien', '9780547928227', 1937, 'Fantasy', TRUE);

INSERT INTO patrons (name, email, phone, address, registered_date)
VALUES
('John Smith', 'john.smith@example.com', '555-123-4567', '123 Main St, Anytown', '2023-01-15'),
('Jane Doe', 'jane.doe@example.com', '555-987-6543', '456 Oak Ave, Somecity', '2023-02-20'),
('Bob Johnson', 'bob.johnson@example.com', '555-456-7890', '789 Pine Rd, Otherplace', '2023-03-10');
