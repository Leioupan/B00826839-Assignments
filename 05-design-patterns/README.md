# Design patterns assignment

This folder combines the three linked course pages into one assignment, as requested. It contains seven runnable examples:

- **Creational:** Factory for payment processors, Builder for employee onboarding, Singleton configuration manager.
- **Structural:** Adapter for a legacy XML report generator, Decorator for order pricing add-ons.
- **Behavioral:** Strategy for switching report formats at runtime, Template Method for a shared ETL pipeline.

Each implementation lives in its own module under `creational/`, `structural/`, or `behavioral/`. The combined class diagrams and modeling notes are in [`diagrams.md`](diagrams.md). The code uses Python's standard library only.

## Run examples

```bash
python3 creational/factory.py
python3 creational/builder.py
cp config.example.json config.json
python3 creational/singleton.py
python3 structural/adapter.py
python3 structural/decorator.py
python3 behavioral/strategy.py
python3 behavioral/template_method.py
```

The strategy exercise prints PDF and Excel shaped text previews, not real PDF/XLSX files. A production implementation should inject a PDF renderer and workbook writer; CSV, JSON, and HTML use real text serializations. The ETL source classes use local sample records rather than connecting to real services.
