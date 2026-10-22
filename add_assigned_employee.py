#!/usr/bin/env python3
"""
Migration script to add assigned_employee_id column to car table
"""

from app import app, db
from sqlalchemy import text

def add_assigned_employee_column():
    """Add assigned_employee_id column to car table"""
    try:
        with app.app_context():
            with db.engine.connect() as connection:
                # Check if column already exists
                result = connection.execute(text("SHOW COLUMNS FROM car LIKE 'assigned_employee_id'"))
                if result.fetchone():
                    print("Column 'assigned_employee_id' already exists in car table")
                    return
                
                # Add the column
                connection.execute(text("""
                    ALTER TABLE car 
                    ADD COLUMN assigned_employee_id INT NULL,
                    ADD CONSTRAINT fk_car_assigned_employee 
                    FOREIGN KEY (assigned_employee_id) REFERENCES employee(id)
                """))
                connection.commit()
                print("Successfully added assigned_employee_id column to car table")
                
    except Exception as e:
        print(f"Error adding column: {e}")

if __name__ == "__main__":
    add_assigned_employee_column()