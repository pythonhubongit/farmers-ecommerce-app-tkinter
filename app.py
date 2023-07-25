import tkinter as tk
from tkinter import messagebox
import mysql.connector
from tkinter import ttk

def get_database_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="udemymysql",
        database="myfarmers"
    )
    

def create_database():
    try:
        connection = get_database_connection()
        cursor = connection.cursor()

        # Create the new database
        sql = "CREATE DATABASE IF NOT EXISTS myfarmers"
        # cursor.execute("SHOW DATABASES")
        cursor.execute(sql)

        # for x in cursor:
        #     print(x)

        cursor.close()
        connection.close()

    except mysql.connector.Error as error:
        print(f"Error creating database: {error}")
        
def create_users_table():
    try:
        connection = get_database_connection()
        cursor = connection.cursor()

        sql = """
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255) NOT NULL,
            password VARCHAR(255) NOT NULL,
            user_type VARCHAR(80) NOT NULL
        )
        """
        cursor.execute(sql)

        cursor.close()
        connection.close()

    except mysql.connector.Error as error:
        print(f"Error creating 'users' table: {error}")

def create_products_table():
    try:
        connection = get_database_connection()
        cursor = connection.cursor()

        sql = """
        CREATE TABLE IF NOT EXISTS products (
            farmername VARCHAR(255) NOT NULL,
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            description VARCHAR(1000) NOT NULL,
            quantity DECIMAL(10, 2) NOT NULL,
            expiry_date DATE NOT NULL,
            price DECIMAL(10, 2) NOT NULL
        )
        """
        # sql = "DROP TABLE products"
        cursor.execute(sql)

        cursor.close()
        connection.close()

    except mysql.connector.Error as error:
        print(f"Error creating 'products' table: {error}")


# Function to handle login button click
def login():
    global username, password, user_type
    username = username_entry.get()
    password = password_entry.get()
    user_type = user_type_var.get()

    # Implement your MySQL database login verification here
    # Use the username, password, and user_type to check the database
    # and validate the login credentials.
    # For simplicity, let's assume the validation always passes for now.

    try:
        connection = get_database_connection()
        cursor = connection.cursor()

        # Fetch user data from the database based on the entered username and user_type
        sql = "SELECT password FROM users WHERE username = %s AND password = %s"
        values = (username, password)
        cursor.execute(sql, values)
        result = cursor.fetchone()
        print("None->", result)

        if result != None:
            if user_type == "Farmer":
                farmer_home_screen()
            elif user_type == "Normal User":
                normal_user_screen()
            elif user_type == "Company":
                company_screen()

        else:
            messagebox.showerror("Login Failed", "User not found. Please register first.")
            register_screen()

        cursor.close()
        connection.close()

    except mysql.connector.Error as error:
        messagebox.showerror("Login Error", f"Error during login: {error}")

# Function to handle registration button click
def register():
    username = username_entry.get()
    password = password_entry.get()
    user_type = user_type_var.get()
    
    if(len(username)<4 or len(password)<8):
        messagebox.showerror("Registration failed","username should be at least 4 characters long and password should be at least 8 characters long")
        register_screen()
        return

    # Implement your MySQL database registration logic here
    # Use the username, password, and user_type to insert the new user
    # into the database.
    # For simplicity, let's assume the registration always succeeds for now.
    # Connect to the MySQL database
    try:
        connection = get_database_connection()
        cursor = connection.cursor()

        # Insert the user data into the database
        sql = "INSERT INTO users (username, password, user_type) VALUES (%s, %s, %s)"
        values = (username, password, user_type)
        cursor.execute(sql, values)

        connection.commit()
        cursor.close()
        connection.close()

        messagebox.showinfo("Registration Successful", "Registration successful! Please log in.")
        login_screen()

    except mysql.connector.Error as error:
        messagebox.showerror("Registration Error", f"Error during registration: {error}")
        register_screen()

    login_screen()

