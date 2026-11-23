"""Template Method exercise: share ETL workflow across data sources."""
from __future__ import annotations

from abc import ABC, abstractmethod
from copy import deepcopy
from typing import Any


class DataPipeline(ABC):
    """The run method fixes workflow order while subclasses specialize steps."""
    required_fields: tuple[str, ...] = ()

    def __init__(self, source: str) -> None:
        self.source = source
        self.data: list[dict[str, Any]] | None = None

    def run(self) -> list[dict[str, Any]]:
        try:
            self.connect()
            self.data = self.extract()
            self.transform()
            self.validate()
            self.load()
            return deepcopy(self.data)
        finally:
            self.cleanup()

    def connect(self) -> None:
        print(f"Connecting to {self.source}...")

    @abstractmethod
    def extract(self) -> list[dict[str, Any]]: ...

    @abstractmethod
    def transform(self) -> None: ...

    def validate(self) -> None:
        assert self.data is not None
        for index, record in enumerate(self.data):
            missing = [field for field in self.required_fields if field not in record]
            if missing:
                raise ValueError(f"record {index} missing required fields: {', '.join(missing)}")
        print(f"Validated {len(self.data)} records")

    def load(self) -> None:
        assert self.data is not None
        print(f"Loaded {len(self.data)} records")

    def cleanup(self) -> None:
        self.data = None
        print("Pipeline cleanup complete")


class CSVPipeline(DataPipeline):
    required_fields = ("id", "name", "age")

    def extract(self) -> list[dict[str, Any]]:
        print(f"Extracting CSV data from {self.source}")
        return [{"id": 1, "name": "Alice", "age": "30"}, {"id": 2, "name": "Bob", "age": "25"}]

    def transform(self) -> None:
        assert self.data is not None
        for row in self.data:
            row["age"] = int(row["age"])
            row["name"] = row["name"].upper()


class APIPipeline(DataPipeline):
    required_fields = ("user_id", "username", "score", "grade")

    def extract(self) -> list[dict[str, Any]]:
        print(f"Extracting API data from {self.source} (sample fixture; no network call)")
        return [{"user_id": 101, "username": "charlie", "score": "85"},
                {"user_id": 102, "username": "diana", "score": "92"}]

    def transform(self) -> None:
        assert self.data is not None
        for row in self.data:
            row["score"] = int(row["score"])
            row["username"] = row["username"].lower()
            row["grade"] = "A" if row["score"] >= 90 else "B"


class DatabasePipeline(DataPipeline):
    required_fields = ("product_id", "product_name", "price", "tax")

    def extract(self) -> list[dict[str, Any]]:
        print(f"Extracting database data from {self.source} (sample fixture; no DB connection)")
        return [{"product_id": 501, "product_name": "laptop", "price": "1200"},
                {"product_id": 502, "product_name": "mouse", "price": "25"}]

    def transform(self) -> None:
        assert self.data is not None
        for row in self.data:
            row["price"] = float(row["price"])
            row["product_name"] = row["product_name"].title()
            row["tax"] = round(row["price"] * 0.2, 2)


class XMLPipeline(CSVPipeline):
    """Small extension example demonstrating a new source following the template."""
    def extract(self) -> list[dict[str, Any]]:
        print(f"Extracting XML data from {self.source} (sample fixture)")
        return [{"id": 3, "name": "orders", "age": "1"}]


if __name__ == "__main__":
    pipelines = (CSVPipeline("data/users.csv"), APIPipeline("https://api.example.test/users"),
                 DatabasePipeline("sample database"), XMLPipeline("data/orders.xml"))
    for pipeline in pipelines:
        print(pipeline.__class__.__name__, "result:", pipeline.run())
