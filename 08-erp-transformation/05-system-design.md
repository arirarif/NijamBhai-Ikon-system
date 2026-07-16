# 05 — System Design

This chapter is the technical design: the architecture the ERP modules live in, the
**data-model extensions** that fit the existing schema, the **key design decisions** that
need sign-off, how **cross-module posting** works without heavy infrastructure, and the
security model. It is written to be cross-checked before implementation.

---

## 5.1 Architectural stance: a modular monolith

The ERP stays **one Next.js 15 application on one PostgreSQL database** — a *modular
monolith*. This is a decision, not a default; it follows the right-sizing charter (P5) and
the existing tech-stack ADRs ("no microservices, no queues, no GraphQL, no Redis").

```
ikon-app/  (single deployable)
├─ app/(dashboard)/
│   ├─ [existing] dashboard, companies, orders, documents, cash, reports, settings
│   └─ [new]      inventory, procurement, accounting, hr, fleet, admin
├─ app/api/        REST handlers per module (existing pattern)
├─ lib/
│   ├─ db.ts                 one Prisma client (existing)
│   ├─ validations/*         Zod schemas per module (existing pattern)
│   ├─ posting/*   [new]     cross-module posting services (see §5.4)
│   └─ pdf/                  Puppeteer doc generation (existing)
└─ prisma/schema.prisma      ONE schema, extended (see §5.3)
```

Each module is a **folder boundary**, not a network boundary. Modules call each other
through **typed service functions in `lib/`**, inside database transactions — never over
HTTP. This gives modularity (clear seams, independently buildable) without distributed-
systems cost.

**Why this scales to a 10-year, 5–8-user horizon.** At this transaction volume a single
Postgres comfortably serves all modules; the bottleneck is developer maintainability, which
a one-language monolith optimises. The design leaves obvious seams (the `lib/posting`
services) so that *if* a module ever needed to split out, it could — but it won't need to.

---

## 5.2 Conventions inherited by every new entity

To keep the schema coherent, all new models follow the existing house style (observed in
`prisma/schema.prisma`):

- `cuid()` string primary keys; `@@map` to **snake_case plural** table names.
- Money as `Decimal @db.Decimal(12,2)` — **never float**.
- `active Boolean @default(true)` soft-delete on master entities (orders use
  `cancelledAt`/`cancelReason`).
- `createdAt` / `updatedAt` timestamps; actor links via `createdById` → `User`.
- Enums for fixed vocabularies; `Json` only for genuinely variable line-item payloads.
- Index every hot filter/sort/FK column.
- Cross-links via optional FKs (the `CashEntry.orderId` pattern).

---

## 5.3 Data-model extensions (new entities)

Described at field level (not as code). Grouped by module. Relationships and the key
"reuse vs new" decisions are flagged.

### Inventory & Procurement
| Entity | Key fields | Relations |
|---|---|---|
| `Supplier` | name, phone, location, `category`, `active`, timestamps | → `InventoryItem[]`, `PurchaseOrder[]`, `StockMovement[]` |
| `InventoryItem` | name, `sku` @unique, `category` (enum), `unit` (enum, extends `Unit`), `minStockLevel` Int, `unitCost` Decimal, `active` | → `Supplier` (default), `StockMovement[]` |
| `StockMovement` | `direction` (IN/OUT/ADJUST), `quantity` Int, `unitCost` Decimal, `value` Decimal, `date`, `reference?`, note | → `InventoryItem`, `Supplier?`, `Order?`, `createdBy User?` |
| `PurchaseOrder` | `poNo` @unique, `status` (enum), `lines` Json, `total` Decimal, `date`, note | → `Supplier`, `GoodsReceipt?` |
| `GoodsReceipt` | `receiptDate`, `lines` Json | → `PurchaseOrder?`, generates `StockMovement[]` + `Payable` |

> On-hand quantity is **derived** by summing `StockMovement` (auditable), optionally
> snapshotted to a cached `onHand` column for fast lists (recomputed on write).

### Accounting
| Entity | Key fields | Relations |
|---|---|---|
| `LedgerEntry` *(evolved `CashEntry`)* | `type` (INCOME/EXPENSE), `status` (SETTLED/PENDING), `category` (enum), `amount` Decimal, `reference?`, `description?`, `source` (enum), `costType?` | → `Company?`, `Order?`, `PI?`, `createdBy User?` |
| `Payment` | `amount` Decimal, `date`, `method`, note | → `PI` (receivable) **or** `Payable` |
| `Payable` | `amount` Decimal, `dueDate`, `status` (OPEN/PARTIAL/PAID) | → `Supplier`, `GoodsReceipt?` |

> **Receivables** are computed from finalized `PI` + its `Payment[]` (aging = today −
> `PI.date`/terms). A separate `Receivable` table is *not* required — keep PIs as the source
> of truth and attach payments (simpler, fewer moving parts).

