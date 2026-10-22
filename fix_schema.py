"""
Script to fix the database schema for the spare_part table.
"""

from app import app, db
from sqlalchemy import text
from models import SparePart, Supplier

def fix_schema():
    """Fix the schema of the spare_part table"""
    try:
        with app.app_context():
            # Create a new table with the correct schema
            with db.engine.connect() as connection:
                # Backup existing data
                connection.execute(text("CREATE TABLE IF NOT EXISTS spare_part_backup AS SELECT * FROM spare_part"))
                print("Created backup of spare_part table")
                
                # Drop the existing table
                connection.execute(text("DROP TABLE IF EXISTS spare_part"))
                print("Dropped spare_part table")
                
                # Create the table with the correct schema
                connection.execute(text("""
                CREATE TABLE spare_part (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    part_id VARCHAR(8) NOT NULL UNIQUE,
                    part_name VARCHAR(100) NOT NULL,
                    brand VARCHAR(50) NOT NULL,
                    price FLOAT NOT NULL,
                    stock_quantity INT NOT NULL DEFAULT 0,
                    supplier_id INT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    FOREIGN KEY (supplier_id) REFERENCES supplier(id) ON DELETE SET NULL
                )
                """))
                print("Created spare_part table with correct schema")
                
                # Restore data from backup
                connection.execute(text("""
                INSERT INTO spare_part (id, part_id, part_name, brand, price, stock_quantity, supplier_id, created_at, updated_at)
                SELECT id, part_id, part_name, brand, price, stock_quantity, supplier_id, created_at, updated_at
                FROM spare_part_backup
                """))
                print("Restored data from backup")
                
                # Commit the transaction
                connection.commit()
                print("Schema fix completed successfully!")
    except Exception as e:
        print(f"Error fixing schema: {e}")

if __name__ == "__main__":
    fix_schema()
