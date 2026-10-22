from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone
import re

db = SQLAlchemy()

def utc_now():
    """Return timezone-aware UTC now"""
    return datetime.now(timezone.utc)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255))
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    role = db.Column(db.String(20), nullable=False, default='staff')
    password_reset_required = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=utc_now)

    @staticmethod
    def validate_password(password):
        """Validate password strength"""
        if len(password) < 8:
            return False
        if not any(c.isupper() for c in password):
            return False
        if not any(c.islower() for c in password):
            return False
        if not any(c.isdigit() for c in password):
            return False
        if not any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in password):
            return False
        return True

    def set_password(self, password):
        """Set password hash"""
        if not self.validate_password(password):
            raise ValueError("Password does not meet requirements")
        self.password_hash = generate_password_hash(password)
        self.password_reset_required = False

    def check_password(self, password):
        """Check password hash"""
        return check_password_hash(self.password_hash, password)

    @property
    def is_admin(self):
        """Check if user is admin"""
        return self.role == 'admin'

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.String(8), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    address = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=utc_now)
    updated_at = db.Column(db.DateTime, default=utc_now, onupdate=utc_now)

    @staticmethod
    def generate_customer_id():
        # Get the last customer ID from the database
        last_customer = Customer.query.order_by(Customer.id.desc()).first()
        if last_customer:
            # Extract the number from the last customer_id and increment
            last_num = int(last_customer.customer_id[4:])
            new_num = last_num + 1
        else:
            new_num = 1
        # Format the new customer_id
        return f'CUST{new_num:04d}'

    @staticmethod
    def validate_phone(phone):
        # Remove any non-digit characters
        phone = re.sub(r'\D', '', phone)
        # Check if the length is between 10 and 15 digits
        return 10 <= len(phone) <= 15

    @staticmethod
    def validate_email(email):
        # Basic email validation regex
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))

    def __init__(self, **kwargs):
        super(Customer, self).__init__(**kwargs)
        if not self.customer_id:
            self.customer_id = self.generate_customer_id()

class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.String(8), unique=True, nullable=False)
    customer_id = db.Column(db.String(8), db.ForeignKey('customer.customer_id'), nullable=False)
    brand = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    registration_number = db.Column(db.String(20), unique=True, nullable=False)
    vin = db.Column(db.String(17), unique=True, nullable=False)
    assigned_employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=True)
    planned_start_time = db.Column(db.DateTime, nullable=True)
    planned_end_time = db.Column(db.DateTime, nullable=True)
    actual_start_time = db.Column(db.DateTime, nullable=True)
    actual_end_time = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=utc_now)
    updated_at = db.Column(db.DateTime, default=utc_now, onupdate=utc_now)

    @property
    def make(self):
        """Alias for brand to maintain compatibility"""
        return self.brand

    # Relationships
    customer = db.relationship('Customer', backref=db.backref('cars', lazy=True))
    assigned_employee = db.relationship('Employee', backref=db.backref('assigned_vehicles', lazy=True))
    service_records = db.relationship('ServiceRecord', backref='car', lazy=True)
    
    @property
    def service_duration_minutes(self):
        """Calculate service duration in minutes"""
        if self.actual_start_time and self.actual_end_time:
            delta = self.actual_end_time - self.actual_start_time
            return int(delta.total_seconds() / 60)
        return None

    @staticmethod
    def generate_vehicle_id():
        last_vehicle = Car.query.order_by(Car.id.desc()).first()
        if last_vehicle:
            last_num = int(last_vehicle.vehicle_id[3:])
            new_num = last_num + 1
        else:
            new_num = 1
        return f'VEH{new_num:04d}'

    @staticmethod
    def validate_vin(vin):
        # Basic VIN validation (17 characters, alphanumeric)
        return bool(re.match(r'^[A-HJ-NPR-Z0-9]{17}$', vin))

    @staticmethod
    def validate_registration(registration):
        # Basic registration number validation (alphanumeric, 5-10 characters)
        return bool(re.match(r'^[A-Z0-9]{5,10}$', registration))

    def __init__(self, **kwargs):
        super(Car, self).__init__(**kwargs)
        if not self.vehicle_id:
            self.vehicle_id = self.generate_vehicle_id()

class ServiceRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.String(20), unique=True, nullable=False)  # Increased from 8 to 20 to accommodate UUID format
    vehicle_id = db.Column(db.Integer, db.ForeignKey('car.id'), nullable=False)
    service_date = db.Column(db.DateTime, nullable=False, default=utc_now)
    service_status = db.Column(db.String(20), nullable=False, default='Pending')  # Pending, In Progress, Completed
    actual_start_date = db.Column(db.Date, nullable=True)
    actual_start_time = db.Column(db.Time, nullable=True)
    actual_end_date = db.Column(db.Date, nullable=True)
    actual_end_time = db.Column(db.Time, nullable=True)
    serviced_by_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=True)
    total_cost = db.Column(db.Float, nullable=False, default=0.0)
    created_at = db.Column(db.DateTime, default=utc_now)
    updated_at = db.Column(db.DateTime, default=utc_now, onupdate=utc_now)
    
    @property
    def actual_start_datetime(self):
        """Combine actual_start_date and actual_start_time into datetime"""
        if self.actual_start_date and self.actual_start_time:
            return datetime.combine(self.actual_start_date, self.actual_start_time)
        return None
    
    @property
    def actual_end_datetime(self):
        """Combine actual_end_date and actual_end_time into datetime"""
        if self.actual_end_date and self.actual_end_time:
            return datetime.combine(self.actual_end_date, self.actual_end_time)
        return None

    # Relationships
    vehicle = db.relationship('Car', overlaps="car,service_records")
    services = db.relationship('Service', backref='service_record', cascade='all, delete-orphan')
    parts_used = db.relationship('ServicePart', backref='service_record', cascade='all, delete-orphan')
    bill = db.relationship('Bill', backref='service_record', uselist=False, overlaps="bill,service_record")

    @staticmethod
    def generate_service_id():
        """
        Generate a unique service ID using UUID to guarantee uniqueness.
        """
        import uuid

        # Generate a UUID and use part of it to create a unique ID
        # This guarantees uniqueness without needing to query the database
        unique_id = str(uuid.uuid4())

        # Use the first 8 characters of the UUID to create a unique ID
        # Format: SVC-XXXXXXXX where X is a hex digit
        return f'SVC-{unique_id[:8].upper()}'

    def calculate_total_cost(self):
        """Calculate total cost from services and parts"""
        service_cost = sum(service.service_cost for service in self.services)
        parts_cost = sum(part.total_cost for part in self.parts_used)
        self.total_cost = service_cost + parts_cost
        return self.total_cost

    def __init__(self, **kwargs):
        super(ServiceRecord, self).__init__(**kwargs)
        if not self.service_id:
            self.service_id = self.generate_service_id()

class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    service_detail_id = db.Column(db.String(20), unique=True, nullable=False)  # Increased from 8 to 20 to accommodate UUID format
    service_id = db.Column(db.Integer, db.ForeignKey('service_record.id'), nullable=False)
    service_type = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    service_cost = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=utc_now)

    @staticmethod
    def generate_service_detail_id():
        """
        Generate a unique service detail ID using UUID to guarantee uniqueness.
        """
        import uuid

        # Generate a UUID and use part of it to create a unique ID
        # This guarantees uniqueness without needing to query the database
        unique_id = str(uuid.uuid4())

        # Use the first 8 characters of the UUID to create a unique ID
        # Format: SDT-XXXXXXXX where X is a hex digit
        return f'SDT-{unique_id[:8].upper()}'

    def __init__(self, **kwargs):
        super(Service, self).__init__(**kwargs)
        if not self.service_detail_id:
            self.service_detail_id = self.generate_service_detail_id()

class ServicePart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    service_part_id = db.Column(db.String(20), unique=True, nullable=False)  # Increased from 8 to 20 to accommodate UUID format
    service_id = db.Column(db.Integer, db.ForeignKey('service_record.id'), nullable=False)
    part_id = db.Column(db.Integer, db.ForeignKey('spare_part.id'), nullable=False)
    quantity_used = db.Column(db.Integer, nullable=False)
    price_at_time = db.Column(db.Float, nullable=False)
    total_cost = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=utc_now)

    # Relationships
    part = db.relationship('SparePart', backref='service_uses')

    @staticmethod
    def generate_service_part_id():
        """
        Generate a unique service part ID using UUID to guarantee uniqueness.
        """
        import uuid

        # Generate a UUID and use part of it to create a unique ID
        # This guarantees uniqueness without needing to query the database
        unique_id = str(uuid.uuid4())

        # Use the first 8 characters of the UUID to create a unique ID
        # Format: SPT-XXXXXXXX where X is a hex digit
        return f'SPT-{unique_id[:8].upper()}'

    def calculate_total_cost(self):
        """Calculate total cost based on quantity and price"""
        self.total_cost = self.quantity_used * self.price_at_time
        return self.total_cost

    def __init__(self, **kwargs):
        super(ServicePart, self).__init__(**kwargs)
        if not self.service_part_id:
            self.service_part_id = self.generate_service_part_id()
        if not self.price_at_time:
            self.price_at_time = self.part.price
        self.calculate_total_cost()

class Bill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bill_id = db.Column(db.String(8), unique=True, nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('service_record.id'), nullable=False)
    customer_id = db.Column(db.String(8), db.ForeignKey('customer.customer_id'), nullable=False)
    billing_date = db.Column(db.DateTime, nullable=False, default=utc_now)
    total_amount = db.Column(db.Float, nullable=False)
    payment_status = db.Column(db.String(20), nullable=False, default='Pending')  # Pending, Paid
    created_at = db.Column(db.DateTime, default=utc_now)
    updated_at = db.Column(db.DateTime, default=utc_now, onupdate=utc_now)

    # Relationships
    customer = db.relationship('Customer', backref='bills')
    service = db.relationship('ServiceRecord', backref='bill_record', overlaps="bill,service_record")

    @staticmethod
    def generate_bill_id():
        last_bill = Bill.query.order_by(Bill.id.desc()).first()
        if last_bill:
            last_num = int(last_bill.bill_id[3:])
            new_num = last_num + 1
        else:
            new_num = 1
        return f'BIL{new_num:04d}'

    def __init__(self, **kwargs):
        super(Bill, self).__init__(**kwargs)
        if not self.bill_id:
            self.bill_id = self.generate_bill_id()

