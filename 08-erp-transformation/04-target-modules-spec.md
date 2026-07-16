# 04 — Target Module Specifications

Each module below is specified at planning depth: **purpose**, **key entities** (described,
not coded), **primary workflows**, **integration points** (how it cross-links to the rest of
the ERP — the property that makes this an ERP, per chapter 01), and **business value**. All
respect the right-sizing charter (§3.2). Mockups already exist for modules A–D in
`03-mockups/v2/`, so screens are understood.

A consolidated data-model view is in [`05-system-design.md`](05-system-design.md).

---

## Module A — Inventory & Suppliers *(MUST: M2)*

**Purpose.** Know what raw materials and finished accessories are in stock, what they're
worth, and what needs reordering; record every stock-in and stock-out; maintain a supplier
directory. Mockup: `10-inventory.html`.

**Key entities.**
- `Supplier` — raw-material vendor (name, phone, location, category, `active`). *Distinct
  from `Company` (buyer) and from outsource `Vendor`.*
- `InventoryItem` — item master: name, `sku` (unique), category (Button/Zipper/Thread/
  Label/Packaging/Other), `unit`, `minStockLevel`, `unitCost` (Decimal), `defaultSupplierId`,
  `active`. On-hand quantity is **derived** from movements (auditable), not stored loosely.
- `StockMovement` — append-only ledger: item, direction (IN/OUT/ADJUST), quantity,
  `unitCost`, value, date, `supplierId?` (for IN), `orderId?` (for OUT, consumption against
  an order), `reference` (invoice/PO), note, actor.

**Primary workflows.**
1. *Add item* → defines SKU, category, unit, reorder level, opening stock.
2. *Stock In* → records a receipt (qty, unit cost, supplier, ref, optional linked order);
   raises on-hand.
3. *Stock Out* → issues material to an order (consumption) or writes off; lowers on-hand.
4. *Reorder alert* → items at/below `minStockLevel` surface on the dashboard.

**Integration points.**
- **→ Accounting:** a Stock-In posts a **purchase expense / payable**; a Stock-Out against
  an order posts a **MATERIALS cost** (reusing the existing `CostType.MATERIALS`).
- **→ Orders:** Stock-Out `orderId` links consumption to the job, feeding per-order cost.
- **→ Procurement:** Goods Receipt (Module E) is the formal source of Stock-In.

**Business value.** Stops stockouts mid-order, reveals working capital tied up in stock,
and makes material cost-per-order real instead of guessed.

---

## Module B — Accounting *(MUST: M1; generalises the Cash Book)*

**Purpose.** A categorised income/expense ledger producing a **monthly P&L**, plus
**receivables (AR)** against PIs and **payables (AP)** against supplier bills. Mockup:
`11-accounts.html`. This is the **highest-priority** module — it answers the owner's
sharpest questions.

**Design decision (see §05).** *Generalise the existing `CashEntry`* into a fuller
`LedgerEntry` rather than build a parallel system — the Cash Book already has direction,
amount, category, order-link, and cost-type. We add: a `PENDING` (accrual) state for
receivables/payables, richer categories, a fiscal-year view, and links to PI/PO/payroll/
fuel sources.

**Key entities.**
- `LedgerEntry` (evolved `CashEntry`) — date, `type` (INCOME/EXPENSE), `status`
  (SETTLED/PENDING), `category` (income: Order Payment, Advance, Other; expense: Salary,
  Purchase, Rent, Transport, Utilities, Maintenance, Other), `amount` (Decimal),
  `reference`, `description`, optional FKs: `companyId`, `orderId`, `piId`, `costType`,
  `source` (CASH/PAYROLL/STOCK/FUEL/MANUAL), actor.
- `Receivable` — derived/linked from a finalized `PI`: `dueDate`, `amountDue`,
  `amountPaid`, `status` (OPEN/PARTIAL/PAID/OVERDUE). (May be modelled as a `Payment` table
  against PI rather than a separate entity — see §05.)
- `Payable` — supplier bill from a Goods Receipt: due date, amount, paid status.

**Primary workflows.**
1. *Record income/expense* → a categorised ledger entry (manual or auto-posted by another
   module).
2. *Receivables aging* → from finalized PIs, show who owes what and days overdue; record
   payments to clear.
3. *Monthly P&L* → income − expense by category for the fiscal year (Apr–Mar).
4. *Expense breakdown* → % by category for cost control.

**Integration points.** Receives auto-posted entries from **Inventory** (purchases),
**Procurement** (payables), **HR/Payroll** (salaries), and **Fleet** (fuel/maintenance);
receivables flow from **PI/Orders**.

**Business value.** Converts "I think we made money" into a monthly profit figure;
surfaces overdue buyer payments and LC-linked receivables; gives a defensible cost base for
pricing.

---

## Module C — HR & Payroll *(SHOULD: S2)*

**Purpose.** Internal staff directory, monthly payroll, leave. Mockup: `12-hr-payroll.html`
(shows 8 employees across Admin/Accounts/Sales/Operations/Driver).

**Key entities.**
- `Employee` — name, designation, `department` (Admin/Accounts/Sales/Operations/Driver),
  `joinDate`, `monthlySalary` (Decimal), phone, `nationalId`, `paymentMode`
  (Cash/Bank/MobilePay), `bankAccount?`, `status` (Active/On-Leave), `active`. *Optionally
  linked to a `User` for staff who log in; conceptually separate from buyer-side
  `Merchandiser`.*
