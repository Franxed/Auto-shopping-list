import sqlite3

def initialize_database():
    # Connect to SQLite database
    db = sqlite3.connect('Groceries_Database.db')
    cursor = db.cursor()
    try:
        # Create Foodstock table with UNIQUE constraint on 'Item'
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Foodstock(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Item TEXT NOT NULL UNIQUE,
            Quantity INTEGER NOT NULL,
            Minimum_Quantity INTEGER NOT NULL
        )
        ''')

        # Create Shopping_list table linked by id to Foodstock table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Shopping_list(
            id INTEGER PRIMARY KEY,
            Amount_Needed INTEGER NOT NULL,
            FOREIGN KEY(id) REFERENCES Foodstock(id)
        )
        ''')
        db.commit()  # Commit the changes to the database
    finally:
        db.close()  # Close the database connection

def add_foodstock(item, quantity, minimum_quantity):
    db = sqlite3.connect("Groceries_Database.db")
    cursor = db.cursor()
    try:
        # Insert or update Foodstock entry with conflict resolution on 'Item'
        cursor.execute('''
            INSERT INTO Foodstock (Item, Quantity, Minimum_Quantity)
            VALUES (?, ?, ?)
            ON CONFLICT(Item) DO UPDATE SET Quantity = Quantity + excluded.Quantity,
            Minimum_Quantity = excluded.Minimum_Quantity
            ''', (item, quantity, minimum_quantity))
        db.commit()

        # Get the id of the updated/inserted item
        cursor.execute('SELECT id FROM Foodstock WHERE Item = ?', (item,))
        item_id = cursor.fetchone()[0]
        update_shopping_list(item_id)  # Update the shopping list based on this item
    finally:
        db.close()

def update_shopping_list(item_id):
    db = sqlite3.connect("Groceries_Database.db")
    cursor = db.cursor()
    try:
        # Retrieve the current stock and minimum required stock
        cursor.execute('''SELECT Quantity, Minimum_Quantity FROM Foodstock WHERE id = ?''', (item_id,))
        row = cursor.fetchone()
        if row and row[0] < row[1]:
            amount_needed = row[1] - row[0]
            # Update or insert into Shopping_list with conflict resolution on 'id'
            cursor.execute('''
            INSERT INTO Shopping_list (id, Amount_Needed)
            VALUES (?, ?)
            ON CONFLICT(id) DO UPDATE SET Amount_Needed = excluded.Amount_Needed
            ''', (item_id, amount_needed))
        db.commit()
    finally:
        db.close()

def view_shopping_list():
    db = sqlite3.connect("Groceries_Database.db")
    cursor = db.cursor()
    try:
        # Retrieve all items from the Shopping List linked to Foodstock
        cursor.execute('''
        SELECT Foodstock.Item, Shopping_list.Amount_Needed FROM Shopping_list
        JOIN Foodstock ON Shopping_list.id = Foodstock.id''')
        items = cursor.fetchall()
    finally:
        db.close()
        return items

def view_foodstock():
    db = sqlite3.connect("Groceries_Database.db")
    cursor = db.cursor()
    try:
        # Retrieve all items from Foodstock
        cursor.execute('SELECT Item, Quantity, Minimum_Quantity FROM Foodstock')
        items = cursor.fetchall()
    finally:
        db.close()
        return items

def main():
    while True:
        print("\nMenu:")
        print("1. Add an item to Foodstock")
        print("2. Update Shopping List")
        print("3. View Shopping List")
        print("4. View Foodstock")
        print("5. Exit")

        choice = input("Select a number: ")
        try:
            if choice == '1':
                item = input("Enter item name: ")
                quantity = int(input("Enter quantity: "))
                minimum_quantity = int(input("Enter minimum quantity: "))
                add_foodstock(item, quantity, minimum_quantity)
                print(f"Added '{item}' succesfully!")
            elif choice == '2':
                item_id = int(input("Enter item ID to update Shopping List: "))
                update_shopping_list(item_id)
            elif choice == '3':
                items = view_shopping_list()
                print("\nShopping List:")
                for item, amount_needed in items:
                    print(f"Item: {item}, Amount Needed: {amount_needed}")
            elif choice == '4':
                items = view_foodstock()
                print("\nFoodstock:\n")
                for item, quantity, min_qty in items:
                    print(f"Item: {item}\nQuantity: {quantity}\nMinimum Required: {min_qty}\n")
            elif choice == '5':
                print("Exiting the program.")
                break
            else:
                print("Invalid option, please try again.")
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    initialize_database()
    main()