# Function to create and display the login screen
def login_screen():
    clear_screen()
    label = tk.Label(root, text="Login Screen")
    label.pack()

    username_label = tk.Label(root, text="Username")
    username_label.pack()
    global username_entry
    username_entry = tk.Entry(root)
    username_entry.pack()

    password_label = tk.Label(root, text="Password")
    password_label.pack()
    global password_entry
    password_entry = tk.Entry(root, show="*")
    password_entry.pack()

    user_type_label = tk.Label(root, text="User Type")
    user_type_label.pack()
    global user_type_var
    user_type_var = tk.StringVar(root)
    user_type_var.set("Farmer")  # Default value
    user_type_options = ["Farmer", "Normal User", "Company"]
    user_type_dropdown = tk.OptionMenu(root, user_type_var, *user_type_options)
    user_type_dropdown.pack()

    login_button = tk.Button(root, text="Login", command=login)
    login_button.pack()

    register_button = tk.Button(root, text="Register", command=register_screen)
    register_button.pack()

# Function to create and display the registration screen
def register_screen():
    clear_screen()
    label = tk.Label(root, text="Registration Screen")
    label.pack()

    username_label = tk.Label(root, text="Username")
    username_label.pack()
    global username_entry
    username_entry = tk.Entry(root)
    username_entry.pack()

    password_label = tk.Label(root, text="Password")
    password_label.pack()
    global password_entry
    password_entry = tk.Entry(root, show="*")
    password_entry.pack()

    user_type_label = tk.Label(root, text="User Type")
    user_type_label.pack()
    global user_type_var
    user_type_var = tk.StringVar(root)
    user_type_var.set("Farmer")  # Default value
    user_type_options = ["Farmer", "Normal User", "Company"]
    user_type_dropdown = tk.OptionMenu(root, user_type_var, *user_type_options)
    user_type_dropdown.pack()

    register_button = tk.Button(root, text="Register", command=register)
    register_button.pack()

def save_product():
    title = title_entry.get()
    description = description_entry.get()
    quantity = quantity_entry.get()
    expiry_date = expiry_entry.get()
    price = price_entry.get()
    # farmer_name = username_entry.get()

    try:
        connection = get_database_connection()
        cursor = connection.cursor()

        # Insert the product data into the database
        sql = "INSERT INTO products (farmername, title, description, quantity, expiry_date, price ) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (username, title, description, quantity, expiry_date, price)
        cursor.execute(sql, values)

        connection.commit()
        cursor.close()
        connection.close()

        messagebox.showinfo("Product Added", "Product has been added successfully!")
        farmer_home_screen()

    except mysql.connector.Error as error:
        messagebox.showerror("Product Add Error", f"Error adding the product: {error}")


def farmer_add_product_screen():
    # print(username, password, user_type)
    clear_screen()
    label = tk.Label(root, text="Add Product")
    label.pack()

    title_label = tk.Label(root, text="Title")
    title_label.pack()
    global title_entry
    title_entry = tk.Entry(root)
    title_entry.pack()

    description_label = tk.Label(root, text="Description")
    description_label.pack()
    global description_entry
    description_entry = tk.Entry(root)
    description_entry.pack()

    quantity_label = tk.Label(root, text="Quantity (kg)")
    quantity_label.pack()
    global quantity_entry
    quantity_entry = tk.Entry(root)
    quantity_entry.pack()

    expiry_label = tk.Label(root, text="Expiry Date (YYYY-MM-DD)")
    expiry_label.pack()
    global expiry_entry
    expiry_entry = tk.Entry(root)
    expiry_entry.pack()

    price_label = tk.Label(root, text="Price")
    price_label.pack()
    global price_entry
    price_entry = tk.Entry(root)
    price_entry.pack()

    add_product_button = tk.Button(root, text="Add Product", command=save_product)
    add_product_button.pack()
    add_product_button = tk.Button(root, text="Logout", command=login_screen)
    add_product_button.pack()


