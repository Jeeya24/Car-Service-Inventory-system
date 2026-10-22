-- Add time tracking fields to car table
USE car_inventory;

-- Add planned_start_time column if it doesn't exist
SET @sql = (SELECT IF(
    (SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS 
     WHERE TABLE_NAME = 'car' 
     AND COLUMN_NAME = 'planned_start_time' 
     AND TABLE_SCHEMA = DATABASE()) = 0,
    'ALTER TABLE car ADD COLUMN planned_start_time DATETIME NULL',
    'SELECT "planned_start_time column already exists"'
));
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- Add planned_end_time column if it doesn't exist
SET @sql = (SELECT IF(
    (SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS 
     WHERE TABLE_NAME = 'car' 
     AND COLUMN_NAME = 'planned_end_time' 
     AND TABLE_SCHEMA = DATABASE()) = 0,
    'ALTER TABLE car ADD COLUMN planned_end_time DATETIME NULL',
    'SELECT "planned_end_time column already exists"'
));
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- Add actual_start_time column if it doesn't exist
SET @sql = (SELECT IF(
    (SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS 
     WHERE TABLE_NAME = 'car' 
     AND COLUMN_NAME = 'actual_start_time' 
     AND TABLE_SCHEMA = DATABASE()) = 0,
    'ALTER TABLE car ADD COLUMN actual_start_time DATETIME NULL',
    'SELECT "actual_start_time column already exists"'
));
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- Add actual_end_time column if it doesn't exist
SET @sql = (SELECT IF(
    (SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS 
     WHERE TABLE_NAME = 'car' 
     AND COLUMN_NAME = 'actual_end_time' 
     AND TABLE_SCHEMA = DATABASE()) = 0,
    'ALTER TABLE car ADD COLUMN actual_end_time DATETIME NULL',
    'SELECT "actual_end_time column already exists"'
));
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;