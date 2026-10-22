"""
Script to check the database schema for the spare_part table.
"""

from app import app, db
from sqlalchemy import text

def check_schema():
    """Check the schema of the spare_part table"""
    try:
        with app.app_context():
            with db.engine.connect() as connection:
                # Check spare_part table schema
                result = connection.execute(text("DESCRIBE spare_part"))
                print("spare_part table schema:")
                for row in result:
                    print(row)
                
                # Check supplier table schema
                result = connection.execute(text("DESCRIBE supplier"))
                print("\nsupplier table schema:")
                for row in result:
                    print(row)
    except Exception as e:
        print(f"Error checking schema: {e}")

if __name__ == "__main__":
    check_schema()
