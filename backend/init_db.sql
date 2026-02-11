CREATE DATABASE IF NOT EXISTS hrms_lite CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE hrms_lite;

CREATE TABLE IF NOT EXISTS employees (
  employee_id VARCHAR(50) PRIMARY KEY,
  full_name   VARCHAR(120) NOT NULL,
  email       VARCHAR(255) NOT NULL UNIQUE,
  department  VARCHAR(80)  NOT NULL,
  created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS attendance (
  id          BIGINT AUTO_INCREMENT PRIMARY KEY,
  employee_id VARCHAR(50) NOT NULL,
  att_date    DATE NOT NULL,
  status      ENUM('Present', 'Absent') NOT NULL,
  created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  UNIQUE KEY uniq_employee_date (employee_id, att_date),
  CONSTRAINT fk_att_employee FOREIGN KEY (employee_id)
    REFERENCES employees(employee_id)
    ON DELETE CASCADE
);
