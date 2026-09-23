#CAMPUS MAKERSPACE CHECKOUT SYSTEM

Campus MakerSpace Checkout System is a Python command-line application designed to manage members, equipment, and equipment loans in a campus MakerSpace.

The system allows users to register and manage members, register and manage equipment, borrow and return equipment, search records, and manage loan records. Data is stored persistently using an SQLite database.

This project was developed individually for the **Introduction to Programming and Databases** summative assessment.

## Project Scenario

Campus MakerSpace Checkout System**

The application is designed to support a campus MakerSpace by providing a simple system for managing equipment and the members who use it.

The system keeps track of:

- MakerSpace members
- Equipment and its availability
- Equipment loans
- Loan and return dates
- Member and equipment records

The application uses a command-line interface and an SQLite database for persistent storage.

## Key Features

- Register new MakerSpace members
- List all registered members
- Update member email addresses
- Delete members when they have no loan history
- Register new equipment
- List all equipment
- Update equipment information
- Delete equipment when it is not currently borrowed
- Track equipment availability
- Borrow equipment
- Return equipment
- View active loans
- Delete loan records
- Search members by ID, name, or email
- Search equipment by ID, name, category, or serial number
- Search active loans by loan, member, or equipment ID
- Validate user input before performing operations
- Validate dates using the `YYYY-MM-DD` format
- Prevent borrowing equipment that is unavailable
- Prevent returning equipment using an incorrect loan
- Prevent return dates from being earlier than loan dates
- Handle invalid input without crashing the application

## Project Architecture

Lab_MakerSpace_gitaumaggie/
│
├── main.py
├── models.py
├── database.py
├── services.py
├── README.md
└── .gitignore

## Architecture Explanation

| File | Purpose |
|---|---|
| `main.py` | Runs the command-line interface, displays the menu, collects user input, and connects the different parts of the application. |
| `models.py` | Contains the main object-oriented classes: `Member`, `Equipment`, and `Loan`. |
| `database.py` | Handles the SQLite database connection, table creation, SQL operations, and database persistence. |
| `services.py` | Contains validation and business logic between the user interface and database layer. |
| `README.md` | Provides an overview of the project, its architecture, features, setup instructions, and usage. |
| `.gitignore` | Prevents local database files, Python cache files, and other unnecessary files from being tracked by Git. |

## Object-Oriented Design

The application uses three main classes:

### Member

Represents a person registered with the MakerSpace.

A member has:

- Member ID
- Name
- Email address

The `Member` class also contains behaviour for updating a member's email address.

### Equipment

Represents an item of equipment available in the MakerSpace.

An equipment record contains:

- Equipment ID
- Name
- Category
- Serial number
- Availability status

The `Equipment` class contains behaviour for borrowing and returning equipment.

### Loan

Represents a borrowing transaction between a member and a piece of equipment.

A loan contains:

- Loan ID
- Member ID
- Equipment ID
- Loan date
- Return date

The `Loan` class can determine whether a loan is active and can close a loan by recording its return date.

## Database Design

The application uses SQLite through Python's built-in `sqlite3` module.

The database contains three main tables:
members
│
├── id
├── name
└── email


equipment
│
├── id
├── name
├── category
├── serial_number
└── available


