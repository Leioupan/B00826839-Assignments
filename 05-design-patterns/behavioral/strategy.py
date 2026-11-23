"""Strategy exercise: switch report formats at runtime."""
from __future__ import annotations

import csv
import html
import io
import json
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any


class FormatStrategy(ABC):
    extension = "txt"

    @abstractmethod
    def render(self, data: list[dict[str, Any]]) -> str: ...


class CSVFormatStrategy(FormatStrategy):
    extension = "csv"

    def render(self, data: list[dict[str, Any]]) -> str:
        if not data:
            return ""
        output = io.StringIO(newline="")
        writer = csv.DictWriter(output, fieldnames=list(data[0]))
        writer.writeheader()
        writer.writerows(data)
        return output.getvalue()


class JSONFormatStrategy(FormatStrategy):
    extension = "json"

    def render(self, data: list[dict[str, Any]]) -> str:
        return json.dumps(data, indent=2)


class HTMLFormatStrategy(FormatStrategy):
    extension = "html"

    def render(self, data: list[dict[str, Any]]) -> str:
        if not data:
            return "<!doctype html><table></table>"
        headers = list(data[0])
        head = "".join(f"<th>{html.escape(str(key))}</th>" for key in headers)
        rows = "".join("<tr>" + "".join(
            f"<td>{html.escape(str(item.get(key, '')))}</td>" for key in headers
        ) + "</tr>" for item in data)
        return f"<!doctype html><table><thead><tr>{head}</tr></thead><tbody>{rows}</tbody></table>"


class PDFFormatStrategy(FormatStrategy):
    """Readable console preview; plug in a PDF renderer for a real PDF binary."""
    extension = "txt"

    def render(self, data: list[dict[str, Any]]) -> str:
        lines = ["PDF REPORT", "=" * 50]
        lines.extend(f"| {item.get('name', ''):<20} | {item.get('value', ''):>10} |" for item in data)
        lines.extend(["=" * 50, "End of PDF report", "(Text preview; no PDF renderer dependency is bundled.)"])
        return "\n".join(lines)


class ExcelFormatStrategy(FormatStrategy):
    """Tab-separated console preview; plug in an XLSX writer for a real workbook."""
    extension = "txt"

    def render(self, data: list[dict[str, Any]]) -> str:
        if not data:
            return ""
        headers = list(data[0])
        lines = ["\t".join(headers)]
        lines.extend("\t".join(str(row.get(key, "")) for key in headers) for row in data)
        lines.append("(Tab-separated preview; no XLSX writer dependency is bundled.)")
        return "\n".join(lines)


class ReportGenerator:
    def __init__(self, data: list[dict[str, Any]], strategy: FormatStrategy | None = None) -> None:
        self.data = data
        self._strategy = strategy or JSONFormatStrategy()

    def set_strategy(self, strategy: FormatStrategy) -> None:
        self._strategy = strategy

    def generate_report(self) -> str:
        return self._strategy.render(self.data)

    def save_report(self, filename: str | Path) -> Path:
        path = Path(filename)
        if not path.suffix:
            path = path.with_suffix("." + self._strategy.extension)
        path.write_text(self.generate_report(), encoding="utf-8")
        return path


if __name__ == "__main__":
    records = [{"name": "Sales Q1", "value": 15000}, {"name": "Sales Q2", "value": 18000}]
    generator = ReportGenerator(records)
    for strategy in (PDFFormatStrategy(), CSVFormatStrategy(), JSONFormatStrategy(), HTMLFormatStrategy()):
        generator.set_strategy(strategy)
        print(f"--- {strategy.__class__.__name__} ---")
        print(generator.generate_report())
