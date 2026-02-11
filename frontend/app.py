import os
from datetime import date
import pandas as pd
import streamlit as st

from api_client import (
    health, list_employees, create_employee, delete_employee,
    mark_attendance, get_attendance, dashboard_summary
)
from ui_components import inject_css, card_start, card_end, kpi_card, empty_state, show_error

st.set_page_config(page_title="Human Resource Management System",page_icon="👥", layout="wide")
inject_css()

API_BASE = os.getenv("API_BASE", "http://127.0.0.1:5000/api")

# Sidebar
with st.sidebar:
    st.title("HRMS Lite")
    st.caption("Admin Dashboard")
    st.divider()

    page = st.radio("Navigation", ["Dashboard", "Employees", "Attendance"])

    st.divider()
    st.markdown("### API Status")
    try:
        health()
        st.success("Online")
    except Exception as e:
        st.error("Offline")
        st.caption(str(e))


# ---------------- Dashboard ----------------
if page == "Dashboard":
    st.title("Dashboard")

    try:
        data = dashboard_summary()

        c1, c2 = st.columns(2)
        with c1:
            kpi_card("Total Employees", data.get("total_employees", 0))
        with c2:
            kpi_card("Attendance Records", data.get("total_attendance_records", 0))

    except Exception as e:
        show_error(e)


# ---------------- Employees ----------------
elif page == "Employees":
    st.title("Employee Management")

    card_start("Add Employee")

    col1, col2 = st.columns(2)
    with col1:
        employee_id = st.text_input("Employee ID")
        full_name = st.text_input("Full Name")
    with col2:
        email = st.text_input("Email")
        department = st.text_input("Department")

    if st.button("Create Employee", type="primary"):
        try:
            create_employee(employee_id, full_name, email, department)
            st.success("Employee created successfully")
            st.rerun()
        except Exception as e:
            show_error(e)

    card_end()

    st.subheader("Employee List")

    try:
        employees = list_employees()

        # ✅ BONUS 2: Get present days per employee
        summary = dashboard_summary()
        present_map = summary.get("present_days_per_employee", {}) or {}

    except Exception as e:
        show_error(e)
        st.stop()

    if not employees:
        empty_state("No employees found.")
    else:
        df = pd.DataFrame(employees)

        # ✅ Add present days column
        df["present_days"] = df["employee_id"].apply(lambda x: present_map.get(x, 0))

        # ✅ Optional: Sort by present days (high → low)
        df = df.sort_values("present_days", ascending=False)

        st.dataframe(
            df[["employee_id", "full_name", "email", "department", "present_days"]],
            use_container_width=True,
            hide_index=True
        )

        st.markdown("### Delete Employee")
        emp_ids = [e["employee_id"] for e in employees]
        selected = st.selectbox("Select Employee", emp_ids)

        if st.button("Delete Selected"):
            try:
                delete_employee(selected)
                st.success("Employee deleted")
                st.rerun()
            except Exception as e:
                show_error(e)


# ---------------- Attendance ----------------
elif page == "Attendance":
    st.title("Attendance Management")

    try:
        employees = list_employees()
    except Exception as e:
        show_error(e)
        st.stop()

    if not employees:
        empty_state("Add employees first.")
        st.stop()

    emp_ids = [e["employee_id"] for e in employees]

    card_start("Mark Attendance")

    col1, col2, col3 = st.columns(3)
    with col1:
        selected_emp = st.selectbox("Employee", emp_ids)
    with col2:
        att_date = st.date_input("Date", value=date.today())
    with col3:
        status = st.selectbox("Status", ["Present", "Absent"])

    if st.button("Mark Attendance", type="primary"):
        try:
            mark_attendance(selected_emp, att_date.isoformat(), status)
            st.success("Attendance marked")
            st.rerun()
        except Exception as e:
            show_error(e)

    card_end()

    st.subheader("Attendance Records")

    # ✅ BONUS 1: Filter by date
    with st.expander("Filter attendance by date", expanded=False):
        enable_filter = st.checkbox("Enable date filter", value=False)
        filter_date = st.date_input("Select date", value=date.today()) if enable_filter else None

    date_filter_str = filter_date.isoformat() if enable_filter and filter_date else None

    try:
        records = get_attendance(selected_emp, date_filter=date_filter_str)
    except Exception as e:
        show_error(e)
        st.stop()

    if not records:
        empty_state("No attendance records.")
    else:
        df = pd.DataFrame(records)
        st.dataframe(
            df[["date", "status"]].sort_values("date", ascending=False),
            use_container_width=True,
            hide_index=True
        )
