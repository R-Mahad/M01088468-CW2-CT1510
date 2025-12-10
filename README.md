 Week 08 – Database Integration and Testing

This week’s task was to connect our Python project to a SQLite database, create the required tables, load data from CSV files, and test basic CRUD-style functions. The aim was to show that the whole system works from end to end.

---

 1. Database Setup

The database file is stored in:
DATA/intelligence_platform.db

I used the functions in `app/data/schema.py` to create all four tables:

- users  
- cyber_incidents  
- datasets_metadata  
- it_tickets  

These tables are created automatically when running `main.py`.



 2. User Functions

User-related actions are inside:app/data/users.py
This includes:

- adding a user  
- hashing passwords  
- checking a password hash  
- getting all users  

There is also a migration function in:

app/services/user_service.py

It reads from `DATA/users.txt` and inserts users into the database.



 3. Loading CSV Data

I loaded the following files into the database using pandas:

DATA/cyber_incidents.csv
DATA/datasets_metadata.csv
DATA/it_tickets.csv


Each file is written into its matching database table.  
This step happens inside *\main.py*.

---

 4. Incident, Dataset, and Ticket Functions

Each data area has simple CRUD-style read functions:

 Cyber Incidents  
Located in `app/data/incidents.py`  
- get all incidents  
- filter by severity  
- filter by status  

 Datasets  
Located in `app/data/datasets.py`  
- get all dataset metadata  

 IT Tickets  
Located in `app/data/tickets.py`  
- get all tickets  

All SQL queries use `?` placeholders to prevent SQL injection.



5. Testing the System

All testing is done in:
main.py


When I run it, it:

1. Connects to the database  
2. Creates all tables  
3. Migrates users  
4. Loads all CSV data  
5. Runs all the query functions  
6. Prints the results  
7. Closes the database connection  

Seeing the output confirms that the database is populated and the queries work correctly.

![alt text](image.png)