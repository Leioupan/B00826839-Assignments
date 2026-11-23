"""Decorator exercise: compose order pricing features without boolean flags."""
from __future__ import annotations

from abc import ABC, abstractmethod


class OrderComponent(ABC):
    @abstractmethod
    def get_cost(self) -> float: ...

    @abstractmethod
    def get_description(self) -> str: ...


class BaseOrder(OrderComponent):
    def __init__(self, base_price: float) -> None:
        if base_price < 0:
            raise ValueError("base price cannot be negative")
        self.base_price = float(base_price)

    def get_cost(self) -> float:
        return self.base_price

    def get_description(self) -> str:
        return f"Base order: €{self.base_price:.2f}"


class OrderDecorator(OrderComponent):
    def __init__(self, wrapped: OrderComponent) -> None:
        self.wrapped = wrapped

    def get_cost(self) -> float:
        return self.wrapped.get_cost()

    def get_description(self) -> str:
        return self.wrapped.get_description()


class ExpressShippingDecorator(OrderDecorator):
    def get_cost(self) -> float:
        return self.wrapped.get_cost() + 15.00

    def get_description(self) -> str:
        return f"{self.wrapped.get_description()}\nExpress shipping: +€15.00"


class InsuranceDecorator(OrderDecorator):
    def get_cost(self) -> float:
        return self.wrapped.get_cost() + self.wrapped.get_cost() * 0.05

    def get_description(self) -> str:
        return f"{self.wrapped.get_description()}\nInsurance (5%): +€{self.wrapped.get_cost() * 0.05:.2f}"


class GiftWrapDecorator(OrderDecorator):
    def get_cost(self) -> float:
        return self.wrapped.get_cost() + 5.00

    def get_description(self) -> str:
        return f"{self.wrapped.get_description()}\nGift wrap: +€5.00"


class DiscountDecorator(OrderDecorator):
    def __init__(self, wrapped: OrderComponent, percent: float) -> None:
        if not 0 <= percent <= 100:
            raise ValueError("discount percent must be between 0 and 100")
        super().__init__(wrapped)
        self.percent = percent

    def get_cost(self) -> float:
        return self.wrapped.get_cost() * (1 - self.percent / 100)

    def get_description(self) -> str:
        reduction = self.wrapped.get_cost() * self.percent / 100
        return f"{self.wrapped.get_description()}\nDiscount ({self.percent:g}%): -€{reduction:.2f}"


class PremiumMemberDecorator(OrderDecorator):
    def get_cost(self) -> float:
        return self.wrapped.get_cost() * 0.90

    def get_description(self) -> str:
        reduction = self.wrapped.get_cost() * 0.10
        return f"{self.wrapped.get_description()}\nPremium member (10%): -€{reduction:.2f}"


if __name__ == "__main__":
    order: OrderComponent = BaseOrder(100.00)
    order = ExpressShippingDecorator(order)
    order = InsuranceDecorator(order)
    order = GiftWrapDecorator(order)
    order = DiscountDecorator(order, percent=15)
    order = PremiumMemberDecorator(order)
    print(order.get_description())
    print(f"Total: €{order.get_cost():.2f}")
