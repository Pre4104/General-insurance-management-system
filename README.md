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
