"""Factory Method exercise: extensible payment processing."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class PaymentProcessor(ABC):
    @abstractmethod
    def validate(self, details: dict[str, Any]) -> bool:
        """Return whether the method-specific details are valid."""

    @abstractmethod
    def process(self, amount: float, details: dict[str, Any]) -> dict[str, Any]:
        """Validate and return a normalized payment result."""

    @staticmethod
    def _valid_amount(amount: float) -> bool:
        return isinstance(amount, (int, float)) and not isinstance(amount, bool) and amount >= 0


class CreditCardProcessor(PaymentProcessor):
    def validate(self, details: dict[str, Any]) -> bool:
        number, cvv = str(details.get("card_number", "")), str(details.get("cvv", ""))
        return number.isdigit() and len(number) == 16 and cvv.isdigit() and len(cvv) == 3

    def process(self, amount: float, details: dict[str, Any]) -> dict[str, Any]:
        if not self._valid_amount(amount):
            return {"success": False, "error": "Amount must be non-negative."}
        if not self.validate(details):
            return {"success": False, "error": "Invalid card number or CVV."}
        fee = round(amount * 0.029, 2)
        return {"success": True, "method": "credit_card", "amount": round(amount + fee, 2), "fee": fee}


class BankTransferProcessor(PaymentProcessor):
    def validate(self, details: dict[str, Any]) -> bool:
        iban = "".join(str(details.get("iban", "")).split())
        return len(iban) >= 15 and iban.isalnum()

    def process(self, amount: float, details: dict[str, Any]) -> dict[str, Any]:
        if not self._valid_amount(amount):
            return {"success": False, "error": "Amount must be non-negative."}
        if not self.validate(details):
            return {"success": False, "error": "Invalid IBAN."}
        fee = 1.50
        return {"success": True, "method": "bank_transfer", "amount": round(amount + fee, 2), "fee": fee}


class PayPalProcessor(PaymentProcessor):
    def validate(self, details: dict[str, Any]) -> bool:
        email = str(details.get("email", ""))
        return "@" in email and "." in email.rsplit("@", 1)[-1]

    def process(self, amount: float, details: dict[str, Any]) -> dict[str, Any]:
        if not self._valid_amount(amount):
            return {"success": False, "error": "Amount must be non-negative."}
        if not self.validate(details):
            return {"success": False, "error": "Invalid PayPal email."}
        fee = round(amount * 0.034 + 0.30, 2)
        return {"success": True, "method": "paypal", "amount": round(amount + fee, 2), "fee": fee}


class PaymentFactory:
    _processors: dict[str, type[PaymentProcessor]] = {
        "credit_card": CreditCardProcessor,
        "bank_transfer": BankTransferProcessor,
        "paypal": PayPalProcessor,
    }

    @classmethod
    def register(cls, name: str, processor: type[PaymentProcessor]) -> None:
        if not issubclass(processor, PaymentProcessor):
            raise TypeError("processor must implement PaymentProcessor")
        cls._processors[name] = processor

    def get_processor(self, payment_type: str) -> PaymentProcessor:
        try:
            processor = self._processors[payment_type]
        except KeyError as exc:
            raise ValueError(f"Unknown payment type: {payment_type}") from exc
        return processor()


if __name__ == "__main__":
    processor = PaymentFactory().get_processor("credit_card")
    print(processor.process(100.0, {"card_number": "1234567890123456", "cvv": "123"}))
