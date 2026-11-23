"""Solutions for the linked OOP practice: operator overloading and inheritance."""
from __future__ import annotations

from dataclasses import dataclass
from functools import total_ordering
from math import hypot
from typing import Iterable


@dataclass(frozen=True)
class ComplexNumber:
    real: float
    imag: float = 0.0

    def __add__(self, other: ComplexNumber) -> ComplexNumber:
        if not isinstance(other, ComplexNumber):
            return NotImplemented
        return ComplexNumber(self.real + other.real, self.imag + other.imag)

    def __sub__(self, other: ComplexNumber) -> ComplexNumber:
        if not isinstance(other, ComplexNumber):
            return NotImplemented
        return ComplexNumber(self.real - other.real, self.imag - other.imag)


@dataclass(frozen=True)
class Person:
    name: str
    age: int
    gender: str

    def __gt__(self, other: Person) -> bool:
        if not isinstance(other, Person):
            return NotImplemented
        return self.age > other.age


@dataclass(frozen=True)
class Vector:
    x: float
    y: float
    z: float

    def __mul__(self, other: Vector) -> float:
        if not isinstance(other, Vector):
            return NotImplemented
        return self.x * other.x + self.y * other.y + self.z * other.z


@total_ordering
@dataclass(frozen=True)
class Circle:
    radius: float

    def __post_init__(self) -> None:
        if self.radius < 0:
            raise ValueError("radius cannot be negative")

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Circle):
            return NotImplemented
        return self.radius == other.radius

    def __lt__(self, other: Circle) -> bool:
        if not isinstance(other, Circle):
            return NotImplemented
        return self.radius < other.radius


@total_ordering
@dataclass(frozen=True)
class Point2D:
    x: float
    y: float

    @property
    def distance_from_origin(self) -> float:
        return hypot(self.x, self.y)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Point2D):
            return NotImplemented
        return self.distance_from_origin == other.distance_from_origin

    def __lt__(self, other: Point2D) -> bool:
        if not isinstance(other, Point2D):
            return NotImplemented
        return self.distance_from_origin < other.distance_from_origin


Matrix = list[list[float]]


def _shape(matrix: Matrix) -> tuple[int, int]:
    if not matrix or not matrix[0]:
        raise ValueError("matrices must be non-empty")
    width = len(matrix[0])
    if any(len(row) != width for row in matrix):
        raise ValueError("matrix rows must all have the same length")
    return len(matrix), width


def multiply_matrices(left: Matrix, right: Matrix) -> Matrix:
    """Return left × right; raise ValueError if dimensions are incompatible."""
    rows, inner = _shape(left)
    right_rows, columns = _shape(right)
    if inner != right_rows:
        raise ValueError(f"cannot multiply shapes {(rows, inner)} and {(right_rows, columns)}")
    return [[sum(left[r][k] * right[k][c] for k in range(inner))
             for c in range(columns)] for r in range(rows)]


class Vehicle:
    def drive(self) -> str:
        return "Driving a vehicle"


class Car(Vehicle):
    def drive(self) -> str:
        return "Driving a car"


class Bicycle(Vehicle):
    def drive(self) -> str:
        return "Riding a bicycle"


class PersonRecord:
    def __init__(self, name: str, age: int, address: str) -> None:
        self.name, self.age, self.address = name, age, address

    def introduce(self) -> str:
        return f"Hi, I'm {self.name}, age {self.age}, from {self.address}."


class Student(PersonRecord):
    def __init__(self, name: str, age: int, address: str, field_of_study: str) -> None:
        super().__init__(name, age, address)
        self.field_of_study = field_of_study

    def introduce(self) -> str:
        return f"{super().introduce()} I study {self.field_of_study}."


class Employee(PersonRecord):
    def __init__(self, name: str, age: int, address: str, company: str) -> None:
        super().__init__(name, age, address)
        self.company = company

    def introduce(self) -> str:
        return f"{super().introduce()} I work at {self.company}."


class BankAccount:
    def __init__(self, account_number: str, balance: float = 0.0) -> None:
        if balance < 0:
            raise ValueError("initial balance cannot be negative")
        self.account_number = account_number
        self.balance = float(balance)

    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("deposit amount must be positive")
        self.balance += amount

    def withdraw(self, amount: float) -> bool:
        if amount <= 0:
            raise ValueError("withdrawal amount must be positive")
        if amount > self.balance:
            return False
        self.balance -= amount
        return True

    def transfer(self, destination: BankAccount, amount: float) -> bool:
        if amount <= 0:
            raise ValueError("transfer amount must be positive")
        if destination is self:
            raise ValueError("cannot transfer to the same account")
        if not self.withdraw(amount):
            return False
        destination.deposit(amount)
        return True


class SavingsAccount(BankAccount):
    def __init__(self, account_number: str, balance: float = 0.0,
                 interest_rate: float = 0.0) -> None:
        super().__init__(account_number, balance)
        if interest_rate < 0:
            raise ValueError("interest rate cannot be negative")
        self.interest_rate = interest_rate

    def add_interest(self) -> float:
        interest = self.balance * self.interest_rate
        self.balance += interest
        return interest

    def check_balance(self) -> float:
        return self.balance


def main() -> None:
    print("Complex:", ComplexNumber(2, 3) + ComplexNumber(1, -1))
    print("Dot product:", Vector(1, 2, 3) * Vector(4, 5, 6))
    print("Matrix product:", multiply_matrices([[1, 2]], [[3], [4]]))
    print("Vehicle polymorphism:", [v.drive() for v in (Vehicle(), Car(), Bicycle())])
    source = BankAccount("A", 100)
    target = SavingsAccount("B", 25, interest_rate=0.02)
    source.transfer(target, 10)
    target.add_interest()
    print("Balances:", source.balance, target.check_balance())


if __name__ == "__main__":
    main()
