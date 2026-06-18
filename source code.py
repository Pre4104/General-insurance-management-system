import mysql.connector
import datetime
import csv
import random
import hashlib

# ── DATABASE CONNECTION ────────────────────────────────────────────────────────
connection = mysql.connector.connect(
    host="localhost",
    user="root",           # Enter your username
    password="YOUR_PASSWORD",  # Enter your password
    database="Insurance_Company"
)
cursor = connection.cursor()

# ── CONSTANTS ──────────────────────────────────────────────────────────────────
INSURANCE_TYPES = {
    "TW": "31", "PC": "31", "CV": "31",   # Motor
    "NP": "34", "TU": "34", "UK": "34",   # Health
    "FS": "11",                             # Fire
    "SH": "46", "MI": "46", "BI": "46",   # Miscellaneous
    "PU": "42",                             # Personal Accident
}
BRANCH_NO = "67200"

UNDERWRITER_PASSWORD_HASH = hashlib.sha256("Enter your password".encode()).hexdigest()

DB_COLUMNS = [
    "Party Code", "Name", "Phone No.", "City",
    "Type of Insurance", "Email", "Pincode",
    "Policy Start Date", "Policy End Date"
]


# ── PARTY CODE GENERATOR ───────────────────────────────────────────────────────
def generate_party_code(type_of_insurance, year):

    if type_of_insurance not in INSURANCE_TYPES:
        print("Invalid insurance type.")
        return None

    product_code = INSURANCE_TYPES[type_of_insurance]
    random_no = random.randint(10000000, 99999999)
    code = BRANCH_NO + product_code + str(year) + str(random_no)

    # Check for duplicates in file and regenerate if needed
    try:
        with open("party_code.txt", "r") as file:
            existing = file.read().splitlines()
    except FileNotFoundError:
        existing = []

    if code in existing:
        return generate_party_code(type_of_insurance, year)  

    with open("party_code.txt", "a") as file:  
        file.write(code + "\n")

    return int(code)


# ── HELPERS ────────────────────────────────────────────────────────────────────
def name_from_database(party_code):
    query = "SELECT Name FROM Customer_Details WHERE party_code = %s"
    cursor.execute(query, (party_code,))
    result = cursor.fetchone()
    return result[0] if result else None


def password_checking():
    pwd = input("Enter the password: ")
    pwd_hash = hashlib.sha256(pwd.encode()).hexdigest()
    if pwd_hash == UNDERWRITER_PASSWORD_HASH:
        underwriter()
    else:
        print("Access Denied.")


# ── DATA COLLECTION ────────────────────────────────────────────────────────────
def data_from_user():
    """
    Fixes:
    - Date variable mixup (yr/mn/dt vs year/month/date) corrected
    - start_date now correctly uses start date variables
    """
    while True:
        name = input("Enter your name (max 25 characters): ")
        if len(name) <= 25:
            break
        print("Name should have maximum 25 characters.")

    while True:
        phno = input("Enter your phone number: ")
        if len(phno) == 10 and phno.isdigit():
            break
        print("Phone number should contain exactly 10 digits.")

    while True:
        address = input("Enter your city/address (max 50 characters): ")
        if len(address) <= 50:
            break
        print("Address should have maximum 50 characters.")

    while True:
        type_of_insurance = input(f"Enter type of insurance {list(INSURANCE_TYPES.keys())}: ").upper()
        if type_of_insurance in INSURANCE_TYPES:
            break
        print("Invalid insurance type. Please try again.")

    email = input("Enter your email: ")

    while True:
        try:
            pincode = int(input("Enter the pincode: "))
            if 100000 <= pincode <= 999999:
                break
        except ValueError:
            pass
        print("Enter a valid 6-digit pincode.")

    while True:
        try:
            start_str = input("Enter the policy start date (YYYY-MM-DD): ").split('-')
            end_str = input("Enter the policy end date (YYYY-MM-DD): ").split('-')

            # FIX: use start_str for start_date, end_str for end_date (was mixed up before)
            s_yr, s_mn, s_dt = int(start_str[0]), int(start_str[1]), int(start_str[2])
            e_yr, e_mn, e_dt = int(end_str[0]), int(end_str[1]), int(end_str[2])

            start_date = datetime.date(s_yr, s_mn, s_dt)
            end_date = datetime.date(e_yr, e_mn, e_dt)

            if end_date <= start_date:
                print("End date must be after start date.")
                continue
            break
        except (ValueError, IndexError):
            print("Invalid date format. Use YYYY-MM-DD.")

    century_prefix = s_yr // 100
    pc = generate_party_code(type_of_insurance, century_prefix)
    return pc, name, phno, address, type_of_insurance, email, pincode, start_date, end_date


