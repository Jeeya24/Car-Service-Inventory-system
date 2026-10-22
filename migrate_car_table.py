#!/usr/bin/env python3
"""
Simple migration to add assigned_employee_id column to car table
"""

import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def migrate_database():
    try:
        # Connect to MySQL database
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password=os.environ.get('DB_PASSWORD', ''),  # Set DB_PASSWORD in .env
            database='car_inventory'
        )
        
        cursor = connection.cursor()
        
        # Check if column already exists
        cursor.execute("SHOW COLUMNS FROM car LIKE 'assigned_employee_id'")
        if cursor.fetchone():
            print("Column 'assigned_employee_id' already exists in car table")
            return
        
        # Add the column
        cursor.execute("""
            ALTER TABLE car 
            ADD COLUMN assigned_employee_id INT NULL
        """)
        
        # Add foreign key constraint
        cursor.execute("""
            ALTER TABLE car 
            ADD CONSTRAINT fk_car_assigned_employee 
            FOREIGN KEY (assigned_employee_id) REFERENCES employee(id)
        """)
        
        connection.commit()
        print("Successfully added assigned_employee_id column to car table")
        
    except mysql.connector.Error as e:
        print(f"MySQL Error: {e}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    migrate_database()