from app import app, db
from models import Employee

# Create a test context
with app.app_context():
    try:
        # Create a test employee
        employee = Employee(
            first_name="Test",
            last_name="User",
            role="manager",
            phone="1234567890",
            email="test@example.com",
            salary=0.0,
            username="testuser"
        )
        
        # Set password
        try:
            employee.set_password("Test@123")
            print("Password set successfully")
        except Exception as e:
            print(f"Error setting password: {str(e)}")
            
        # Add to database
        try:
            db.session.add(employee)
            db.session.commit()
            print(f"Employee created successfully with ID: {employee.employee_id}")
        except Exception as e:
            db.session.rollback()
            print(f"Error adding employee to database: {str(e)}")
            
    except Exception as e:
        print(f"Error creating employee: {str(e)}")