- `SalaryPayment` — employee, period (month), `gross`, `deduction`, `net`, `paymentMode`,
  `status` (PAID/PENDING/ADVANCE), `paymentDate`, note. Produces a printable slip.
- `LeaveRequest` — employee, type, date range, days, reason, `status`
  (PENDING/APPROVED/REJECTED).

**Primary workflows.** Add employee → process monthly salary (single or "all pending") →
issue slip; submit/approve leave; 6-month payroll summary.

**Integration points.** **→ Accounting:** each `SalaryPayment` auto-posts a **Salary
expense**. **→ Fleet:** `Driver` employees (department = Driver) link to vehicles.

**Business value.** Replaces manual salary registers; ties the single largest expense
category (the mockup shows salary ≈ 37% of expenses) into the P&L automatically.

---

## Module D — Fleet *(COULD: C1; owner-requested)*

**Purpose.** Vehicle/driver register, trip & fuel logging, maintenance, document-expiry
alerts (insurance/fitness/licence). Mockup: `13-vehicles.html`.

**Key entities.**
- `Vehicle` — regNo, make/model/year/color, `type` (Van/Car/Pickup/Motorcycle), `status`
  (Active/In-Service/Off-road), `insuranceExpiry`, `fitnessExpiry`, `odometer`,
  `assignedDriverId`.
- `Driver` — name, phone, `licenseNo`, `licenseExpiry`, `nid`, `assignedVehicleId`,
  `status`. *May reuse `Employee` (department = Driver) rather than a separate table — see
  §05 decision.*
- `Trip` — date, vehicle, driver, from/to, purpose, `distanceKm`, `fuelCost` (Decimal),
  optional `orderId` (delivery/sample dispatch links to an order), note.
- `MaintenanceRecord` — date, vehicle, work done, workshop, `cost` (Decimal), next due.

**Primary workflows.** Register vehicle/driver → log trips (with fuel) → log maintenance →
expiry alerts on the dashboard.

**Integration points.** **→ Accounting:** fuel + maintenance auto-post **Transport
expense**. **→ Orders:** delivery trips link to the order dispatched. **→ HR:** drivers are
employees.

**Business value.** Captures the Transport cost line (mockup ≈ 8% of expenses), prevents
lapsed insurance/fitness fines, and attributes delivery cost to orders.

---

## Module E — Procurement *(SHOULD: S1; pairs with Inventory)*

**Purpose.** Lightweight purchase orders to suppliers and goods receipt — the formal
"procure-to-pay" path that feeds Inventory and Accounts. Greenfield (no mockup yet; kept
deliberately minimal per P4).

**Key entities.**
- `PurchaseOrder` — `poNo`, `supplierId`, date, `status` (DRAFT/SENT/RECEIVED/CANCELLED),
  lines (item, qty, unit cost), total (Decimal), note.
- `GoodsReceipt` — links a PO (or is standalone), receipt date, lines received → generates
  Stock-In movements and a Payable.

**Primary workflows.** Raise PO → send to supplier → receive goods (full/partial) → stock
rises, payable created → settle payable in Accounting.

**Integration points.** **→ Inventory** (Stock-In), **→ Accounting** (Payable/AP). No
approval chains, no RFQ (P4).

**Business value.** Turns ad-hoc buying into tracked spend; automatically values incoming
stock and records what IKON owes suppliers.

---

## Module F — Cross-cutting: Master Data, Audit & Reporting *(MUST: M3 + SHOULD: S3)*

**Purpose.** The "glue" that makes the modules one system rather than five.

**Components.**
- **Generalised audit log** (X1) — extend the order-only `TimelineEntry` concept into an
  `AuditLog` capturing who/what/when/before-after for cash, ledger, stock, payroll, and
  master-data changes. Append-only.
- **Master-data administration** (X2) — admin screens for `User`/role management,
  `Supplier` and `InventoryItem` masters, and `Employee` master; shared partner/item data
  consumed by every module.
- **Consolidated reporting/BI** (S3) — cross-module dashboard: cash position, AR aging,
  stock value & reorder list, monthly P&L, payroll due, expiry alerts.

**Business value.** Traceability (essential once money/stock are tracked), no duplicate
master data, and a single management cockpit — the visible "ERP" surface for the owner.

---

## Module integration map (the ERP-ness, at a glance)

```
                         ┌─────────────────────────────────────────┐
                         │              ACCOUNTING (B)              │
                         │  income/expense ledger · P&L · AR · AP   │
                         └───▲────────▲────────▲────────▲────────▲──┘
       material cost / purchase │     │ payable │ salary │ fuel+maint │ receivable
                         │     │        │        │        │        │
   ┌─────────────┐  Stock-Out  │  ┌──────────┐ ┌────────┐ ┌───────┐ ┌──────────┐
   │ INVENTORY(A)│────────────┘  │PROCURE(E)│ │ HR (C) │ │FLEET D│ │ ORDERS / │
   │ items·stock │  Stock-In ◀────│ PO·GRN   │ │payroll │ │trips  │ │ PI · LC  │
   │ ·suppliers  │                └────┬─────┘ └───┬────┘ └───┬───┘ │ (EXISTING)│
   └──────▲──────┘                     │ supplier  │ driver   │ order└────┬──────┘
          │ consume against order      │           │          │           │
          └────────────────────────────┴───────────┴──────────┴───────────┘
                       all share ONE PostgreSQL database + audit (F)
```

Every arrow is an automatic cross-post — the integration that distinguishes an ERP from a
folder of separate apps.
