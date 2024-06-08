import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import mysql.connector

db_config = {
    'host': 'localhost',
    'user': 'your_username',
    'password': 'your_password',
    'database': 'your_database_name'
}

class Database:
    def __init__(self):
        try:
            self.conn = mysql.connector.connect(**db_config)
            self.cursor = self.conn.cursor()
        except mysql.connector.Error as err:
            print(f"Error connecting to MySQL database: {err}")

    def close_connection(self):
        if self.conn:
            self.cursor.close()
            self.conn.close()

class ProductManager(Database):
    def __init__(self):
        super().__init__()
        self.root = tk.Tk()
        self.root.title("Product Manager")

        self.reg_frame = tk.Frame(self.root)
        self.reg_frame.pack()

        self.name_label = tk.Label(self.reg_frame, text="Product Name:")
        self.name_label.grid(row=0, column=0, padx=5, pady=5)
        self.name_entry = tk.Entry(self.reg_frame)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        self.price_label = tk.Label(self.reg_frame, text="Price:")
        self.price_label.grid(row=1, column=0, padx=5, pady=5)
        self.price_entry = tk.Entry(self.reg_frame)
        self.price_entry.grid(row=1, column=1, padx=5, pady=5)

        self.quantity_label = tk.Label(self.reg_frame, text="Quantity:")
        self.quantity_label.grid(row=2, column=0, padx=5, pady=5)
        self.quantity_entry = tk.Entry(self.reg_frame)
        self.quantity_entry.grid(row=2, column=1, padx=5, pady=5)
       
        self.reg_button = tk.Button(self.reg_frame, text="Register", command=self.register_product)
        self.reg_button.grid(row=3, column=0, columnspan=2, pady=10)

        self.view_frame = tk.Frame(self.root)
        self.view_frame.pack()

        self.product_tree = ttk.Treeview(self.view_frame, columns=("Name", "Price", "Quantity"), show="headings")
        self.product_tree.heading("Name", text="Product Name")
        self.product_tree.heading("Price", text="Price")
        self.product_tree.heading("Quantity", text="Quantity")
        self.product_tree.pack()

        self.view_button = tk.Button(self.view_frame, text="View All Products", command=self.view_products)
        self.view_button.pack(pady=10)

        self.update_button = tk.Button(self.view_frame, text="Update Stock", command=self.update_stock)
        self.update_button.pack(pady=10)

        self.logout_button = tk.Button(self.view_frame, text="Logout", command=self.logout)
        self.logout_button.pack(pady=10)

        self.root.mainloop()

    def register_product(self):
        name = self.name_entry.get()
        price = self.price_entry.get()
        quantity = self.quantity_entry.get()

        if not name or not price or not quantity:
            messagebox.showerror("Error", "Please fill all fields.")
            return

        try:
            price = float(price)
            quantity = int(quantity)
        except ValueError:
            messagebox.showerror("Error", "Price and quantity must be numbers.")
            return

        self.cursor.execute("INSERT INTO products (name, price, quantity) VALUES (%s, %s, %s)", (name, price, quantity))
        self.conn.commit()
        messagebox.showinfo("Success", "Product registered successfully")
                            
        self.name_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)
        self.quantity_entry.delete(0, tk.END)

    def view_products(self):
        
        self.cursor.execute("SELECT * FROM products")
        products = self.cursor.fetchall()

        for i in self.product_tree.get_children():
            self.product_tree.delete(i)

        for product in products:
            self.product_tree.insert("", tk.END, values=(product[1], product[2], product[3]))

    def update_stock(self):
        selected_product = self.product_tree.selection()
        if not selected_product:
            messagebox.showerror("Error", "Please select a product to update.")
            return

        product_id = selected_product[0]
        self.cursor.execute("SELECT * FROM products WHERE id = %s", (product_id,))
        product = self.cursor.fetchone()

        
        update_dialog = tk.Toplevel(self.root)
        update_dialog.title("Update Stock")


        quantity_label = tk.Label(update_dialog, text="New Quantity:")
        quantity_label.grid(row=0, column=0, padx=5, pady=5)
        quantity_entry = tk.Entry(update_dialog)
        quantity_entry.grid(row=0, column=1, padx=5, pady=5)

        
        update_button = tk.Button(update_dialog, text="Update", command=lambda: self.update_product_stock(product_id, quantity_entry.get(), update_dialog))
        update_button.grid(row=1, column=0, columnspan=2, pady=10)

    def update_product_stock(self, product_id, new_quantity, update_dialog):
        try:
            new_quantity = int(new_quantity)
        except ValueError:
            messagebox.showerror("Error", "Quantity must be an integer.")
            return

        self.cursor.execute("UPDATE products SET quantity = %s WHERE id = %s", (new_quantity, product_id))
        self.conn.commit()
        messagebox.showinfo("Success", "Product stock updated successfully!")
        update_dialog.destroy()

       
        self.view_products()

    def logout(self):
        self.root.destroy()

