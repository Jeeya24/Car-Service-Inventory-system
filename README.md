# Car Service Inventory system

A full-stack web application for running a car service workshop: tracking customers, their vehicles, service jobs, spare-parts inventory, suppliers and billing. Built with Flask, MySQL and SQLAlchemy as my IB Computer Science Internal Assessment.

## Features

- **Role-based login** for managers/admins and staff, with separate dashboards
- **Customer management**: register, edit and search customers
- **Vehicle management**: brand/model dropdowns, VIN tracking, and assigning vehicles to staff
- **Service records**: planned and actual start/end times, plus progress status
- **Spare parts inventory**: stock levels, prices and parts used per service
- **Supplier management**: delivery lead times and preferred suppliers
- **Billing**: generates invoices and downloadable PDF invoices
- **Email notifications** to customers on registration and when a service is completed
- **Employee management** for managers

## Tech Stack

Python · Flask · Flask-Login · SQLAlchemy · MySQL · Jinja2 · HTML/CSS/JavaScript · xhtml2pdf

## Prerequisites

- Python 3.8 or higher
- MySQL Server
- pip

## Setup

1. Clone the repository:
```bash
git clone https://github.com/Jeeya24/Car-Service-Inventory-system.git
cd Car-Service-Inventory-system
```

2. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Copy `.env.example` to `.env` and fill in your own values:
```bash
cp .env.example .env
```
| Variable | Purpose |
| --- | --- |
| `SECRET_KEY` | Flask session secret |
| `DATABASE_URL` | MySQL connection string |
| `DB_PASSWORD` | MySQL password (used by migration scripts) |
| `MAIL_USERNAME` / `MAIL_PASSWORD` | Gmail address + [app password](https://myaccount.google.com/apppasswords) for email notifications (optional) |

5. Create the MySQL database:
```sql
CREATE DATABASE car_inventory;
```
The tables are created automatically when the app starts.

## Running the Application

```bash
python app.py
```
Then open http://localhost:8083. To create demo login accounts, visit `/create-test-users` once.

## Project Structure

```
├── app.py              # Flask routes and application logic
├── models.py           # SQLAlchemy models
├── config.py           # Configuration (reads from .env)
├── car_data.py         # Car brands/models for dropdowns
├── templates/          # Jinja2 HTML templates
├── static/             # CSS and JavaScript
├── migrations/         # One-off schema migrations
├── *.sql, migrate_*.py # Schema update scripts
└── requirements.txt
```
