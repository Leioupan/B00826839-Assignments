"""Adapter exercise: make a legacy XML report producer fit a JSON consumer."""
from __future__ import annotations

import json
import xml.etree.ElementTree as ET
from abc import ABC, abstractmethod
from typing import Any


class ReportGeneratorInterface(ABC):
    @abstractmethod
    def generate(self, data: dict[str, Any]) -> str:
        """Return a JSON string for the analytics dashboard."""


class LegacyReportGenerator:
    """External legacy dependency; its XML interface is left unchanged."""
    def generate_report(self, data: dict[str, Any]) -> str:
        root = ET.Element("report")
        for key, value in data.items():
            ET.SubElement(root, str(key)).text = str(value)
        return ET.tostring(root, encoding="unicode")


class LegacyReportAdapter(ReportGeneratorInterface):
    def __init__(self, legacy: LegacyReportGenerator) -> None:
        self._legacy = legacy

    def generate(self, data: dict[str, Any]) -> str:
        xml_report = self._legacy.generate_report(data)
        root = ET.fromstring(xml_report)
        normalized = {child.tag: child.text or "" for child in root}
        return json.dumps(normalized)


class AnalyticsDashboard:
    def display(self, json_data: str) -> str:
        data = json.loads(json_data)
        lines = ["=== Analytics Dashboard ==="]
        lines.extend(f"{key}: {value}" for key, value in data.items())
        return "\n".join(lines)


if __name__ == "__main__":
    report_generator = LegacyReportAdapter(LegacyReportGenerator())
    report = report_generator.generate({"total_sales": 150000, "orders": 1234})
    print(AnalyticsDashboard().display(report))
