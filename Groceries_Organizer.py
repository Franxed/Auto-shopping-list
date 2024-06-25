import sqlite3


def initialize_database():
    # Connect to the SQLite database.
    db = sqlite3.connect('Groceries_Database.db')
    cursor = db.cursor()
    try:
        # Create the Foodstock table if it doesn't exist.
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Foodstock(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Item TEXT NOT NULL UNIQUE,
            Quantity INTEGER NOT NULL,
            Minimum_Quantity INTEGER NOT NULL
        )
        ''')
        # Create the Shopping_list table if it doesn't exist.
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Shopping_list(
            id INTEGER PRIMARY KEY,
            Amount_Needed INTEGER NOT NULL,
            FOREIGN KEY(id) REFERENCES Foodstock(id)
        )
        ''')
        # Commit the changes.
        db.commit()
    finally:
        # Close the database connection.
        db.close()


def update_foodstock(item, quantity, minimum_quantity):
    # Connect to the SQLite database.
    db = sqlite3.connect("Groceries_Database.db")
    cursor = db.cursor()
    try:
        # Insert or update the Foodstock table.
        cursor.execute('''
            INSERT INTO Foodstock (Item, Quantity, Minimum_Quantity)
            VALUES (?, ?, ?)
            ON CONFLICT(Item) DO UPDATE SET Quantity = ?, Minimum_Quantity = ?
            ''', (item, quantity, minimum_quantity, quantity, minimum_quantity))
        db.commit()
        # Get the id of the item.
        cursor.execute('SELECT id FROM Foodstock WHERE Item = ?', (item,))
        item_id = cursor.fetchone()[0]
        # Update the Shopping_list based on the item's quantity.
        update_shopping_list(item_id)
        print(f"Added or updated '{item}' successfully!")
    finally:
        # Close the database connection.
        db.close()


def remove_foodstock(item):
    # Connect to the SQLite database.
    db = sqlite3.connect("Groceries_Database.db")
    cursor = db.cursor()
    try:
        # Remove the item from the Foodstock table.
        cursor.execute('DELETE FROM Foodstock WHERE Item = ?', (item,))
        db.commit()
        print(f"Removed '{item}' successfully!")
    finally:
        # Close the database connection.
        db.close()


def update_shopping_list(item_id):
    # Connect to the SQLite database.
    db = sqlite3.connect("Groceries_Database.db")
    cursor = db.cursor()
    try:
        # Check the current quantity and minimum quantity of the item.
        cursor.execute('''SELECT Quantity, Minimum_Quantity FROM Foodstock WHERE id = ?''', (item_id,))
        row = cursor.fetchone()
        if row:
            if row[0] < row[1]:
                # If the quantity is less than the minimum, update the Shopping_list.
                amount_needed = row[1] - row[0]
                cursor.execute('''
                INSERT INTO Shopping_list (id, Amount_Needed)
                VALUES (?, ?)
                ON CONFLICT(id) DO UPDATE SET Amount_Needed = excluded.Amount_Needed
                ''', (item_id, amount_needed))
            else:
                # If the quantity meets or exceeds the minimum, remove it from the Shopping_list.
                cursor.execute('DELETE FROM Shopping_list WHERE id = ?', (item_id,))
        db.commit()
    finally:
        # Close the database connection.
        db.close()


def view_shopping_list():
    # Connect to the SQLite database.
    db = sqlite3.connect("Groceries_Database.db")
    cursor = db.cursor()
    try:
        # Retrieve items from the Shopping_list.
        cursor.execute('''
        SELECT Foodstock.Item, Shopping_list.Amount_Needed FROM Shopping_list
        JOIN Foodstock ON Shopping_list.id = Foodstock.id''')
        items = cursor.fetchall()
    finally:
        # Close the database connection.
        db.close()
        return items


def view_foodstock():
    # Connect to the SQLite database.
    db = sqlite3.connect("Groceries_Database.db")
    cursor = db.cursor()
    try:
        # Retrieve items from the Foodstock.
        cursor.execute('SELECT Item, Quantity, Minimum_Quantity FROM Foodstock')
        items = cursor.fetchall()
    finally:
        # Close the database connection.
        db.close()
        return items


def main():
    while True:
        # Print the menu.
        print("\nMenu:")
        print("1. Update an item in Foodstock")
        print("2. Remove an item from Foodstock")
        print("3. View Shopping List")
        print("4. View Foodstock")
        print("5. Exit")

        # Get the user's choice.
        choice = input("Select a number: ")
        try:
            if choice == '1':
                # Update an item in Foodstock.
                item = input("Enter item name: ").title()
                quantity = int(input("Enter new quantity: "))
                minimum_quantity = int(input("Enter new minimum quantity: "))
                update_foodstock(item, quantity, minimum_quantity)
            elif choice == '2':
                # Remove an item from Foodstock.
                item = input("Enter item name to remove: ").title()
                remove_foodstock(item)
            elif choice == '3':
                # View the Shopping List.
                items = view_shopping_list()
                print("\nShopping List:\n")
                for item, amount_needed in items:
                    print(f"Item: {item}\nAmount Needed: {amount_needed}\n")
            elif choice == '4':
                # View the Foodstock.
                items = view_foodstock()
                print("\nFoodstock:\n")
                for item, quantity, min_qty in items:
                    print(f"Item: {item}\nQuantity: {quantity}\nMinimum Required: {min_qty}\n")
            elif choice == '5':
                # Exit the program.
                print("Exiting the program.")
                break
            else:
                print("Invalid option, please try again.")
        except Exception as e:
            print(f"An error occurred: {e}")


if __name__ == "__main__":
    # Initialize the database.
    initialize_database()
    # Start the main program loop.
    main()
