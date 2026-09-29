import sqlite3

# Connect to SQLite database (creates 'inventory.db' file in your folder)
conn = sqlite3.connect("inventory.db")
cursor = conn.cursor()

# Create Products Table
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS products (
        product_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price REAL NOT NULL,
        stock_quantity INTEGER NOT NULL
    )
"""
)

# Create Orders Table
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS orders (
        order_id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER,
        quantity_ordered INTEGER,
        total_price REAL,
        FOREIGN KEY(product_id) REFERENCES products(product_id)
    )
"""
)
conn.commit()

def view_products():
  cursor.execute("SELECT * FROM products")
  products = cursor.fetchall()

  print("\n--- Current Inventory ---")
  if not products:
    print("No products found in inventory.")
  else:
    for row in products:
      print(
          f"ID: {row[0]} | Name: {row[1]} | Price: ${row[2]} | Stock:"
          f" {row[3]}"
      )

def add_product():
  name = input("Enter product name: ")
  price = float(input("Enter product price: "))
  stock = int(input("Enter stock quantity: "))

  # Using parameterized queries to prevent SQL injection
  cursor.execute(
      "INSERT INTO products (name, price, stock_quantity) VALUES (?, ?, ?)",
      (name, price, stock),
  )
  conn.commit()
  print(f"Success! Product '{name}' added to the inventory.")

def update_stock():
  product_id = int(input("Enter Product ID to update: "))
  new_stock = int(input("Enter new stock quantity: "))

  cursor.execute(
      "UPDATE products SET stock_quantity = ? WHERE product_id = ?",
      (new_stock, product_id),
  )
  conn.commit()
  print("Stock updated successfully!")


def place_order():
  product_id = int(input("Enter Product ID to order: "))
  quantity = int(input("Enter quantity to order: "))

  # Check if product exists and get stock/price
  cursor.execute(
      "SELECT stock_quantity, price FROM products WHERE product_id = ?",
      (product_id,),
  )
  product = cursor.fetchone()

  if not product:
    print("Error: Product ID not found!")
    return

  current_stock, price = product

  if quantity > current_stock:
    print(f"Error: Insufficient stock! Only {current_stock} available.")
  else:
    new_stock = current_stock - quantity
    total_price = price * quantity

    # Update product stock
    cursor.execute(
        "UPDATE products SET stock_quantity = ? WHERE product_id = ?",
        (new_stock, product_id),
    )
    # Record the order
    cursor.execute(
        "INSERT INTO orders (product_id, quantity_ordered, total_price) VALUES"
        " (?, ?, ?)",
        (product_id, quantity, total_price),
    )
    conn.commit()
    print(f"Order placed successfully! Total Price: {total_price}")

def main_menu():
  while True:
    print("\n--- Inventory & Order Management System ---")
    print("1. View Products")
    print("2. Add New Product")
    print("3. Update Stock Quantity")
    print("4. Place an Order")
    print("5. Exit")

    choice = input("Enter your choice (1-5): ")

    if choice == "1":
      view_products()
    elif choice == "2":
      add_product()
    elif choice == "3":
      update_stock()
    elif choice == "4":
      place_order()
    elif choice == "5":
      print("Exiting... Goodbye!")
      conn.close()
      break
    else:
      print("Invalid choice. Please try again.")


if __name__ == "__main__":
  main_menu()

