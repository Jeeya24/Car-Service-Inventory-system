-- Fix database schema issues
USE car_inventory;

-- Add assigned_employee_id column if it doesn't exist
SET @sql = (SELECT IF(
    (SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS 
     WHERE TABLE_NAME = 'car' 
     AND COLUMN_NAME = 'assigned_employee_id' 
     AND TABLE_SCHEMA = DATABASE()) = 0,
    'ALTER TABLE car ADD COLUMN assigned_employee_id INT NULL',
    'SELECT "Column already exists"'
));
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- Add foreign key constraint if it doesn't exist
SET @sql = (SELECT IF(
    (SELECT COUNT(*) FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE 
     WHERE TABLE_NAME = 'car' 
     AND CONSTRAINT_NAME = 'fk_car_assigned_employee'
     AND TABLE_SCHEMA = DATABASE()) = 0,
    'ALTER TABLE car ADD CONSTRAINT fk_car_assigned_employee FOREIGN KEY (assigned_employee_id) REFERENCES employee(id)',
    'SELECT "Foreign key already exists"'
));
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;