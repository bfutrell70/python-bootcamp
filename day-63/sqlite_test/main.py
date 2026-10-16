import os
import sqlite3

 # Finds the directory where your script is saved
script_dir = os.path.dirname(os.path.abspath(__file__))

# Joins the script directory with your target file name
file_path = os.path.join(script_dir, "books-collection.db")
db = sqlite3.connect(file_path)

cursor = db.cursor()

# create a table in the database
# will throw sqlite3.OperationalError if the table 'books' already exists
# cursor.execute("CREATE TABLE books (id INTEGER PRIMARY KEY, title varchar(250) NOT NULL UNIQUE, author varchar(250) NOT NULL, rating FLOAT NOT NULL)")

# add data to the table
cursor.execute("INSERT INTO books VALUES(1, 'Harry Potter', 'J. K. Rowling', '9.3')")

# commit changes to the database
db.commit()