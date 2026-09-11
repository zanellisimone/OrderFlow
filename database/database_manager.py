import sqlite3
from contextlib import closing
from model import Client, Order, OrderStatus, OrderLine, Product
from services import OrderFlowManager
from pathlib import Path
from datetime import datetime

class DatabaseManager:
    def __init__(self, directory : Path | None) -> None:
        if directory is not None and not isinstance(directory, Path):
            raise TypeError("The directory must be None or an instance of Path class!")
        if directory is None:
            directory = Path(__file__).resolve().parent
        directory.mkdir(exist_ok=True, parents=True)
        self.__file_db = directory / "order_flow_database.db"
        self.__create_tables()

    def __create_tables(self) -> None:
        with closing(sqlite3.connect(self.__file_db)) as connection:
            cursor = connection.cursor()
            try:
                cursor.execute("PRAGMA foreign_keys = ON;")
                self.__create_clients_table(connection)
                self.__create_products_table(connection)
                self.__create_orders_table(connection)
                self.__create_order_lines_table(connection)
                connection.commit()
            except sqlite3.Error as error:
                connection.rollback()
                raise ValueError("Something went wrong while creating the tables...") from error

    def __create_clients_table(self, connection : sqlite3.Connection) -> None:
        cursor = connection.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS clients(
                id_client TEXT PRIMARY KEY CHECK(id_client GLOB 'C[0-9][0-9][0-9][0-9]'),
                name TEXT NOT NULL CHECK(TRIM(name) <> ''),
                surname TEXT NOT NULL CHECK(TRIM(surname) <> ''),
                email TEXT NOT NULL UNIQUE CHECK(TRIM(email) <> ''),
                phone TEXT
            )
            """)

    def __create_products_table(self, connection : sqlite3.Connection) -> None:
        cursor = connection.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS products(
                id_product TEXT PRIMARY KEY CHECK(id_product GLOB 'P[0-9][0-9][0-9][0-9]'),
                name TEXT NOT NULL CHECK(TRIM(name) <> ''),
                category TEXT NOT NULL CHECK(TRIM(category) <> ''),
                price REAL NOT NULL CHECK(price > 0),
                quantity_available INTEGER NOT NULL CHECK(quantity_available >= 0)
            )
            """
        )

    def __create_orders_table(self, connection : sqlite3.Connection) -> None:
        cursor = connection.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS orders(
                id_order TEXT PRIMARY KEY CHECK(id_order GLOB 'O[0-9][0-9][0-9][0-9]'),
                id_client TEXT NOT NULL,
                creation_date TEXT NOT NULL,
                status TEXT NOT NULL CHECK(status IN ('DRAFT', 'CONFIRMED', 'CANCELLED', 'SHIPPED')),
                FOREIGN KEY (id_client) REFERENCES clients(id_client) ON DELETE RESTRICT
            )
            """)

    def __create_order_lines_table(self, connection : sqlite3.Connection) -> None:
        cursor = connection.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS order_lines(
                id_order TEXT NOT NULL,
                id_product TEXT NOT NULL,
                quantity INTEGER NOT NULL CHECK(quantity > 0),
                unit_price REAL NOT NULL CHECK(unit_price > 0),
                PRIMARY KEY(id_order, id_product),
                FOREIGN KEY (id_order) REFERENCES orders(id_order) ON DELETE CASCADE,
                FOREIGN KEY (id_product) REFERENCES products(id_product) ON DELETE RESTRICT
            )
            """)

    def __clear_tables(self, connection : sqlite3.Connection) -> None:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM order_lines;")
        cursor.execute("DELETE FROM orders;")
        cursor.execute("DELETE FROM products;")
        cursor.execute("DELETE FROM clients;")

    def save(self, manager : OrderFlowManager) -> None:
        if not isinstance(manager, OrderFlowManager):
            raise TypeError("The argument must be an instance of OrderFlowManager class!")
        with closing(sqlite3.connect(self.__file_db)) as connection:
            try:
                connection.execute("PRAGMA foreign_keys = ON;")
                self.__clear_tables(connection)
                self.__save_clients(connection, manager)
                self.__save_products(connection, manager)
                self.__save_orders(connection, manager)
                self.__save_order_lines(connection, manager)
                connection.commit()
            except sqlite3.Error as error:
                connection.rollback()
                raise ValueError("Something went wrong while saving...") from error

    def __save_clients(self, connection : sqlite3.Connection, manager : OrderFlowManager) -> None:
        cursor = connection.cursor()
        for client in manager.get_clients():
            cursor.execute("INSERT INTO clients(id_client, name, surname, email, phone) VALUES (?,?,?,?,?)", 
                           (client.id_client, client.name, client.surname, client.email, client.phone))
            
    def __save_products(self, connection : sqlite3.Connection, manager : OrderFlowManager) -> None:
        cursor = connection.cursor()
        for product in manager.get_products():
            cursor.execute("INSERT INTO products(id_product, name, category, price, quantity_available) VALUES (?,?,?,?,?)",
                           (product.id_product, product.name, product.category, product.price, product.quantity_available))

    def __save_orders(self, connection : sqlite3.Connection, manager : OrderFlowManager) -> None:
        cursor = connection.cursor()
        for order in manager.get_orders():
            cursor.execute("INSERT INTO orders(id_order, id_client, creation_date, status) VALUES (?,?,?,?)", 
                           (order.id_order, order.client.id_client, order.creation_date.isoformat(), order.status.name))

    def __save_order_lines(self, connection : sqlite3.Connection, manager : OrderFlowManager) -> None:
        cursor = connection.cursor()
        for order in manager.get_orders():
            for line in order.lines:
                cursor.execute("INSERT INTO order_lines(id_order, id_product, quantity, unit_price) VALUES (?,?,?,?)",
                               (order.id_order, line.product.id_product, line.quantity, line.unit_price))

    def load(self) -> OrderFlowManager:
        manager = OrderFlowManager()
        with closing(sqlite3.connect(self.__file_db)) as connection:
            try:
                connection.execute("PRAGMA foreign_keys = ON;")
                self.__load_clients(connection, manager)
                self.__load_products(connection, manager)
                self.__load_orders(connection, manager)
                self.__load_order_lines(connection, manager)
            except sqlite3.Error as error:
                raise ValueError("Something went wrong while loading...") from error
        return manager

    def __load_clients(self, connection : sqlite3.Connection, manager : OrderFlowManager) -> None:
        cursor = connection.cursor()
        cursor.execute("SELECT id_client, surname, name, email, phone FROM clients;")
        clients = cursor.fetchall()
        for id_client, surname, name, email, phone in clients:
            manager.add_client(Client(id_client, surname, name, email, phone))

    def __load_products(self, connection : sqlite3.Connection, manager : OrderFlowManager) -> None:
        cursor = connection.cursor()
        cursor.execute("SELECT id_product, name, category, price, quantity_available FROM products;")
        products = cursor.fetchall()
        for id_product, name, category, price, quantity_available in products:
            manager.add_product(Product(id_product, name, category, price, quantity_available))

    def __load_orders(self, connection : sqlite3.Connection, manager : OrderFlowManager) -> None:
        cursor = connection.cursor()
        cursor.execute("SELECT id_order, id_client, creation_date, status FROM orders;")
        orders = cursor.fetchall()
        for id_order, id_client, creation_date, status in orders:
            creation_date = datetime.fromisoformat(creation_date)
            status = OrderStatus[status]
            client = manager.get_client(id_client)
            order = Order(id_order, client, creation_date, status)
            manager.add_order(order)

    def __load_order_lines(self, connection : sqlite3.Connection, manager : OrderFlowManager) -> None:
        cursor = connection.cursor()
        cursor.execute("SELECT id_order, id_product, quantity, unit_price FROM order_lines;")
        order_lines = cursor.fetchall()
        for id_order, id_product, quantity, unit_price in order_lines:
            order = manager.get_order(id_order)
            product = manager.get_product(id_product)
            order.add_loaded_line(OrderLine(product, quantity, unit_price))