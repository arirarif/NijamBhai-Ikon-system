# 03 — Gap Analysis & the Minimum ERP

This chapter converts the capability matrix (chapter 02) into a prioritised list of what
to add, states the **right-sizing principles** that keep the build appropriate for a
micro-enterprise, and defines the **minimum ERP scope** for IKON.

---

## 3.1 The gap, stated plainly

To move from "order-management app" to "small ERP," IKON must add four module groups and
generalise three cross-cutting concerns:

**Module gaps (the "missing ERP heads"):**

| # | Missing capability | Becomes module |
|---|---|---|
| G1 | Raw-material & finished-goods stock, valuation, reorder alerts | **Inventory** |
| G2 | Supplier master + purchase orders + goods receipt | **Procurement & Suppliers** (paired with Inventory) |
| G3 | Categorised income/expense ledger, monthly P&L, receivables (AR), payables (AP) | **Accounting** (generalises the Cash Book) |
| G4 | Employee master, monthly payroll, leave | **HR & Payroll** |
| G5 | Vehicle/driver register, trip & fuel log, maintenance | **Fleet** *(owner-requested; optional to "ERP-ness")* |

**Cross-cutting gaps:**

| # | Missing capability | Becomes |
|---|---|---|
| X1 | Audit trail for non-order data (cash, master data, payroll) | **Generalised audit log** |
| X2 | Admin UI for users/roles + a supplier/item master | **Master-data administration** |
| X3 | Cross-module dashboards (finance, stock, HR rolled up) | **Consolidated reporting/BI** |

---

## 3.2 Right-sizing principles (the anti-over-engineering charter)

These rules are the academic and engineering heart of the proposal: they make the result a
*real* ERP while explicitly refusing enterprise complexity that a 5–8-person firm cannot
sustain. They extend the existing project's "What NOT to Build" stance.

| Principle | We DO | We DON'T (and why) |
|---|---|---|
| **P1 — Simplified finance** | A categorised **single-entry+ ledger** (income/expense with categories, references, receivable/payable status) that yields a monthly P&L | ❌ Double-entry GL with debit/credit journals & chart of accounts — needs a bookkeeper; over-engineered for the owner to operate |
| **P2 — Light manufacturing** | Keep the existing `BulkProduction` status/deadline tracker | ❌ MRP, multi-level BOM, demand forecasting, shop-floor routing — irrelevant for made-to-order trims |
| **P3 — Simple inventory** | Single stock location, item + movement ledger, reorder level | ❌ Multi-warehouse, bin/location management, lot/serial tracking |
| **P4 — Lightweight procurement** | A simple Purchase Order + Goods-Receipt that raises stock and a payable | ❌ Tendering, multi-level approval chains, RFQ workflows |
| **P5 — One integrated monolith** | Extend the single Next.js app + one Postgres DB; reuse existing conventions | ❌ Microservices, separate finance service, message queues, GraphQL, Redis |
| **P6 — Reuse before invent** | Generalise `CashEntry`/`CostType`, `TimelineEntry` audit, `Attachment`, soft-delete, `Decimal(12,2)` | ❌ Parallel new subsystems that duplicate what exists |
| **P7 — Module-at-a-time value** | Each module ships independently and is useful alone | ❌ Big-bang cutover |
| **P8 — Operable by non-experts** | Forms and language a non-programmer owner can run (the existing mockups already do this) | ❌ Jargon-heavy accounting/HR UIs |

> **Design test for every proposed feature:** *"Does this remove a manual burden the owner
> feels today, and can a non-technical staff member operate it?"* If not, it is deferred or
> dropped.

---

## 3.3 MoSCoW prioritisation

Prioritised against business pain (from the SRS and the owner's mockups) and the
right-sizing charter.

### MUST — required to legitimately call it an ERP
- **M1 Accounting module** (G3): generalise the Cash Book into income/expense + P&L +
  **receivables (AR)** tied to PIs. *Rationale:* "who owes me / what did I make this
  month" is the owner's sharpest unanswered question, and AR is the natural extension of
  the order→PI→LC chain already built.
- **M2 Inventory + Suppliers** (G1+G2 core): item master, stock-in/out movements,
  reorder alerts, supplier master. *Rationale:* enables material costing against orders
  and closes the "what do I have in stock" gap.
- **M3 Generalised audit + master-data admin** (X1+X2): so finance and stock changes are
  traceable — non-negotiable once money and stock are in the system.

### SHOULD — strong value, expected of an ERP
- **S1 Procurement** (G2 full): Purchase Orders + Goods Receipt that post to stock and AP.
- **S2 HR & Payroll** (G4): employee master, monthly payroll posting a Salary expense to
  Accounting, leave tracking.
- **S3 Consolidated reporting/BI** (X3): finance + stock + order dashboards.

### COULD — useful, owner-requested, not core to "ERP-ness"
- **C1 Fleet** (G5): vehicles, drivers, trips/fuel, maintenance — posts Transport expense
  to Accounting.
- **C2 Customer 360 / receivable-aware buyer page** (CRM polish).

### WON'T (this phase) — explicitly out of scope
- Double-entry GL, MRP/BOM, multi-warehouse, tax filing/VAT return automation, bank/ERP
  integrations, e-commerce, the AI/WhatsApp "Future Vision" features (tracked separately in
  `09-future-vision.html`).

---

## 3.4 The minimum ERP — definition of "done"

IKON is a **minimum ERP** when the MUST set (+ enough of SHOULD) is live such that:

1. **One database captures every core transaction** — orders, stock, money, and people.
2. **Flows cross-link automatically:**
   - Stock issue → consumes inventory **and** posts a material cost to the order **and**
     to the expense ledger.
   - Goods receipt → raises stock **and** a payable.
   - PI issued → creates a receivable; payment received → clears it.
   - Payroll run → posts a salary expense; fuel log → posts a transport expense.
3. **The owner can answer, from the system:** *What stock do I have and what needs
   reordering? Who owes me and how overdue? What did this order cost and did it make money?
   What did I earn and spend this month? Who did I pay in salary?*

That is the bar. It is reached by **activating the four mocked modules on the existing
integrated core** — not by rebuilding anything.

---

## 3.5 Why this is genuinely an ERP (and not just "more features")

The transformation satisfies the chapter-01 definition on all three counts:

- **Single source of truth** — already true; preserved by extending one schema.
- **Process integration** — newly achieved by the cross-links in §3.4, seeded by the
  existing `CashEntry` job-costing pattern.
- **Common data & security model** — achieved by X1/X2 (shared audit, shared roles, shared
  partner/item masters).

The result is a small, coherent, *integrated* ERP — exactly the shape the SME literature
(chapter 01) prescribes for a firm of this size.
