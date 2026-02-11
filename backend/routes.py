from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, func
from db import get_db_session
from models import Employee, Attendance
from validators import is_valid_email, parse_date, require_fields

api = Blueprint("api", __name__)

def json_error(message: str, status_code: int = 400, details=None):
    body = {"error": message}
    if details is not None:
        body["details"] = details
    return jsonify(body), status_code

@api.get("/health")
def health():
    return jsonify({"status": "ok"}), 200

# ----------------- Employees -----------------

@api.get("/employees")
def list_employees():
    db = get_db_session()
    try:
        q = select(Employee).order_by(Employee.created_at.desc())
        employees = db.execute(q).scalars().all()
        return jsonify([
            {
                "employee_id": e.employee_id,
                "full_name": e.full_name,
                "email": e.email,
                "department": e.department,
                "created_at": e.created_at.isoformat() if e.created_at else None
            } for e in employees
        ]), 200
    finally:
        db.close()

@api.post("/employees")
def create_employee():
    payload = request.get_json(silent=True) or {}
    missing = require_fields(payload, ["employee_id", "full_name", "email", "department"])
    if missing:
        return json_error("Missing required fields.", 400, {"missing": missing})

    employee_id = str(payload["employee_id"]).strip()
    full_name = str(payload["full_name"]).strip()
    email = str(payload["email"]).strip().lower()
    department = str(payload["department"]).strip()

    if not is_valid_email(email):
        return json_error("Invalid email format.", 400)

    db = get_db_session()
    try:
        emp = Employee(
            employee_id=employee_id,
            full_name=full_name,
            email=email,
            department=department
        )
        db.add(emp)
        db.commit()
        return jsonify({"message": "Employee created.", "employee_id": employee_id}), 201
    except IntegrityError as e:
        db.rollback()
        # Unique conflicts: employee_id or email
        return json_error(
            "Duplicate employee_id or email. Use unique values.",
            409
        )
    finally:
        db.close()

@api.delete("/employees/<employee_id>")
def delete_employee(employee_id):
    db = get_db_session()
    try:
        emp = db.get(Employee, employee_id)
        if not emp:
            return json_error("Employee not found.", 404)

        db.delete(emp)
        db.commit()
        return jsonify({"message": "Employee deleted.", "employee_id": employee_id}), 200
    finally:
        db.close()

# ----------------- Attendance -----------------

@api.get("/employees/<employee_id>/attendance")
def get_attendance(employee_id):
    date_filter = request.args.get("date")  # optional YYYY-MM-DD
    db = get_db_session()
    try:
        emp = db.get(Employee, employee_id)
        if not emp:
            return json_error("Employee not found.", 404)

        q = select(Attendance).where(Attendance.employee_id == employee_id)
        if date_filter:
            d = parse_date(date_filter)
            if not d:
                return json_error("Invalid date format. Use YYYY-MM-DD.", 400)
            q = q.where(Attendance.att_date == d)

        q = q.order_by(Attendance.att_date.desc())
        rows = db.execute(q).scalars().all()

        return jsonify([
            {
                "id": r.id,
                "employee_id": r.employee_id,
                "date": r.att_date.isoformat(),
                "status": r.status,
                "created_at": r.created_at.isoformat() if r.created_at else None
            } for r in rows
        ]), 200
    finally:
        db.close()

@api.post("/employees/<employee_id>/attendance")
def mark_attendance(employee_id):
    payload = request.get_json(silent=True) or {}
    missing = require_fields(payload, ["date", "status"])
    if missing:
        return json_error("Missing required fields.", 400, {"missing": missing})

    d = parse_date(str(payload["date"]).strip())
    if not d:
        return json_error("Invalid date format. Use YYYY-MM-DD.", 400)

    status = str(payload["status"]).strip()
    if status not in ("Present", "Absent"):
        return json_error("Invalid status. Use Present or Absent.", 400)

    db = get_db_session()
    try:
        emp = db.get(Employee, employee_id)
        if not emp:
            return json_error("Employee not found.", 404)

        rec = Attendance(employee_id=employee_id, att_date=d, status=status)
        db.add(rec)
        db.commit()
        return jsonify({"message": "Attendance marked.", "employee_id": employee_id, "date": d.isoformat()}), 201
    except IntegrityError:
        db.rollback()
        return json_error("Attendance for this employee and date already exists.", 409)
    finally:
        db.close()

# ----------------- Dashboard (Bonus) -----------------

@api.get("/dashboard/summary")
def dashboard_summary():
    db = get_db_session()
    try:
        total_employees = db.execute(select(func.count()).select_from(Employee)).scalar_one()
        total_attendance = db.execute(select(func.count()).select_from(Attendance)).scalar_one()

        # total present days per employee
        q = (
            select(Attendance.employee_id, func.count().label("present_days"))
            .where(Attendance.status == "Present")
            .group_by(Attendance.employee_id)
        )
        present_counts = db.execute(q).all()
        present_map = {eid: int(cnt) for eid, cnt in present_counts}

        return jsonify({
            "total_employees": int(total_employees),
            "total_attendance_records": int(total_attendance),
            "present_days_per_employee": present_map
        }), 200
    finally:
        db.close()
