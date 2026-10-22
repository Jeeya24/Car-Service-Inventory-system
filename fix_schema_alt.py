"""
Alternative script to fix the database schema for the spare_part table.
"""

from app import app, db
from sqlalchemy import text
from models import SparePart, Supplier

def fix_schema():
    """Fix the schema of the spare_part table"""
    try:
        with app.app_context():
            with db.engine.connect() as connection:
                # Check if the supplier_id column exists in the spare_part table
                result = connection.execute(text("SHOW COLUMNS FROM spare_part LIKE 'supplier_id'"))
                if not result.fetchone():
                    # Add the supplier_id column if it doesn't exist
                    connection.execute(text("""
                    ALTER TABLE spare_part 
                    ADD COLUMN supplier_id INT NULL,
                    ADD CONSTRAINT fk_spare_part_supplier
                    FOREIGN KEY (supplier_id) REFERENCES supplier(id)
                    ON DELETE SET NULL
                    """))
                    print("Added supplier_id column to spare_part table")
                else:
                    print("supplier_id column already exists in spare_part table")
                
                # Commit the transaction
                connection.commit()
                print("Schema fix completed successfully!")
    except Exception as e:
        print(f"Error fixing schema: {e}")

if __name__ == "__main__":
    fix_schema()
