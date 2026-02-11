import os
import requests

API_BASE = os.getenv("API_BASE", "http://127.0.0.1:5000/api")
TIMEOUT = 15

def _handle(resp: requests.Response):
    try:
        data = resp.json()
    except Exception:
        data = {"error": "Server returned non-JSON response."}

    if resp.status_code >= 400:
        msg = data.get("error", "Request failed")
        details = data.get("details")
        if details:
            msg = f"{msg} | {details}"
        raise RuntimeError(msg)

    return data

def health():
    r = requests.get(f"{API_BASE}/health", timeout=TIMEOUT)
    return _handle(r)

def list_employees():
    r = requests.get(f"{API_BASE}/employees", timeout=TIMEOUT)
    return _handle(r)

def create_employee(employee_id, full_name, email, department):
    r = requests.post(
        f"{API_BASE}/employees",
        json={
            "employee_id": employee_id,
            "full_name": full_name,
            "email": email,
            "department": department
        },
        timeout=TIMEOUT
    )
    return _handle(r)

def delete_employee(employee_id):
    r = requests.delete(f"{API_BASE}/employees/{employee_id}", timeout=TIMEOUT)
    return _handle(r)

def mark_attendance(employee_id, date_str, status):
    r = requests.post(
        f"{API_BASE}/employees/{employee_id}/attendance",
        json={"date": date_str, "status": status},
        timeout=TIMEOUT
    )
    return _handle(r)

def get_attendance(employee_id, date_filter=None):
    params = {}
    if date_filter:
        params["date"] = date_filter
    r = requests.get(
        f"{API_BASE}/employees/{employee_id}/attendance",
        params=params,
        timeout=TIMEOUT
    )
    return _handle(r)

def dashboard_summary():
    r = requests.get(f"{API_BASE}/dashboard/summary", timeout=TIMEOUT)
    return _handle(r)
