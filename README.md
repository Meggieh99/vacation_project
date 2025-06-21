# Vacation Management System
A full-stack Django-based application for managing vacations, including user and admin roles, like/unlike functionality, and vacation CRUD operations.

## Student
Full Name:Meggie Hadad

## Technologies
- Python 3.x
- Django
- PostgreSQL
- HTML/CSS/JavaScript (Part II)

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Meggieh99/vacation_project
   cd project

2. Create a virtual environment
python -m venv .venv
source .venv/Scripts/activate

3. Install dependencies
pip install -r requirements.txt

4. Database setup / migration
Create databases
In PostgreSQL:
CREATE DATABASE vacation_db;
CREATE DATABASE test_db;

5. Run main setup
This will apply migrations, load initial data, and run tests:
python main.py

Alternatively, you can run:
python manage.py migrate
python manage.py init_data


6. Running the project
Start the Django server:
python manage.py runserver

7. Running tests
You can run all tests with:
python main.py

Or directly via Django:
python manage.py test vacations

**
Tests run on a separate test database (test_db) and initialize fresh data on each run.
The main entry point for running tests and setting up the DB is main.py.


Enjoy Your Vacation :),


