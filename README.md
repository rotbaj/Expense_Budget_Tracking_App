# Expense & Budget Tracking App 💰📊

[![Django](https://img.shields.io/badge/Django-3.2-green.svg)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.12-blue.svg)](https://www.django-rest-framework.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This Django-based web application helps users manage their personal finances by tracking expenses and budgets. It provides a user-friendly interface to record income, categorize spending, and set up budgets to monitor financial health.


## Features ✨

### Core Functionality
- **Expense Tracking**: Record and categorize daily expenses
- **Income Management**: Track income sources and amounts
- **Budget Planning**: Set monthly budgets by categories
- **Financial Reports**: Generate spending insights and trends
- **User Authentication**: Secure signup/login system

### Advanced Features
- Budget progress tracking with visual indicators
- Spending analysis by category/time period
- Income vs. expense comparisons
- Custom report presets
- Responsive web interface

## Tech Stack 🛠️

**Backend:**
- Python 3.9+
- Django 3.2
- Django REST Framework
- PostgreSQL (default SQLite for development)

**Frontend:**
- HTML5, CSS3, JavaScript
- Bootstrap 5
- Chart.js for visualizations

**APIs:**
- RESTful API endpoints
- JWT Authentication
- Filtering/Search capabilities


## Setup Instructions 🚀

1.  **Clone the repository:**

    ```bash
    git clone <repository_url>
    cd Expense_Budget_Tracking_App
    ```

2.  **Create a virtual environment (recommended):**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Linux/macOS
    venv\Scripts\activate  # On Windows
    ```

3.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt  # You'll need to create this file
    ```

4.  **Apply migrations:**

    ```bash
    python manage.py migrate
    ```

5.  **Create a superuser (for admin access):**

    ```bash
    python manage.py createsuperuser
    ```

6.  **Run the development server:**

    ```bash
    python manage.py runserver
    ```

7.  **Access the application in your browser:**

    ```
    http://localhost:8000/
    ```