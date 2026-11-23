"""Fluent Builder exercise for readable employee construction."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Employee:
    first_name: str
    last_name: str
    email: str
    department: str
    position: str
    salary: float
    start_date: str
    manager_id: int | None = None
    phone: str | None = None
    address: str | None = None
    emergency_contact: str | None = None
    has_parking: bool = False
    has_laptop: bool = False
    has_vpn_access: bool = False
    has_admin_rights: bool = False
    office_location: str | None = None
    contract_type: str = "permanent"


class EmployeeBuilder:
    def __init__(self) -> None:
        self._values: dict[str, object] = {}

    def with_name(self, first_name: str, last_name: str) -> EmployeeBuilder:
        self._values.update(first_name=first_name, last_name=last_name)
        return self

    def with_email(self, email: str) -> EmployeeBuilder:
        self._values["email"] = email
        return self

    def with_job(self, department: str, position: str, salary: float,
                 start_date: str = "") -> EmployeeBuilder:
        self._values.update(department=department, position=position,
                            salary=salary, start_date=start_date)
        return self

    def with_equipment(self, *, laptop: bool = False, parking: bool = False) -> EmployeeBuilder:
        self._values.update(has_laptop=laptop, has_parking=parking)
        return self

    def with_access(self, *, vpn: bool = False, admin: bool = False) -> EmployeeBuilder:
        self._values.update(has_vpn_access=vpn, has_admin_rights=admin)
        return self

    def with_contact(self, *, phone: str | None = None, address: str | None = None,
                     emergency_contact: str | None = None) -> EmployeeBuilder:
        self._values.update(phone=phone, address=address, emergency_contact=emergency_contact)
        return self

    def with_manager(self, manager_id: int | None) -> EmployeeBuilder:
        self._values["manager_id"] = manager_id
        return self

    def with_contract(self, contract_type: str, office_location: str | None = None) -> EmployeeBuilder:
        self._values.update(contract_type=contract_type, office_location=office_location)
        return self

    def build(self) -> Employee:
        required = ("first_name", "last_name", "email", "department", "position", "salary")
        missing = [field for field in required if not self._values.get(field)]
        if missing:
            raise ValueError("Missing required employee fields: " + ", ".join(missing))
        if "@" not in str(self._values["email"]):
            raise ValueError("A valid email is required")
        if float(self._values["salary"]) < 0:
            raise ValueError("Salary cannot be negative")
        values = {"start_date": "", **self._values}
        return Employee(**values)  # type: ignore[arg-type]


class DeveloperBuilder(EmployeeBuilder):
    """Convenient preset for a developer role with standard engineering access."""
    def __init__(self, first_name: str, last_name: str, email: str) -> None:
        super().__init__()
        self.with_name(first_name, last_name).with_email(email)
        self.with_job("Engineering", "Developer", 0.0)
        self.with_equipment(laptop=True).with_access(vpn=True)


if __name__ == "__main__":
    employee = (EmployeeBuilder().with_name("Jane", "Doe")
                .with_email("jane.doe@example.com")
                .with_job("Engineering", "Senior Developer", 75000, "2026-01-15")
                .with_equipment(laptop=True).with_access(vpn=True, admin=True).build())
    print(employee)
