#!/usr/bin/env python3
"""
Database viewer script for Car Service Management System
This script connects to the MySQL database and displays its structure
"""

import os
import sys
from sqlalchemy import create_engine, inspect, text
from tabulate import tabulate
import configparser

# Try to import from the application to reuse database configuration
try:
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from app import app, db
    print("Successfully imported database configuration from app")
    engine = db.engine
except ImportError:
    print("Could not import from app, using default configuration")
    # Default database configuration
    DB_USER = 'root'
    DB_PASSWORD = ''
    DB_HOST = 'localhost'
    DB_NAME = 'car_inventory'
    
    # Create SQLAlchemy engine
    engine = create_engine(f'mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}')

def show_tables():
    """Display all tables in the database"""
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    
    print("\n=== DATABASE TABLES ===")
    for i, table in enumerate(tables, 1):
        print(f"{i}. {table}")
    
    return tables

def show_table_structure(table_name):
    """Display the structure of a specific table"""
    inspector = inspect(engine)
    columns = inspector.get_columns(table_name)
    
    print(f"\n=== TABLE STRUCTURE: {table_name} ===")
    table_data = []
    for col in columns:
        table_data.append([
            col['name'], 
            str(col['type']), 
            'PRIMARY KEY' if col.get('primary_key') else '',
            'NOT NULL' if not col.get('nullable') else 'NULL'
        ])
    
    print(tabulate(table_data, headers=['Column', 'Type', 'Key', 'Nullable']))

def show_table_data(table_name, limit=5):
    """Display sample data from a specific table"""
    with engine.connect() as connection:
        result = connection.execute(text(f"SELECT * FROM {table_name} LIMIT {limit}"))
        rows = result.fetchall()
        
        if rows:
            print(f"\n=== SAMPLE DATA: {table_name} (First {limit} rows) ===")
            headers = result.keys()
            table_data = [list(row) for row in rows]
            print(tabulate(table_data, headers=headers))
        else:
            print(f"\nNo data found in table: {table_name}")

def show_relationships():
    """Display foreign key relationships between tables"""
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    
    print("\n=== TABLE RELATIONSHIPS ===")
    for table in tables:
        fks = inspector.get_foreign_keys(table)
        if fks:
            print(f"\nTable: {table}")
            for fk in fks:
                print(f"  → References {fk['referred_table']} ({', '.join(fk['referred_columns'])}) via {', '.join(fk['constrained_columns'])}")

def main():
    """Main function to run the database viewer"""
    print("=== CAR SERVICE MANAGEMENT SYSTEM DATABASE VIEWER ===")
    
    try:
        # Show all tables
        tables = show_tables()
        
        while True:
            print("\nOptions:")
            print("1. View table structure")
            print("2. View sample data")
            print("3. View relationships")
            print("4. Exit")
            
            choice = input("\nEnter your choice (1-4): ")
            
            if choice == '1':
                table_idx = int(input(f"Enter table number (1-{len(tables)}): ")) - 1
                if 0 <= table_idx < len(tables):
                    show_table_structure(tables[table_idx])
                else:
                    print("Invalid table number")
            
            elif choice == '2':
                table_idx = int(input(f"Enter table number (1-{len(tables)}): ")) - 1
                if 0 <= table_idx < len(tables):
                    limit = int(input("Enter number of rows to display: ") or "5")
                    show_table_data(tables[table_idx], limit)
                else:
                    print("Invalid table number")
            
            elif choice == '3':
                show_relationships()
            
            elif choice == '4':
                print("Exiting database viewer")
                break
            
            else:
                print("Invalid choice, please try again")
    
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
