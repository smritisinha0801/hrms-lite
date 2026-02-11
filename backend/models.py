from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Date, Enum, BigInteger, ForeignKey, UniqueConstraint, func
from sqlalchemy import DateTime

class Base(DeclarativeBase):
    pass

class Employee(Base):
    __tablename__ = "employees"

    employee_id: Mapped[str] = mapped_column(String(50), primary_key=True)
    full_name: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    department: Mapped[str] = mapped_column(String(80), nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())

    attendance_records = relationship(
        "Attendance",
        back_populates="employee",
        cascade="all, delete",
        passive_deletes=True,
    )

class Attendance(Base):
    __tablename__ = "attendance"
    __table_args__ = (UniqueConstraint("employee_id", "att_date", name="uniq_employee_date"),)

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    employee_id: Mapped[str] = mapped_column(
        String(50),
        ForeignKey("employees.employee_id", ondelete="CASCADE"),
        nullable=False
    )
    att_date: Mapped[Date] = mapped_column(Date, nullable=False)
    status: Mapped[str] = mapped_column(Enum("Present", "Absent"), nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())

    employee = relationship("Employee", back_populates="attendance_records")