# Function to create and display the farmer's home screen
def farmer_home_screen():
    clear_screen()
    label = tk.Label(root, text="Welcome to Farmer's Page")
    label.pack()
    add_product_button = tk.Button(root, text="Add Product", command=farmer_add_product_screen)
    add_product_button.pack()
    
    add_product_button = tk.Button(root, text="Logout", command=login_screen)
    add_product_button.pack()

# Function to create and display the normal user screen
def normal_user_screen():
    clear_screen()
    root.geometry('1100x400')
    label = tk.Label(root, text="Normal User Screen - Products List")
    label.pack()

    try:
        connection = get_database_connection()
        cursor = connection.cursor()

        # Fetch all products from the database
        sql = "SELECT farmername, title, description, quantity, expiry_date, price FROM products"
        cursor.execute(sql)
        products = cursor.fetchall()

        # Create a Treeview widget to display products in a table-like format
        tree = ttk.Treeview(root, columns=("FarmerName", "Title", "Description", "Quantity", "Expiry Date", "Price"), show="headings")

        # Add headings to the columns
        tree.heading("FarmerName", text="FarmerName")
        tree.heading("Title", text="Title")
        tree.heading("Description", text="Description")
        tree.heading("Quantity", text="Quantity")
        tree.heading("Expiry Date", text="Expiry Date")
        tree.heading("Price", text="Price")
        
        # setting width
        tree.column("FarmerName", width=80)
        tree.column("Title", width=100)
        tree.column("Description", width=200)
        tree.column("Quantity", width=80)
        tree.column("Expiry Date", width=80)
        tree.column("Price", width=80)

        # Add products data to the treeview
        for product in products:
            tree.insert("", "end", values=product)

        tree.pack()

        cursor.close()
        connection.close()

    except mysql.connector.Error as error:
        messagebox.showerror("Error", f"Error fetching products: {error}")
    add_product_button = tk.Button(root, text="Logout", command=login_screen)
    add_product_button.pack()

# Function to create and display the company screen
def company_screen():
    clear_screen()
    root.geometry('1100x400')
    label = tk.Label(root, text="Company Screen - Products List")
    label.pack()

    try:
        connection = get_database_connection()
        cursor = connection.cursor()

        # Fetch all products from the database
        sql = "SELECT farmername, title, description, quantity, expiry_date, price FROM products"
        cursor.execute(sql)
        products = cursor.fetchall()

        # Create a Treeview widget to display products in a table-like format
        tree = ttk.Treeview(root, columns=("Farmername", "Title", "Description", "Quantity", "Expiry Date", "Price"), show="headings")

        # Add headings to the columns
        tree.heading("Farmername", text="Farmername")
        tree.heading("Title", text="Title")
        tree.heading("Description", text="Description")
        tree.heading("Quantity", text="Quantity")
        tree.heading("Expiry Date", text="Expiry Date")
        tree.heading("Price", text="Price")
        
        # setting width
        tree.column("FarmerName", width=80)
        tree.column("Title", width=120)
        tree.column("Description", width=200)
        tree.column("Quantity", width=80)
        tree.column("Expiry Date", width=80)
        tree.column("Price", width=80)

        # Add products data to the treeview
        for product in products:
            tree.insert("", "end", values=product)

        tree.pack()

        cursor.close()
        connection.close()

    except mysql.connector.Error as error:
        messagebox.showerror("Error", f"Error fetching products: {error}")
    add_product_button = tk.Button(root, text="Logout", command=login_screen)
    add_product_button.pack()


# Function to clear the screen
def clear_screen():
    for widget in root.winfo_children():
        widget.destroy()

# Main program
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Farmer Ecommerce App")
    root.geometry("400x300")
    create_database()
    create_users_table()
    create_products_table()
    login_screen()
    root.mainloop()
