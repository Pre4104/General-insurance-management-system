import mysql.connector
import random
import string

def create_connection():
    try:
        conn = mysql.connector.connect(
            host="host(%)",
            user="CS",
            password="root171861",
            database="insurance_company"
        )
        print("Connection successful")
        return conn
    except Error as e:
        print(e)
        return None

def close_connection(conn):
    conn.close()

def create_table(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS customers")
        cursor.execute("DROP TABLE IF EXISTS policies")
        cursor.execute("DROP TABLE IF EXISTS change_requests")

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
        print("Tables created successfully")
    except Error as e:
        print(e)

def insert_customer(conn, customer):
    cursor = conn.cursor()
    sql = """ INSERT INTO customers (name, email) VALUES (%s, %s) """
    cursor.execute(sql, customer)
    conn.commit()
    print("Customer inserted successfully")

def insert_policy(conn, policy):
    cursor = conn.cursor()
    sql = """ INSERT INTO policies (customer_id, policy_type, premium) VALUES (%s, %s, %s) """
    cursor.execute(sql, policy)
    conn.commit()
    print("Policy inserted successfully")

def request_policy_change(conn, change_request):
    cursor = conn.cursor()
    sql = """ INSERT INTO change_requests (policy_id, new_policy_type, new_premium) VALUES (%s, %s, %s) """
    cursor.execute(sql, change_request)
    conn.commit()
    print("Policy change request inserted successfully")

def view_customer_policies(conn, customer_id):
    cursor = conn.cursor()
    sql = """ SELECT * FROM policies WHERE customer_id = %s """
    cursor.execute(sql, (customer_id,))
    policies = cursor.fetchall()
    return policies

def view_policy_change_requests(conn, policy_id):
    cursor = conn.cursor()
    sql = """ SELECT * FROM change_requests WHERE policy_id = %s """
    cursor.execute(sql, (policy_id,))
    change_requests = cursor.fetchall()
    return change_requests
