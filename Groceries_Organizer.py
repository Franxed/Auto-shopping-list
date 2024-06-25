import sqlite3


# Defined function to create database calld 'Groceries_Database.db'.
def initialize_database():
    db = sqlite3.connect('Groceries_Database.db')
    cursor = db.cursor()

# Create Foodstock table.
    cursor.execute('''CREATE TABLE IF NOT EXISTS Foodstock(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        Item TEXT NOT NULL,
                        Quantity INTEGER,
                        Minimum Quantity INTEGER NOT NULL)''')
    db.commit()

# Create Shopping_list.
    cursor.execute('''CREATE TABLE IF NOT EXISTS Shopping_list(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        Item TEXT NOT NULL,
                        Amount Needed INTEGER NOT NULL)''')
    db.commit()

# Create database with tables.
initialize_database()