class Employee(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.String(8), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # admin, manager, staff
    phone = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    salary = db.Column(db.Float, nullable=False)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=utc_now)
    updated_at = db.Column(db.DateTime, default=utc_now, onupdate=utc_now)

    @property
    def name(self):
        """Return full name for compatibility with User model"""
        return f"{self.first_name} {self.last_name}"

    @property
    def is_admin(self):
        """Check if user is admin"""
        return self.role == 'admin'

    @staticmethod
    def generate_employee_id():
        last_employee = Employee.query.order_by(Employee.id.desc()).first()
        if last_employee:
            last_num = int(last_employee.employee_id[3:])
            new_num = last_num + 1
        else:
            new_num = 1
        return f'EMP{new_num:04d}'

    def set_password(self, password):
        # Check password requirements
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not re.search(r'[A-Z]', password):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r'[a-z]', password):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r'\d', password):
            raise ValueError("Password must contain at least one number")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValueError("Password must contain at least one special character")

        # Use Werkzeug's generate_password_hash with sha256 method instead of default
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')

    def check_password(self, password):
        """Verify a password against the stored hash using Werkzeug's check_password_hash"""
        if not self.password_hash:
            return False

        try:
            # Use the standard check_password_hash function from Werkzeug
            return check_password_hash(self.password_hash, password)
        except Exception as e:
            # Log the error but don't expose details to the user
            print(f"Error checking password: {str(e)}")
            return False

    @staticmethod
    def validate_password(password):
        """
        Validate password strength:
        - At least 8 characters
        - At least one uppercase letter
        - At least one lowercase letter
        - At least one number
        - At least one special character
        """
        if len(password) < 8:
            return False
        if not re.search(r'[A-Z]', password):
            return False
        if not re.search(r'[a-z]', password):
            return False
        if not re.search(r'\d', password):
            return False
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            return False
        return True

    @staticmethod
    def validate_phone(phone):
        phone = re.sub(r'\D', '', phone)
        return 10 <= len(phone) <= 15

    @staticmethod
    def validate_email(email):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))

    def __init__(self, **kwargs):
        super(Employee, self).__init__(**kwargs)
        if not self.employee_id:
            self.employee_id = self.generate_employee_id()

class Supplier(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    supplier_id = db.Column(db.String(8), unique=True, nullable=False)
    supplier_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    delivery_lead_time = db.Column(db.Integer, nullable=False, default=1)  # in days
    preferred_supplier = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=utc_now)
    updated_at = db.Column(db.DateTime, default=utc_now, onupdate=utc_now)

    # Relationships
    parts = db.relationship('SparePart', backref='supplier', lazy=True)

    @staticmethod
    def generate_supplier_id():
        """Generate a unique supplier ID in the format SUP####"""
        last_supplier = Supplier.query.order_by(Supplier.id.desc()).first()
        if last_supplier:
            last_num = int(last_supplier.supplier_id[3:])
            new_num = last_num + 1
        else:
            new_num = 1
        return f'SUP{new_num:04d}'

    @staticmethod
    def validate_phone(phone):
        """Validate phone number format"""
        # Remove any non-digit characters
        phone = re.sub(r'\D', '', phone)
        # Check if the length is between 10 and 15 digits
        return 10 <= len(phone) <= 15

    @staticmethod
    def validate_email(email):
        """Validate email format"""
        # Basic email validation regex
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))

    def __init__(self, **kwargs):
        super(Supplier, self).__init__(**kwargs)
        if not self.supplier_id:
            self.supplier_id = self.generate_supplier_id()

class SparePart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    part_id = db.Column(db.String(8), unique=True, nullable=False)
    part_name = db.Column(db.String(100), nullable=False)
    brand = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock_quantity = db.Column(db.Integer, nullable=False, default=0)
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=utc_now)
    updated_at = db.Column(db.DateTime, default=utc_now, onupdate=utc_now)

    @staticmethod
    def generate_part_id():
        last_part = SparePart.query.order_by(SparePart.id.desc()).first()
        if last_part:
            last_num = int(last_part.part_id[3:])
            new_num = last_num + 1
        else:
            new_num = 1
        return f'PRT{new_num:04d}'

    def update_stock(self, quantity):
        """Update stock quantity and ensure it doesn't go below 0"""
        new_quantity = self.stock_quantity + quantity
        if new_quantity < 0:
            raise ValueError("Stock quantity cannot be negative")
        self.stock_quantity = new_quantity

    def is_low_stock(self):
        """Check if stock is below warning threshold"""
        return self.stock_quantity < 5

    def __init__(self, **kwargs):
        super(SparePart, self).__init__(**kwargs)
        if not self.part_id:
            self.part_id = self.generate_part_id()