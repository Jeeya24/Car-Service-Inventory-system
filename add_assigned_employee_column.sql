-- Migration script to add assigned_employee_id column to car table

-- Check if column exists first (optional check)
-- SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS 
-- WHERE TABLE_NAME = 'car' AND COLUMN_NAME = 'assigned_employee_id';

-- Add the assigned_employee_id column
ALTER TABLE car 
ADD COLUMN assigned_employee_id INT NULL;

-- Add foreign key constraint
ALTER TABLE car 
ADD CONSTRAINT fk_car_assigned_employee 
FOREIGN KEY (assigned_employee_id) REFERENCES employee(id);

-- Verify the column was added
DESCRIBE car;