# ── CUSTOMER MODULE ────────────────────────────────────────────────────────────
def customer():
    """
    Fixes:
    - SQL injection in view details fixed (parameterised query)
    - 'detailno' NameError fixed — now correctly uses 'detail' variable
    """
    party_code = input("Enter your party code: ")
    name = name_from_database(party_code)

    if name is None:
        print("Party Code doesn't exist.")
        return

    print(f"Welcome, {name}!")
    print("""
    What would you like to do?
    1. View your details
    2. Request a change to your details""")

    choice = input("Enter your choice: ").strip()

    if choice == "1":
        # FIX: parameterised query instead of string concatenation
        cursor.execute("SELECT * FROM Customer_Details WHERE party_code = %s", (party_code,))
        results = cursor.fetchall()
        for row in results:
            for label, value in zip(DB_COLUMNS, row):
                print(f"{label}: {value}")

    elif choice == "2":
        print("""
    Detail Number — Field
    1  — Name
    2  — Phone No.
    3  — Address
    4  — Type of Insurance
    5  — Email
    6  — Pincode
    7  — Policy Start Date
    8  — Policy End Date""")

        with open("Requests.csv", "a", newline="") as file:
            csvwriter = csv.writer(file)
            while True:
                detail = input("Enter the detail number (1-8): ").strip()  # FIX: was 'detailno' (undefined)
                if detail not in [str(i) for i in range(1, 9)]:
                    print("Invalid detail number.")
                    continue
                value = input("Enter the new value: ")
                csvwriter.writerow([party_code, detail, value])
                ch = input("Request another change? (y/n): ")
                if ch.lower() == 'n':
                    print("Your request has been successfully submitted.")
                    break
    else:
        print("Invalid choice.")


# ── UNDERWRITER MODULE ─────────────────────────────────────────────────────────
def add_policy(data):
    query = "INSERT INTO Customer_Details VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(query, data)
    connection.commit()  # FIX: commit added


def updating_the_policy():
    """
    Fixes:
    - String vs int comparison fixed (no == "1" not no == 1)
    - commit() added
    """
    field_map = {
        "1": "Name",
        "2": "Phone_no",
        "3": "Address",
        "4": "Type_of_Insurance",
        "5": "Email",
        "6": "Pincode",
        "7": "Policy_Start_Date",
        "8": "Policy_End_Date",
    }

    with open("Requests.csv", "r+", newline="") as file:
        csvreader = csv.reader(file)
        rows = list(csvreader)
        for row in rows:
            if len(row) == 0:
                continue
            pc, no, value = row
            if no not in field_map:  # FIX: comparing strings to strings
                print(f"Unknown field number '{no}', skipping.")
                continue
            column = field_map[no]
            query = f"UPDATE Customer_Details SET {column} = %s WHERE party_code = %s"
            cursor.execute(query, (value, pc))
        connection.commit()  # FIX: commit added
        file.seek(0)
        file.truncate()
    print("Requests processed and cleared.")


def canceling_a_policy():
    """Fix: parameterised queries instead of f-strings; commit() added."""
    party_code = input("Enter the party code: ").strip()
    cursor.execute("SELECT * FROM Customer_Details WHERE party_code = %s", (party_code,))
    result = cursor.fetchone()
    if result:
        cursor.execute("DELETE FROM Customer_Details WHERE party_code = %s", (party_code,))
        connection.commit()  # FIX: commit added
        print(f"Policy {party_code} has been cancelled successfully.")
    else:
        print(f"No policy found with party code {party_code}.")


def renew_a_policy():
    """Fix: parameterised query; commit() added."""
    party_code = input("Enter the party code: ").strip()
    query = """
        UPDATE Customer_Details
        SET Policy_Start_Date = DATE_ADD(Policy_Start_Date, INTERVAL 1 YEAR),
            Policy_End_Date   = DATE_ADD(Policy_End_Date,   INTERVAL 1 YEAR)
        WHERE party_code = %s
    """
    cursor.execute(query, (party_code,))  # FIX: parameterised
    connection.commit()  # FIX: commit added
    print(f"Policy {party_code} renewed successfully.")


def display_policies():
    """
    Fixes:
    - Label list order corrected to match DB column order
    - Renamed 'list' variable to 'labels' (shadows built-in otherwise)
    """
    cursor.execute("SELECT * FROM Customer_Details")
    results = cursor.fetchall()
    if not results:
        print("No policies found.")
        return
    for row in results:
        print("-" * 60)
        for label, value in zip(DB_COLUMNS, row):  # FIX: use shared DB_COLUMNS constant
            print(f"  {label}: {value}")
    print("-" * 60)


def view_requests():
    try:
        with open("Requests.csv") as file:
            csvreader = csv.reader(file)
            rows = [row for row in csvreader if row]
            if not rows:
                print("No pending requests.")
            for row in rows:
                print(row)
    except FileNotFoundError:
        print("No requests file found.")


# ── UNDERWRITER MENU ───────────────────────────────────────────────────────────
def underwriter():
    print('-' * 60)
    print("""
    What would you like to do?
    1. Add a new policy
    2. Process update requests
    3. Cancel a policy
    4. Renew a policy
    5. Display all policies
    6. View change requests from customers
    7. Exit""")

    valid_choices = {'1', '2', '3', '4', '5', '6', '7'}  # FIX: proper set, not string membership
    while True:
        choice = input("Enter your choice: ").strip()
        if choice not in valid_choices:
            print("Enter a valid choice (1–7).")
        elif choice == '1':
            data = data_from_user()
            if data:
                add_policy(data)
                print("Policy added successfully.")
        elif choice == '2':
            updating_the_policy()
        elif choice == '3':
            canceling_a_policy()
        elif choice == '4':
            renew_a_policy()
        elif choice == '5':
            display_policies()
        elif choice == '6':
            view_requests()
        elif choice == '7':
            print("Session ended.")
            print('-' * 60)
            break


# ── ENTRY POINT ────────────────────────────────────────────────────────────────
print(" " * 20, "Welcome to the Insurance Management System")
print("""
1. Customer
2. Underwriter""")

while True:
    choice = input("Enter your choice: ").strip()
    if choice == '1':
        customer()
        break
    elif choice == '2':
        password_checking()
        break
    else:
        print("Please enter 1 or 2.")
