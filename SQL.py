import mysql.connector
from mysql.connector import Error 


def create_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",          # e.g. "localhost" or your DB host
            user="YOUR_DB_USER",       # e.g. "CS"
            password="YOUR_DB_PASSWORD",
            database="insurance_company"
        )
        print("Connection successful")
        return conn
    except Error as e:
        print(e)
        return None


def close_connection(conn):
    if conn is not None and conn.is_connected():
        conn.close()


def create_table(conn):
    """FIX: wrapped in try/except using the now-imported Error class."""
    try:
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS change_requests")
        cursor.execute("DROP TABLE IF EXISTS policies")
        cursor.execute("DROP TABLE IF EXISTS customers")

        cursor.execute("""
            CREATE TABLE customers (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(50) NOT NULL,
                email VARCHAR(50) NOT NULL UNIQUE
            )
        """)

        cursor.execute("""
            CREATE TABLE policies (
                id INT AUTO_INCREMENT PRIMARY KEY,
                customer_id INT NOT NULL,
                policy_type VARCHAR(20) NOT NULL,
                premium DECIMAL(10, 2) NOT NULL,
                FOREIGN KEY (customer_id) REFERENCES customers(id)
            )
        """)

        cursor.execute("""
            CREATE TABLE change_requests (
                id INT AUTO_INCREMENT PRIMARY KEY,
                policy_id INT NOT NULL,
                new_policy_type VARCHAR(20),
                new_premium DECIMAL(10, 2),
                FOREIGN KEY (policy_id) REFERENCES policies(id)
            )
        """)
        conn.commit()  
        print("Tables created successfully")
    except Error as e:
        print(e)


def insert_customer(conn, customer):
    """customer = (name, email)"""
    try:
        cursor = conn.cursor()
        sql = "INSERT INTO customers (name, email) VALUES (%s, %s)"
        cursor.execute(sql, customer)
        conn.commit()
        print("Customer inserted successfully")
        return cursor.lastrowid  
    except Error as e:
        print(e)
        return None


def insert_policy(conn, policy):
    """policy = (customer_id, policy_type, premium)"""
    try:
        cursor = conn.cursor()
        sql = "INSERT INTO policies (customer_id, policy_type, premium) VALUES (%s, %s, %s)"
        cursor.execute(sql, policy)
        conn.commit()
        print("Policy inserted successfully")
        return cursor.lastrowid
    except Error as e:
        print(e)
        return None


def request_policy_change(conn, change_request):
    """change_request = (policy_id, new_policy_type, new_premium)"""
    try:
        cursor = conn.cursor()
        sql = """ INSERT INTO change_requests (policy_id, new_policy_type, new_premium)
                  VALUES (%s, %s, %s) """
        cursor.execute(sql, change_request)
        conn.commit()
        print("Policy change request inserted successfully")
        return cursor.lastrowid
    except Error as e:
        print(e)
        return None


def view_customer_policies(conn, customer_id):
    try:
        cursor = conn.cursor()
        sql = "SELECT * FROM policies WHERE customer_id = %s"
        cursor.execute(sql, (customer_id,))
        return cursor.fetchall()
    except Error as e:
        print(e)
        return []


def view_policy_change_requests(conn, policy_id):
    try:
        cursor = conn.cursor()
        sql = "SELECT * FROM change_requests WHERE policy_id = %s"
        cursor.execute(sql, (policy_id,))
        return cursor.fetchall()
    except Error as e:
        print(e)
        return []
