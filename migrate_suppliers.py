"""
Database migration script to add suppliers table and update spare_parts table.
Run this script to create the suppliers table and add the supplier_id column to spare_parts.
"""

from app import app, db
from sqlalchemy import text
from models import Supplier, SparePart
import re

def create_suppliers_table():
    """Create the suppliers table if it doesn't exist"""
    try:
        # Use SQLAlchemy's connection to execute raw SQL
        with db.engine.connect() as connection:
            # Check if suppliers table exists
            result = connection.execute(text("SHOW TABLES LIKE 'supplier';"))
            if not result.fetchone():
                # Create suppliers table
                connection.execute(text("""
                CREATE TABLE supplier (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    supplier_id VARCHAR(8) NOT NULL UNIQUE,
                    supplier_name VARCHAR(100) NOT NULL,
                    email VARCHAR(120) NOT NULL UNIQUE,
                    phone VARCHAR(15) NOT NULL,
                    delivery_lead_time INT NOT NULL DEFAULT 1,
                    preferred_supplier BOOLEAN DEFAULT FALSE,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                );
                """))
                print("Created suppliers table")
            else:
                print("Suppliers table already exists")

            # Commit the transaction
            connection.commit()
    except Exception as e:
        print(f"Error creating suppliers table: {e}")

def update_spare_parts_table():
    """Add supplier_id column to spare_parts table if it doesn't exist"""
    try:
        # Use SQLAlchemy's connection to execute raw SQL
        with db.engine.connect() as connection:
            # Check if supplier_id column exists in spare_part table
            result = connection.execute(text("SHOW COLUMNS FROM spare_part LIKE 'supplier_id';"))
            if not result.fetchone():
                # Add supplier_id column to spare_part table
                connection.execute(text("""
                ALTER TABLE spare_part 
                ADD COLUMN supplier_id INT NULL,
                ADD CONSTRAINT fk_spare_part_supplier
                FOREIGN KEY (supplier_id) REFERENCES supplier(id)
                ON DELETE SET NULL;
                """))
                print("Added supplier_id column to spare_part table")
            else:
                print("supplier_id column already exists in spare_part table")

            # Commit the transaction
            connection.commit()
    except Exception as e:
        print(f"Error updating spare_parts table: {e}")

def create_default_supplier():
    """Create a default supplier if none exists"""
    try:
        with app.app_context():
            # Check if any supplier exists
            supplier_count = Supplier.query.count()
            if supplier_count == 0:
                # Create default supplier
                default_supplier = Supplier(
                    supplier_name="Default Supplier",
                    email="default@supplier.com",
                    phone="1234567890",
                    delivery_lead_time=3,
                    preferred_supplier=True
                )
                db.session.add(default_supplier)
                db.session.commit()
                print(f"Created default supplier with ID: {default_supplier.supplier_id}")
            else:
                print("Suppliers already exist, skipping default supplier creation")
    except Exception as e:
        print(f"Error creating default supplier: {e}")

if __name__ == "__main__":
    with app.app_context():
        create_suppliers_table()
        update_spare_parts_table()
        create_default_supplier()
        print("Database migration completed successfully!")
