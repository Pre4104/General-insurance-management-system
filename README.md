# General-insurance-management-system
A Python + MySQL based insurance management system for customers and underwriters

A database-driven desktop application built with **Python 3.12** and **MySQL 8.0**
for managing general insurance policies. Developed as a Investigatory

---

## About the Project

This system provides two separate interfaces — one for **customers** and one
for **underwriters** — to manage insurance policies efficiently, replacing
manual paperwork.

---

## Features

### Customer
- View insurance policy details using Party Code
- Submit requests to change personal details

### Underwriter (Password Protected)
- Add a new policy (auto-generates Party Code)
- Update an existing policy
- Cancel a policy
- Renew a policy (extends dates by 1 year)
- Display all policies
- View change requests submitted by customers

---

## Insurance Types Supported

| Code | Type              | Product Code |
|------|-------------------|--------------|
| TW, PC, CV | Motor Insurance  | 31 |
| NP, TU, UK | Health Insurance | 34 |
| FS         | Fire Insurance   | 11 |
| SH, MI, BI | Miscellaneous    | 46 |
| PU         | Personal Accident| 42 |

---

## Project Structure
├── source_code.py       # Main application file
├── blackbox_SQL_.py     # Database connection and table setup
├── party_code.py        # Party code generation logic
├── party_code.txt       # Stores used party codes
├── Requests.csv         # Stores customer change requests

---

## How to Run

### Prerequisites
- Python 3.12
- MySQL Server 8.0
- `mysql-connector-python` library

### Installation

```bash
pip install mysql-connector-python
```

### Database Setup

1. Open MySQL and create the database:
```sql
CREATE DATABASE Insurance_Company;
```

2. Create the `Customer_Details` table:
```sql
USE Insurance_Company;
CREATE TABLE Customer_Details (
    party_code BIGINT PRIMARY KEY,
    Name VARCHAR(25) NOT NULL,
    Phone_no VARCHAR(10) NOT NULL,
    Address VARCHAR(50),
    Type_of_Insurance VARCHAR(5),
    Email VARCHAR(50),
    Pincode INT,
    Policy_Start_Date DATE,
    Policy_End_Date DATE
);
```

3. Update the database credentials in `source_code.py`:
```python
connection = mysql.connector.connect(
    host="localhost",
    user="your_username",
    password="your_password",
    database="Insurance_Company"
)
```

### Run the Program

```bash
python source_code.py
```

---

## Technologies Used

- **Language:** Python 3.12
- **Database:** MySQL 8.0
- **Libraries:** `mysql-connector-python`, `datetime`, `csv`, `random` 
---

## Disclaimer

This project was created for educational purposes. Database credentials in the code should be changed
before any real-world use.
