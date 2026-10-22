#!/usr/bin/env python3
"""
Database migration script to add actual_start_time and actual_end_time columns to ServiceRecord table
"""

from app import app
from models import db
from sqlalchemy import text

def migrate_database():
    with app.app_context():
        try:
            # Check if columns already exist
            result = db.session.execute(text("DESCRIBE service_record"))
            columns = [row[0] for row in result.fetchall()]
            
            # Add actual_start_time column if it doesn't exist
            if 'actual_start_time' not in columns:
                db.session.execute(text("ALTER TABLE service_record ADD COLUMN actual_start_time DATETIME NULL"))
                print("Added actual_start_time column to service_record table")
            else:
                print("actual_start_time column already exists")
            
            # Add actual_end_time column if it doesn't exist
            if 'actual_end_time' not in columns:
                db.session.execute(text("ALTER TABLE service_record ADD COLUMN actual_end_time DATETIME NULL"))
                print("Added actual_end_time column to service_record table")
            else:
                print("actual_end_time column already exists")
            
            db.session.commit()
            print("Database migration completed successfully!")
            
        except Exception as e:
            db.session.rollback()
            print(f"Migration failed: {str(e)}")

if __name__ == '__main__':
    migrate_database()