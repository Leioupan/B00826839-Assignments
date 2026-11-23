# Design-pattern class diagrams

The three course pages form one assignment. The diagrams below show the example classes and pattern relationships.

## Creational patterns

```mermaid
classDiagram
    class PaymentProcessor {
      <<interface>>
      +validate(details) bool
      +process(amount, details) dict
    }
    class CreditCardProcessor
    class BankTransferProcessor
    class PayPalProcessor
    class PaymentFactory {
      +get_processor(type) PaymentProcessor
      +register(type, processor)
    }
    PaymentProcessor <|.. CreditCardProcessor
    PaymentProcessor <|.. BankTransferProcessor
    PaymentProcessor <|.. PayPalProcessor
    PaymentFactory ..> PaymentProcessor : creates
    class Employee {
      +first_name
      +last_name
      +email
      +department
      +position
      +salary
    }
    class EmployeeBuilder {
      +with_name()
      +with_job()
      +with_equipment()
      +build() Employee
    }
    EmployeeBuilder ..> Employee : builds
    class ConfigManager {
      -_instance
      -_config
      +get_instance(path) ConfigManager
      +get(key, default)
    }
```

## Structural patterns

```mermaid
classDiagram
    class ReportGeneratorInterface {
      <<interface>>
      +generate(data) str
    }
    class LegacyReportGenerator {
      +generate_report(data) XML
    }
    class LegacyReportAdapter {
      +generate(data) JSON
    }
    ReportGeneratorInterface <|.. LegacyReportAdapter
    LegacyReportAdapter o--> LegacyReportGenerator : wraps
    class OrderComponent {
      <<interface>>
      +get_cost() float
      +get_description() str
    }
    class BaseOrder
    class OrderDecorator
    class ExpressShippingDecorator
    class InsuranceDecorator
    class GiftWrapDecorator
    class DiscountDecorator
    class PremiumMemberDecorator
    OrderComponent <|.. BaseOrder
    OrderComponent <|.. OrderDecorator
    OrderDecorator <|-- ExpressShippingDecorator
    OrderDecorator <|-- InsuranceDecorator
    OrderDecorator <|-- GiftWrapDecorator
    OrderDecorator <|-- DiscountDecorator
    OrderDecorator <|-- PremiumMemberDecorator
    OrderDecorator o--> OrderComponent : wraps
```

## Behavioral patterns

```mermaid
classDiagram
    class FormatStrategy {
      <<interface>>
      +render(data) str
    }
    class PDFFormatStrategy
    class ExcelFormatStrategy
    class CSVFormatStrategy
    class JSONFormatStrategy
    class HTMLFormatStrategy
    class ReportGenerator {
      -strategy
      +set_strategy(strategy)
      +generate_report() str
      +save_report(filename)
    }
    FormatStrategy <|.. PDFFormatStrategy
    FormatStrategy <|.. ExcelFormatStrategy
    FormatStrategy <|.. CSVFormatStrategy
    FormatStrategy <|.. JSONFormatStrategy
    FormatStrategy <|.. HTMLFormatStrategy
    ReportGenerator o--> FormatStrategy : delegates to
    class DataPipeline {
      <<abstract>>
      +run()
      +connect()
      +extract()*
      +transform()*
      +validate()
      +load()
      +cleanup()
    }
    class CSVPipeline
    class APIPipeline
    class DatabasePipeline
    class XMLPipeline
    DataPipeline <|-- CSVPipeline
    DataPipeline <|-- APIPipeline
    DataPipeline <|-- DatabasePipeline
    CSVPipeline <|-- XMLPipeline
```

In the Template Method example, `run()` owns the fixed step order. Concrete pipelines override extraction and transformation while the base class shares validation, loading, and cleanup.
