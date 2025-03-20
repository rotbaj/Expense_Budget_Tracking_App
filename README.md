# Step 1: Project Setup and Configuration

## Objective

To set up a new Django project for the Expense & Budget Tracker, including environment configuration, app creation, initial models, and database setup.

## Task Description

### Step 1: Project Setup

* Install Django:
    ```bash
    pip install django
    ```
* Install Django REST Framework:
    ```bash
    pip install djangorestframework
    ```
* Start a new Django project:
    ```bash
    django-admin startproject expense_tracker
    ```
* Navigate into the project directory:
    ```bash
    cd expense_tracker
    ```
* Create a new Django app:
    ```bash
    python manage.py startapp core
    ```
* Register the 'core' app and 'rest\_framework' in `INSTALLED_APPS` in `expense_tracker/settings.py`.

### Step 2: Configure the Database

* Configure PostgreSQL or use SQLite by adjusting the `DATABASES` setting in `settings.py`.

### Step 3: Define Models

* Create models in `core/models.py` based on the ERD:
    * `User`: Use Django's built-in `User` model.
    * `Expense`:
        * `user_id` (ForeignKey to `User`)
        * `amount` (Decimal)
        * `category` (String)  (e.g., Food, Rent, Entertainment) [cite: 5, 28]
        * `description` (Text, Optional)
        * `date` (Date)
    * `Income`:
        * `user_id` (ForeignKey to `User`)
        * `amount` (Decimal)
        * `category` (String) (e.g., Salary, Freelance, Investments) [cite: 7, 28]
        * `description` (Text, Optional)
        * `date` (Date)
    * `Budget`:
        * `user_id` (ForeignKey to `User`)
        * `amount` (Decimal)
        * `category` (String)  (e.g., Food, Rent, Transport) [cite: 28, 29]
        * `description` (Text, Optional)
        * `start_date` (Date)
        * `end_date` (Date)
* Run migrations:
    ```bash
    python manage.py makemigrations core
    ```
    ```bash
    python manage.py migrate
    ```

