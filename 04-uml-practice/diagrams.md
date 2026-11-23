# UML diagrams

## Exercise 1 — Hospital Management System

### Class diagram, developed model

```mermaid
classDiagram
    class User {
      <<abstract>>
      +str id
      +str name
      +str password_hash
      +login()
      +logout()
    }
    class Patient {
      +str contact_details
      +submit_problem(text)
      +pay(payment)
    }
    class Doctor {
      +str specialty
      +review(problem)
      +issue_prescription(problem, text)
    }
    class Organizer {
      +str role
      +assign_doctor(problem, doctor)
      +deliver_prescription(prescription)
      +forward_payment(payment)
      +create_member(name)
    }
    class HealthProblem {
      +str id
      +str description
      +ProblemStatus status
      +datetime submitted_at
      +set_status(status)
    }
    class Prescription {
      +str id
      +str instructions
      +datetime issued_at
    }
    class Payment {
      +str id
      +decimal amount
      +PaymentStatus status
      +process()
      +forward_to_doctor()
    }
    class ProblemStatus {
      <<enumeration>>
      pending
      in_review
      resolved
    }
    class PaymentStatus {
      <<enumeration>>
      pending
      paid
      forwarded
      failed
    }
    class PaymentMethod {
      <<interface>>
      +process(amount)
    }
    class CashPayment
    class CheckPayment
    class CardPayment
    User <|-- Patient
    User <|-- Doctor
    User <|-- Organizer
    Patient "1" --> "0..*" HealthProblem : submits
    Doctor "0..*" --> "0..*" HealthProblem : reviews
    Organizer "1" --> "0..*" HealthProblem : coordinates
    HealthProblem "1" --> "0..*" Prescription : history
    Doctor "1" --> "0..*" Prescription : issues
    Patient "1" --> "0..*" Payment : makes
    Payment "1" --> "1" PaymentMethod : uses
    PaymentMethod <|.. CashPayment
    PaymentMethod <|.. CheckPayment
    PaymentMethod <|.. CardPayment
    Organizer "1" --> "0..*" Payment : forwards
```

`ProblemStatus` has `pending`, `in_review`, and `resolved`; `PaymentStatus` has `pending`, `paid`, `forwarded`, and `failed`. Multiple doctors can review a problem. A prescription is a dated record linked to its problem, so older prescriptions remain available. A payment method handles the method-specific payment operation.

### Patient submits a problem, receives a prescription, and pays

```mermaid
sequenceDiagram
    actor Patient
    participant Portal
    participant Organizer
    participant Doctor
    participant Payment
    Patient->>Portal: submit problem(description)
    Portal->>Organizer: queue problem
    Organizer->>Doctor: assign for review
    Doctor->>Portal: issue prescription
    Portal-->>Patient: deliver prescription
    Patient->>Portal: pay(method, amount)
    Portal->>Payment: process(method, amount)
    Payment-->>Organizer: payment received
    Organizer->>Doctor: forward payment
```

### Registration

```mermaid
sequenceDiagram
    actor Patient
    participant Organizer
    participant MembershipService
    Patient->>Organizer: request registration
    Organizer->>MembershipService: create member(name, contact)
    MembershipService-->>Organizer: member id and credentials
    Organizer-->>Patient: provide account details
```

### Consultation and payment processing

```mermaid
sequenceDiagram
    actor Patient
    participant Organizer
    participant Doctor
    participant PaymentService
    Patient->>Organizer: submit health problem
    Organizer->>Doctor: assign problem
    Doctor->>Organizer: prescription and fee
    Organizer-->>Patient: deliver prescription and amount due
    Patient->>PaymentService: pay using selected method
    PaymentService-->>Organizer: record successful payment
    Organizer->>Doctor: forward payment
    Organizer->>Doctor: confirm remittance
```

### Data integrity notes

- Give every payment a unique idempotency key; retrying a request must not charge twice.
- Record payment state transitions transactionally (`pending` → `paid` → `forwarded`) and keep an audit trail.
- Mark the patient payment as successful only after the chosen method confirms it; record failed attempts separately.
- Treat forwarding as a separate, reconcilable transaction linked to the patient payment.

The payment strategy interface is the Strategy pattern: each cash, check, or card method provides the same `process(amount)` contract.

## Exercise 2 — ABCD Records

### Use-case diagram, core level

```mermaid
flowchart LR
    Member[Member] --> PlaceOrder((Place order))
    Clerk[Order processing clerk] --> Verify((Verify membership))
    Clerk --> Process((Process order))
    Member --> Pay((Make payment))
    PlaceOrder -. includes .-> Verify
    PlaceOrder -. includes .-> Process
```

### Full use-case diagram

