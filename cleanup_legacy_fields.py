#!/usr/bin/env python3
"""
Migration script to clean up legacy assigned_staff_id field
and consolidate all data to use assigned_employee_id
"""

from app import app, db
from sqlalchemy import text

def cleanup_legacy_fields():
    """Clean up legacy assigned_staff_id field"""
    try:
        with app.app_context():
            with db.engine.connect() as connection:
                # Check if assigned_staff_id column exists
                result = connection.execute(text("SHOW COLUMNS FROM car LIKE 'assigned_staff_id'"))
                if not result.fetchone():
                    print("assigned_staff_id column does not exist - nothing to clean up")
                    return
                
                # Migrate data from assigned_staff_id to assigned_employee_id where needed
                print("Migrating data from assigned_staff_id to assigned_employee_id...")
                connection.execute(text("""
                    UPDATE car 
                    SET assigned_employee_id = assigned_staff_id 
                    WHERE assigned_staff_id IS NOT NULL 
                    AND assigned_employee_id IS NULL
                """))
                
                # Check how many records were affected
                result = connection.execute(text("""
                    SELECT COUNT(*) as count 
                    FROM car 
                    WHERE assigned_staff_id IS NOT NULL
                """))
                count = result.fetchone()[0]
                print(f"Found {count} records with assigned_staff_id data")
                
                # Drop the legacy column
                print("Dropping assigned_staff_id column...")
                connection.execute(text("ALTER TABLE car DROP COLUMN assigned_staff_id"))
                
                connection.commit()
                print("Successfully cleaned up legacy assigned_staff_id field!")
                
    except Exception as e:
        print(f"Error cleaning up legacy fields: {e}")

if __name__ == "__main__":
    cleanup_legacy_fields()