### HR & Payroll
| Entity | Key fields | Relations |
|---|---|---|
| `Employee` | name, designation, `department` (enum), `joinDate`, `monthlySalary` Decimal, phone, `nationalId`, `paymentMode` (enum), `bankAccount?`, `status`, `active` | → `User?` (optional login link), `SalaryPayment[]`, `LeaveRequest[]` |
| `SalaryPayment` | `period` (YYYY-MM), `gross` Decimal, `deduction` Decimal, `net` Decimal, `paymentMode`, `status` (PAID/PENDING/ADVANCE), `paymentDate?` | → `Employee`, posts `LedgerEntry` |
| `LeaveRequest` | `type`, `startDate`, `endDate`, `days` Int, reason, `status` | → `Employee` |

### Fleet
| Entity | Key fields | Relations |
|---|---|---|
| `Vehicle` | `regNo` @unique, make, model, year, color, `type`, `status`, `insuranceExpiry`, `fitnessExpiry`, `odometer` | → `Driver?` (assigned), `Trip[]`, `MaintenanceRecord[]` |
| `Trip` | `date`, from, to, purpose, `distanceKm` Int, `fuelCost` Decimal, note | → `Vehicle`, `Driver`, `Order?`, posts `LedgerEntry` |
| `MaintenanceRecord` | `date`, workDone, workshop, `cost` Decimal, `nextDue?` | → `Vehicle`, posts `LedgerEntry` |

> **Driver** is modelled as an `Employee` with `department = DRIVER` plus driver-specific
> fields (`licenseNo`, `licenseExpiry`) — avoids a duplicate person table. (Decision D-E3.)

### Cross-cutting
| Entity | Key fields | Relations |
|---|---|---|
| `AuditLog` *(generalised `TimelineEntry`)* | `entityType`, `entityId`, `action`, `before` Json?, `after` Json?, `createdAt` | → `User?` |

New enums: `InventoryCategory`, `POStatus`, `LedgerType`, `LedgerStatus`, `IncomeCategory`,
`ExpenseCategory`, `LedgerSource`, `Department`, `PaymentMode`, `SalaryStatus`,
`LeaveType`/`LeaveStatus`, `VehicleType`, `VehicleStatus`. `Unit` extends with CONES,
SHEETS, KG.

---

## 5.4 Cross-module posting (how the integration actually works)

The ERP property — a transaction in one module updating another — is implemented with
**posting services**, not a message queue.

- Each cross-effect is a function in `lib/posting/` (e.g. `postMaterialIssue`,
  `postGoodsReceipt`, `postSalary`, `postVehicleExpense`).
- The triggering action and its posting run **in a single `prisma.$transaction`**, so they
  commit together or not at all (the discipline already used in the order pipeline).
- Every posting writes an `AuditLog` row.

Example — *Stock-Out against an order*:
```
$transaction:
  1. StockMovement{direction:OUT, item, qty, orderId}        // inventory
  2. LedgerEntry{type:EXPENSE, category:PURCHASE-consumption,  // accounting + job cost
                 costType:MATERIALS, orderId, source:STOCK}
  3. AuditLog{entityType:'StockMovement', action:'issue', ...} // audit
  (recompute item.onHand)
```

This keeps integration **synchronous, transactional, and debuggable** — appropriate for the
scale, and avoiding the eventual-consistency complexity of queues (P5).

---

## 5.5 Security & roles

Reuse the existing model (already strong): NextAuth session + `requireRole` on every
mutation, enforced server-side. Extend the role matrix for the new, money-sensitive
modules:

| Capability | OWNER | MANAGER | STAFF | VIEWER |
|---|:--:|:--:|:--:|:--:|
| Orders / samples / production | ✓ | ✓ | ✓ | read |
| Inventory in/out | ✓ | ✓ | ✓ | read |
| Procurement (PO/GRN) | ✓ | ✓ | – | read |
| **Accounting (ledger, AR/AP, P&L)** | ✓ | ✓ | – | read |
| **HR & Payroll** | ✓ | – | – | – |
| Fleet | ✓ | ✓ | ✓ | read |
| User/role admin | ✓ | – | – | – |

Payroll and user administration are **OWNER-only** (matches the mockups). Object-level
scoping remains **N/A** — IKON is single-tenant, internal, login-only (no public signup).

---

## 5.6 Non-functional design notes

- **Audit everywhere money or stock moves** — enforced by routing all writes through the
  posting services (§5.4).
- **Pagination** on every new list (inventory, ledger, payroll history) from day one — these
  grow unbounded over a 10-year life. (A current gap in existing lists; fix forward.)
- **Reporting** reads from the same tables via Prisma aggregations (no separate analytics
  store, no warehouse — P5).
- **Documents** (salary slip, PO, stock report) reuse the existing Puppeteer pipeline.
- **Migrations** continue via `prisma migrate`, run as a release step (already configured in
  `railway.json`).

---

## 5.7 What this design deliberately omits

To keep the record explicit (and defensible to a reviewer): **no** double-entry GL/chart of
accounts, **no** MRP/BOM/forecasting, **no** multi-warehouse/bin/lot/serial, **no**
procurement approval hierarchy, **no** microservices/queues/Redis/GraphQL, **no** separate
analytics database. Each omission is justified by scale in §3.2 and is reversible later if
the business genuinely outgrows it.