```mermaid
flowchart LR
    Member[Member] --> Place((Place order))
    Clerk[Order processing clerk] --> Verify((Verify membership))
    Clerk --> Availability((Verify item availability))
    Clerk --> Process((Process order))
    Collection[Collection department clerk] --> Payment((Record payment))
    Nonmember[Non-member] --> Apply((Request membership form))
    Place -. includes .-> Verify
    Place -. includes .-> Availability
    Process -. includes .-> Discount((Apply discount))
    Process -. includes .-> Invoice((Print invoice))
    Process -. includes .-> Shipping((Print shipping list))
    Unavailable((Order unavailable item)) -. extends .-> Availability
    Unavailable -. condition: Royal member .-> Royal[Royal member]
    Apply -. includes .-> SendForm((Send membership application))
```

The unavailable-item extension is permitted only for Royal members. `Place order` and `process order` are shown separately to make membership and fulfillment responsibilities clear.

### Class diagram

```mermaid
classDiagram
    class Member {
      <<abstract>>
      +str member_id
      +str name
      +str address
      +place_order()
    }
    class RoyalMember {
      +float discount_rate
      +bool priority
      +order_unavailable_item()
    }
    class RegularMember
    class Order {
      +str order_id
      +datetime created_at
      +OrderStatus status
      +calculate_total()
    }
    class OrderLine {
      +int quantity
      +decimal unit_price
      +line_total()
    }
    class Item {
      <<abstract>>
      +str item_id
      +str title
      +decimal price
      +bool available
    }
    class CD
    class Tape
    class Invoice {
      +str invoice_id
      +decimal total
      +print()
    }
    class ShippingList {
      +str list_id
      +print()
    }
    class Payment {
      <<abstract>>
      +decimal amount
      +record()
    }
    class CashPayment
    class CheckPayment
    class BankDraftPayment
    class MembershipApplication
    class OrderProcessingClerk
    class CollectionDepartmentClerk
    Member <|-- RoyalMember
    Member <|-- RegularMember
    Item <|-- CD
    Item <|-- Tape
    Payment <|-- CashPayment
    Payment <|-- CheckPayment
    Payment <|-- BankDraftPayment
    Member "1" --> "0..*" Order : places
    Order "1" *-- "1..*" OrderLine : contains
    OrderLine "0..*" --> "1" Item : refers to
    Order "1" --> "0..1" Invoice : produces
    Order "1" --> "0..1" ShippingList : produces
    Order "1" --> "0..1" Payment : paid by
    OrderProcessingClerk "1" --> "0..*" Order : verifies and processes
    CollectionDepartmentClerk "1" --> "0..*" Payment : records
```

### Order processing: Royal member, two CDs, one unavailable, pays by check

```mermaid
sequenceDiagram
    actor RoyalMember
    participant Clerk as Order Processing Clerk
    participant Catalog
    participant Order
    participant Collection as Collection Department Clerk
    RoyalMember->>Clerk: place order (2 CDs)
    Clerk->>Catalog: verify Royal membership
    Catalog-->>Clerk: membership valid
    Clerk->>Catalog: check availability
    Catalog-->>Clerk: one available, one unavailable
    Clerk->>Order: add both lines and apply Royal discount
    Clerk-->>RoyalMember: invoice and shipping list
    RoyalMember->>Collection: pay by check
    Collection->>Order: record payment
    Order-->>Catalog: save order in daily records
```

### Membership verification: success and failure

```mermaid
sequenceDiagram
    actor Clerk
    participant Membership as Membership Registry
    Clerk->>Membership: verify(member id)
    alt valid member
        Membership-->>Clerk: active; tier=Royal or Regular
        Clerk->>Clerk: continue order processing
    else unknown or inactive member
        Membership-->>Clerk: verification failed
        Clerk-->>Clerk: reject order and explain reason
    end
```

### Payment processing by type

```mermaid
sequenceDiagram
    actor Member
    participant Collection as Collection Clerk
    participant Payment as Payment Processor
    Member->>Collection: submit payment and order id
    alt Cash
        Collection->>Payment: record cash received
    else Check
        Collection->>Payment: record check details
    else Bank draft
        Collection->>Payment: record bank draft details
    end
    Payment-->>Collection: payment status and receipt id
    Collection-->>Member: confirm recorded payment
```

### Reorder unavailable item for Royal member

```mermaid
sequenceDiagram
    actor RoyalMember
    participant Clerk as Order Processing Clerk
    participant Catalog
    participant Order
    RoyalMember->>Clerk: request unavailable item
    Clerk->>Catalog: verify Royal tier and item status
    Catalog-->>Clerk: Royal tier confirmed; item unavailable
    Clerk->>Order: add backorder line
    Order-->>RoyalMember: confirm backorder and expected follow-up
    Clerk->>Catalog: save order in daily records
```

### Assumptions

- Each order has one member and at least one order line; a member may place many orders.
- A Royal discount is calculated during order processing. The business must define whether discounts apply to shipping; this model assumes item subtotals only.
- A daily record is an order repository/audit record, not a separate UML entity in the first class diagram.
- A Royal unavailable-item request is a backorder; stock reservation and delivery timing are outside this exercise's stated scope.