class Customer(Database):
    def __init__(self):
        super().__init__()
        self.root = tk.Tk()
        self.root.title("Customer")

        
        self.login_frame = tk.Frame(self.root)
        self.login_frame.pack()

        
        self.username_label = tk.Label(self.login_frame, text="Username:")
        self.username_label.grid(row=0, column=0, padx=5, pady=5)
        self.username_entry = tk.Entry(self.login_frame)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)

        self.password_label = tk.Label(self.login_frame, text="Password:")
        self.password_label.grid(row=1, column=0, padx=5, pady=5)
        self.password_entry = tk.Entry(self.login_frame, show="*")
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)

        
        self.login_button = tk.Button(self.login_frame, text="Login", command=self.login)
        self.login_button.grid(row=2, column=0, columnspan=2, pady=10)

        
        self.reg_frame = tk.Frame(self.root)
        self.reg_frame.pack()

      
        self.name_label = tk.Label(self.reg_frame, text="Name:")
        self.name_label.grid(row=0, column=0, padx=5, pady=5)
        self.name_entry = tk.Entry(self.reg_frame)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        self.username_label = tk.Label(self.reg_frame, text="Username:")
        self.username_label.grid(row=1, column=0, padx=5, pady=5)
        self.username_entry = tk.Entry(self.reg_frame)
        self.username_entry.grid(row=1, column=1, padx=5, pady=5)

        self.password_label = tk.Label(self.reg_frame, text="Password:")
        self.password_label.grid(row=2, column=0, padx=5, pady=5)
        self.password_entry = tk.Entry(self.reg_frame, show="*")
        self.password_entry.grid(row=2, column=1, padx=5, pady=5)

        
        self.reg_button = tk.Button(self.reg_frame, text="Register", command=self.register_customer)
        self.reg_button.grid(row=3, column=0, columnspan=2, pady=10)

        
        self.actions_frame = tk.Frame(self.root)
        self.actions_frame.pack()

        
        self.view_button = tk.Button(self.actions_frame, text="View All Products", command=self.view_products)
        self.view_button.pack(pady=10)

        
        self.purchase_button = tk.Button(self.actions_frame, text="Purchase Product", command=self.purchase_product)
        self.purchase_button.pack(pady=10)

       
        self.orders_button = tk.Button(self.actions_frame, text="View All Orders", command=self.view_orders)
        self.orders_button.pack(pady=10)

        # Create a button to log out
        self.logout_button = tk.Button(self.actions_frame, text="Logout", command=self.logout)
        self.logout_button.pack(pady=10)

        self.root.mainloop()

    
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "Please fill all fields.")
            return

        
        self.cursor.execute("SELECT * FROM customers WHERE username = %s AND password = %s", (username, password))
        customer = self.cursor.fetchone()

        if customer:
            messagebox.showinfo("Success", "Login successful!")

            
            self.login_frame.pack_forget()
            self.reg_frame.pack_forget()

            
            self.actions_frame.pack()

            
            self.username_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Invalid username or password.")

    
    def register_customer(self):
        name = self.name_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not name or not username or not password:
            messagebox.showerror("Error", "Please fill all fields.")
            return

        
        self.cursor.execute("SELECT * FROM customers WHERE username = %s", (username,))
        customer = self.cursor.fetchone()

        if customer:
            messagebox.showerror("Error", "Username already exists.")
            return

        
        self.cursor.execute("INSERT INTO customers (name, username, password) VALUES (%s, %s, %s)", (name, username, password))
        self.conn.commit()
        messagebox.showinfo("Success", "Customer registered successfully!")

       
        self.name_entry.delete(0, tk.END)
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)

    
    def view_products(self):
        
        self.cursor.execute("SELECT * FROM products")
        products = self.cursor.fetchall()

        
        view_dialog = tk.Toplevel(self.root)
        view_dialog.title("All Products")

       
        product_tree = ttk.Treeview(view_dialog, columns=("Name", "Price", "Quantity"), show="headings")
        product_tree.heading("Name", text="Product Name")
        product_tree.heading("Price", text="Price")
        product_tree.heading("Quantity", text="Quantity")
        product_tree.pack()

        
        for product in products:
            product_tree.insert("", tk.END, values=(product[1], product[2], product[3]))

    
    def purchase_product(self):
        
        self.cursor.execute("SELECT * FROM products")
        products = self.cursor.fetchall()

        
        purchase_dialog = tk.Toplevel(self.root)
        purchase_dialog.title("Purchase Product")

        
        product_listbox = tk.Listbox(purchase_dialog)
        product_listbox.pack()

        
        for product in products:
            product_listbox.insert(tk.END, f"{product[1]} - Price: {product[2]}, Quantity: {product[3]}")

        
        quantity_label = tk.Label(purchase_dialog, text="Quantity:")
        quantity_label.pack()

        
        quantity_entry = tk.Entry(purchase_dialog)
        quantity_entry.pack()

        
        purchase_button = tk.Button(purchase_dialog, text="Purchase", command=lambda: self.confirm_purchase(product_listbox, quantity_entry, purchase_dialog))
        purchase_button.pack()

    
    def confirm_purchase(self, product_listbox, quantity_entry, purchase_dialog):
        selected_product = product_listbox.get(tk.ANCHOR)
        if not selected_product:
            messagebox.showerror("Error", "Please select a product.")
            return

        try:
            quantity = int(quantity_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Quantity must be an integer.")
            return

        
        product_name = selected_product.split(" - ")[0]
        product_id = int(selected_product.split(" - ")[0].split(" ")[1])

        
        self.cursor.execute("SELECT quantity FROM products WHERE id = %s", (product_id,))
        available_quantity = self.cursor.fetchone()[0]
        if quantity > available_quantity:
            messagebox.showerror("Error", "Not enough quantity in stock.")
            return

        
        confirm_dialog = tk.Toplevel(self.root)
        confirm_dialog.title("Confirm Purchase")

        
        details_label = tk.Label(confirm_dialog, text=f"You are about to purchase {quantity} of {product_name}.")
        details_label.pack()

        
        confirm_button = tk.Button(confirm_dialog, text="Confirm", command=lambda: self.make_purchase(product_id, quantity, confirm_dialog, purchase_dialog))
        confirm_button.pack(pady=5)
        cancel_button = tk.Button(confirm_dialog, text="Cancel", command=lambda: confirm_dialog.destroy())
        cancel_button.pack()

    
    def make_purchase(self, product_id, quantity, confirm_dialog, purchase_dialog):
        
        self.cursor.execute("UPDATE products SET quantity = quantity - %s WHERE id = %s", (quantity, product_id))

        
        self.cursor.execute("INSERT INTO orders (customer_id, product_id, quantity) VALUES (%s, %s, %s)", (self.get_customer_id(), product_id, quantity))
        self.conn.commit()
        messagebox.showinfo("Success", "Purchase successful!")
        confirm_dialog.destroy()
        purchase_dialog.destroy()

    
    def get_customer_id(self):
        
        self.cursor.execute("SELECT id FROM customers WHERE username = %s", (self.username_entry.get(),))
        customer_id = self.cursor.fetchone()[0]
        return customer_id

    
    def view_orders(self):
      
        self.cursor.execute("SELECT * FROM orders WHERE customer_id = %s", (self.get_customer_id(),))
        orders = self.cursor.fetchall()

      
        view_dialog = tk.Toplevel(self.root)
        view_dialog.title("All Orders")

        
        order_tree = ttk.Treeview(view_dialog, columns=("Product", "Quantity"), show="headings")
        order_tree.heading("Product", text="Product Name")
        order_tree.heading("Quantity", text="Quantity")
        order_tree.pack()

        
        for order in orders:
            self.cursor.execute("SELECT name FROM products WHERE id = %s", (order[2],))
            product_name = self.cursor.fetchone()[0]
            order_tree.insert("", tk.END, values=(product_name, order[3]))

    
    def logout(self):
        self.root.destroy()


product_manager = ProductManager()
customer = Customer()


database = Database()
database.close_connection()
