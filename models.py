#File need to be runned once!
import sqlite3

class DBManager:
    def __init__(self):
        """Connecting to the database and creating fields"""
        self.connection = sqlite3.connect('db.db')
        self.cursor = self.connection.cursor()
    
    def get_product(self, product):
        """Get item from database"""
        with self.connection:
            query = self.cursor.execute(f"SELECT * FROM products WHERE name = '{product}';").fetchall()
            return list(query[0])
    def get_from_category(self, category):
        """Get all products from a category"""
        with self.connection:
            query = self.cursor.execute(f"SELECT name FROM products WHERE category = '{category}';").fetchall()
            products = []
            for i in query:
                products.append(i[0])
            return products
    def get_categories(self):
        """Get all product categories"""
        with self.connection:
            query = self.cursor.execute("SELECT category FROM products;").fetchall()
            categories = []
            for i in query:
                categories.append(i[0])
            return categories
    def get_products(self):
        """Get the names of all products"""
        with self.connection:
            query = self.cursor.execute("SELECT name FROM products;").fetchall()
            products = []
            for i in query:
                products.append(i[0])
            return products
