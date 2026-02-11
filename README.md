# Project Overview

HRMS Lite is a lightweight Human Resource Management System designed to manage employee records and track daily attendance.

The application simulates a basic internal HR tool for administrative use. It allows:

1. Adding and deleting employees

2. Viewing employee records

3. Marking daily attendance

4. Viewing attendance history per employee

5. Dashboard summary of total employees and attendance records

The focus of the project is clean architecture, proper API design, database integration, validation handling, and a production-ready UI.

# Tech Stack Used:-
1. Frontend

   Streamlit

   Pandas

   Requests

2. Backend

   Python

   Flask (REST API)

   SQLAlchemy (ORM)

   Gunicorn (Production server)

3. Database

   MySQL

4. Version Control

   Git & GitHub


#  Steps to Run the Project Locally
   1. Clone the Repository- git clone https://github.com/your-username/hrms-lite.git
      cd hrms-lite

   2. Backend Setup

    Navigate to backend folder: cd backend

   3. Create virtual environment: python -m venv .venv


   4. Activate environment:

       Windows:

      .venv\Scripts\activate


   5. Install dependencies:

      pip install -r requirements.txt

   6. Setup MySQL Database

    Login to MySQL and run:

   CREATE DATABASE hrms_lite;


Then configure environment variables in .env file:

DB_HOST=localhost
DB_PORT=3306
DB_NAME=hrms_lite
DB_USER=root
DB_PASSWORD=your_password


 7.Run backend:

  python app.py


  Backend runs on: http://127.0.0.1:5000

8. Frontend Setup

Open new terminal.

Navigate to frontend:

cd frontend

Install dependencies:

pip install -r requirements.txt


Run Streamlit app:

streamlit run app.py


Frontend runs on:

http://localhost:8501

#Functional Features Implemented

Add Employee (Unique Employee ID)

Delete Employee

View Employees

Mark Attendance (Present / Absent)

View Attendance History

Dashboard Summary

Filter Attendance by Date (Bonus)

Total Present Days per Employee (Bonus)

Server-side validations

Proper HTTP status codes

Error handling with meaningful messages

Loading, empty, and error states in UI

#Assumptions

Single admin user (no authentication required)

Employee ID must be unique

Attendance is tracked per employee per date

No payroll or leave management included (out of scope)

# Deployment Status

The application works fully in the local environment.

Deployment was attempted on cloud platforms. However, deployment issues occurred due to environment configuration and platform-specific build/runtime constraints.

The project is fully functional locally and deployment troubleshooting is currently in progress.

# Repository

GitHub Repository:
https://github.com/smritisinha0801/hrms-lite

