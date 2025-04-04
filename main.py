import sqlite3

conn = sqlite3.connect('library.db')
cursor = conn.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS books "
    "(book_id INTEGER,"
    "title TEXT,"
    "author TEXT,"
    "year INTEGER,"
    "available INTEGER)")

cursor.execute("CREATE TABLE IF NOT EXISTS readers " 
    "(reader_id,"
    "name TEXT,"
    "phone TEXT,"
    "book_id INTEGER,"
    "FOREIGN KEY (book_id) REFERENCES books (book_id))")

conn.commit()

def add_book(title, author, year):
    cursor.execute('''
    INSERT INTO books (title, author, year) VALUES (?, ?, ?)
    ''', (title, author, year))
    conn.commit()

def add_reader(name, phone):
    cursor.execute('''
    INSERT INTO readers (name, phone) VALUES (?, ?)
    ''', (name, phone))
    conn.commit()

def get_available_books():
    cursor.execute('''
    SELECT * FROM books WHERE available = 1
    ''')
    return cursor.fetchall()

def get_reader_books(reader_id):
    cursor.execute('''
    SELECT b.* FROM books b
    JOIN readers r ON b.book_id = r.book_id
    WHERE r.reader_id = ?
    ''', (reader_id,))
    return cursor.fetchall()
    
def give_book(reader_id, book_id):
    cursor.execute('''
    UPDATE books SET available = 0 WHERE book_id = ?
    ''', (book_id,))
    cursor.execute('''
    UPDATE readers SET book_id = ? WHERE reader_id = ?
    ''', (book_id, reader_id))
    
def close_connection():
    conn.close()
