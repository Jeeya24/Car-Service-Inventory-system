"""
Script to fix the SparePart model to match the database schema.
"""

from app import app, db
from sqlalchemy import text
from models import SparePart, Supplier

def fix_model():
    """Fix the SparePart model to match the database schema"""
    try:
        with app.app_context():
            # Create a test part to verify the model works
            supplier = Supplier.query.first()
            if not supplier:
                supplier = Supplier(
                    supplier_name="Test Supplier",
                    email="test@supplier.com",
                    phone="1234567890",
                    delivery_lead_time=3,
                    preferred_supplier=True
                )
                db.session.add(supplier)
                db.session.commit()
                print(f"Created test supplier with ID: {supplier.supplier_id}")
            
            # Create a test part
            part = SparePart(
                part_name="Test Part",
                brand="Test Brand",
                price=10.0,
                stock_quantity=10,
                supplier_id=supplier.id
            )
            db.session.add(part)
            db.session.commit()
            print(f"Created test part with ID: {part.part_id}")
            
            # Verify the part was created with the correct supplier
            part = SparePart.query.filter_by(part_name="Test Part").first()
            if part and part.supplier_id == supplier.id:
                print(f"Test part has correct supplier_id: {part.supplier_id}")
            else:
                print(f"Test part has incorrect supplier_id: {part.supplier_id if part else 'None'}")
            
            print("Model verification completed successfully!")
    except Exception as e:
        print(f"Error verifying model: {e}")

if __name__ == "__main__":
    fix_model()