loans
│
├── id
├── member_id
├── equipment_id
├── loan_date
└── return_date
```

The relationship between the tables is:

Member ──────────< Loan >────────── Equipment

A member can have multiple loans over time, and an equipment item can appear in multiple loan records over time.

The `loans` table uses foreign keys to connect each loan to a member and an equipment item.

## How the Application Works

1. The program starts from `main.py`.
2. `main.py` establishes a connection to the SQLite database.
3. The required database tables are created if they do not already exist.
4. The command-line menu is displayed.
5. The user selects an operation.
6. `main.py` collects the required input.
7. `services.py` validates the input and applies the relevant business rules.
8. `database.py` performs the required SQL operation.
9. The database is updated and the result is returned to the user.
10. The menu remains available until the user chooses to exit.

## Main Menu

When the program runs, the user sees a numbered menu similar to:

===== CAMPUS MAKERSPACE CHECKOUT SYSTEM =====

1. Register Member
2. List Members
3. Register Equipment
4. List Equipment
5. Borrow Equipment
6. Return Equipment
7. View Active Loans
8. Delete
9. Search
10. Exit

The Delete option provides additional choices for managing members, equipment, and loans.

The Search option allows users to search members, equipment, and active loans.

## Example Workflow

A typical MakerSpace workflow is:

1. Register a member
2. Register a piece of equipment
3. Borrow the equipment
4. View active loans
5. Search for the member or equipment
6. Return the equipment
7. Confirm that the equipment is available again


For example:

Member ID: 1
Equipment ID: 1
Loan date: 2026-09-23

When the equipment is successfully borrowed, its availability changes from available to unavailable.

When the equipment is returned, the loan is closed and the equipment becomes available again.

## Validation and Business Rules

The application validates input and prevents invalid operations.

| Input / Operation | Rule |
|---|---|
| Member name | Cannot be empty and must contain letters and spaces |
| Member email | Cannot be empty and must have a basic valid email format |
| Equipment name | Cannot be empty |
| Equipment category | Cannot be empty |
| Serial number | Cannot be empty and must be unique |
| Member ID | Must refer to an existing member |
| Equipment ID | Must refer to an existing equipment record |
| Borrowing equipment | Equipment must be available |
| Loan date | Must use `YYYY-MM-DD` |
| Return date | Must use `YYYY-MM-DD` |
| Return date | Cannot be earlier than the loan date |
| Returning equipment | Equipment must belong to the specified loan |
| Delete equipment | Cannot delete equipment that is currently borrowed |
| Delete member | Cannot delete a member with loan history |
| Delete loan | If an active loan is deleted, the equipment is made available again |

These rules are handled mainly in `services.py` before database changes are made.

## Search

The application provides search functionality for:

### Members

Members can be searched using:

- Member ID
- Name
- Email

### Equipment

Equipment can be searched using:

- Equipment ID
- Name
- Category
- Serial number

### Active Loans

Active loans can be searched using:

- Loan ID
- Member ID
- Equipment ID

The searches use SQL queries with `LIKE` to allow partial matches.

## Technologies Used

- Python 3
- SQLite
- Python `sqlite3` standard library
- Python `datetime`
- Git
- GitHub

No external Python packages are required.

## How to Run

Clone the repository and open the project directory in a terminal.

Run:

python3 main.py


The application will connect to the SQLite database and display the MakerSpace menu.

If the database has not yet been created, it can be initialized by running:

python3 database.py

This creates the required SQLite database and tables.

## Project Files


main.py
Contains the command-line interface and application flow.

models.py
Contains the `Member`, `Equipment`, and `Loan` classes.

database.py
Contains SQLite database connection, table creation, and SQL operations.

services.py
Contains validation and business logic.

README.md
Contains project documentation.

.gitignore
Prevents local database files and Python cache files from being uploaded to GitHub.


## Database Files

The application creates a local SQLite database:

makerspace.db
A local backup may also be created during development:

makerspace_backup.db
These files are intentionally excluded from GitHub using `.gitignore`.

The source code is stored in the repository, while the local database is created when the application is run.

## AI Assistance Disclosure
AI tools were used as a learning and development aid during this project.
AI assistance was used to:

- Help understand Python concepts and error messages
- Suggest and explain docstrings and code comments
- Help clarify programming concepts
- Assist with debugging and interpreting errors
- Support understanding of Git and GitHub commands

The overall application architecture, class structure, database design, business logic, and implementation were developed by me.

I wrote and integrated the application code and tested the system myself. I understand how the different components work together, including the object-oriented classes, SQLite database operations, validation logic, service layer, and command-line interface.

AI was therefore used as a supporting learning and debugging tool rather than as a replacement for understanding or developing the complete application.

## Assessment Scope

This project demonstrates:
- Variables and data types
- Conditional statements
- Loops
- Functions
- Exception handling
- Input validation
- Object-oriented programming
- Classes and objects
- Methods and attributes
- Modular Python programming
- SQLite database operations
- SQL queries
- CRUD operations
- Foreign keys
- Searching and filtering
- Command-line application design
- Git and GitHub version control

## Author

Margaret Gitau
BSc (Hons) Software Engineering  
Africa Leadership College of Higher Education (ALCHE)
GitHub: (gitaumaggie)


