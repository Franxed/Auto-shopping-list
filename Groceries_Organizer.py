import sqlite3

def initialize_database():
    db = sqlite3.connect('Groceries_Database.db')
    cursor = db.cursor()

    # Create Foodstock table with a column for minimum quantity
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Foodstock(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Item TEXT NOT NULL,
        Quantity INTEGER NOT NULL,
        Minimum_Quantity INTEGER NOT NULL
    )
    ''')

    # Create Shopping_list table with a same id as Foodstock's table.
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Shopping_list(
        id INTEGER PRIMARY KEY,
        Amount_Needed INTEGER NOT NULL,
        FOREIGN KEY(id) REFERENCES Foodstock(id)
    )
    ''')
    db.commit()
    db.close()

def add_foodstock(item, quantity, minimum_quantity):
    db = sqlite3.connect("Groceries_Database.db")
    cursor = db.cursor()

    # Insert or update an item in Foodstock
    cursor.execute('''
        INSERT INTO Foodstock (Item, Quantity, Minimum_Quantity)
        VALUES (?, ?, ?)
        ON CONFLICT(Item) DO UPDATE SET Quantity = Quantity + excluded.Quantity,
        Minimum_Quantity = excluded.Minimum_Quantity
        ''', (item, quantity, minimum_quantity))
    db.commit()

    # Ensure that any update in Foodstock leads to checking the shopping list
    cursor.execute('SELECT id FROM Foodstock WHERE Item = ?', (item))
    item_id = cursor.fetchone()[0]
    db.close()
    update_shopping_list(item_id)

def update_shoppinglist(item_id):
    db = sqlite3.connect("Groceries_Database.db")
    cursor = db.cursor()

    cursor.execut('''SELECT Quantity, Minimum_Quantity FROM Foodstock WHERE id = ?''',
                  (item_id))
    row = cursor.fetchone()
    if row and row[0] < row[1]:
        amount_needed = row[1] - row[0]
        cursor.execute('''
        INSERT INTO Shopping_list(id, Amount_Needed)
        VALUES(?,?)
        ON CONFLICT(id) DO UPDATE SET Amount_Needed = excluded.Amount_Needed
        ''', (item_id, amount_needed))
    db.commit()
    db.close()''')
