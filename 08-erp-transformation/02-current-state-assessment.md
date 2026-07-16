# 02 — Current-State Assessment

This chapter measures what the *ikon-app* does **today** against the canonical ERP module
map from chapter 01. It is evidence-based: every claim maps to a built route, an API
handler, or a Prisma model in the existing codebase.

---

## 2.1 What is already built

The application (`ikon-app/`, a Next.js 15 + Prisma 7 + PostgreSQL modular monolith) ships
these working modules:

| Built module | Route(s) | Backing data |
|---|---|---|
| Dashboard | `/dashboard` | aggregates across orders |
| Companies & Merchandisers | `/companies` | `Company`, `Merchandiser` |
| Orders (pipeline) | `/orders`, `/orders/new`, `/orders/[id]`, `/orders/samples` | `Order`, `SampleRevision`, `BulkProduction`, `TimelineEntry`, `Attachment` |
| Export documents | `/documents/pi`, `/documents/lc`, `/documents/challan` | `PI`, `LCRecord`, `Challan` |
| Cash Book | `/cash` | `CashEntry` (incl. per-order job costing) |
| Reports | `/reports` | aggregates |
| Settings | `/settings` | `SystemSettings` |
| Auth | `/login` | `User`, NextAuth v5 |

Cross-cutting strengths already in place: server-side role checks on every mutation,
Zod validation at every boundary, an order-scoped audit trail (`TimelineEntry` with user
attribution), Puppeteer-generated PDF documents, a tuned Postgres connection pool,
automated daily backups, and a CI pipeline. (See the production-readiness work in the
parent project for detail.)

---

## 2.2 Current data model (13 entities)

| Entity | Role | Notable fields |
|---|---|---|
| `User` | Internal login identity + audit actor | `role` (OWNER/MANAGER/STAFF/VIEWER), `active` |
| `Company` | **Buyer** firm | `country`, contact info, `active` |
| `Merchandiser` | Buyer-side contact | `whatsapp`, `designation`, FK→Company |
| `Order` | Pipeline spine | `orderNo` `F-YYYY-NNN`, `stage` (10-stage enum), `priority`, `quantity/unit` |
| `SampleRevision` | Sample iteration | `revisionNo`, `type` (in-house/outsourced), `result` |
| `BulkProduction` | Production tracking (1:1 order) | `deadline`, `completionPct`, `status` |
| `Challan` | Delivery note (1:1) | `challanNo`, `items` (JSON) |
| `PI` | Proforma invoice (1:1) | `piNo`, `lineItems` (JSON), `totalAmount` Decimal, `finalized` |
| `LCRecord` | Letter of credit (1:1) | `lcNo`, `openDate`/`maturityDate`, doc-checklist booleans |
| `TimelineEntry` | Per-order activity log | `action`, `detail`, FK→User |
| `Attachment` | File uploads | polymorphic (order or revision) |
| `CashEntry` | Daily cash + **job costing** | `direction` (IN/OUT), `amount` Decimal, `category`, `costType` (MATERIALS/MANPOWER/SAMPLE/MISC), optional FK→Order |
| `SystemSettings` | Singleton config | company/bank/PI-terms |

**The integration backbone already exists.** Two facts matter most for the ERP argument:

1. **One shared database** with a central `Order` entity that PI, LC, Challan, samples,
   production, timeline, and cash all reference.
2. **`CashEntry` already crosses modules** — it is simultaneously a cash ledger *and* an
   order-cost record (`costType` + optional `orderId`). This is, in miniature, exactly the
   stock↔cost↔order↔ledger propagation that defines an ERP. The new modules extend this
   pattern rather than invent it.

---

## 2.3 Capability matrix — IKON today vs the ERP module map

Legend: ✅ built · 🟡 partial · 🔴 absent · ⚪ not needed at this scale

| ERP module | IKON status | Evidence / note |
|---|---|---|
| **Sales / Order Management (order-to-cash)** | ✅ | Full 10-stage pipeline, the product's core strength |
| **Export documentation** (PI/LC/Challan) | ✅ | Puppeteer PDF; unusually strong for firm size |
| **CRM — customers (buyers)** | 🟡 | `Company` + `Merchandiser` exist; no 360° view, no receivable-aware customer page |
| **CRM / Master data — suppliers** | 🔴 | No `Supplier` entity at all (a free-text field only) |
| **Inventory / Materials Management** | 🔴 | Mocked (`10-inventory.html`); no model/route |
| **Procurement (procure-to-pay)** | 🔴 | No purchase orders, no goods receipt |
| **Production / Manufacturing** | 🟡 | `BulkProduction` tracks status/deadline/% — right depth; no material consumption link |
| **Financial Accounting — cash/bank** | 🟡 | `CashEntry` cash book exists |
| **Financial Accounting — receivables (AR)** | 🔴 | No invoice-payment/aging tracking (mocked in `11-accounts.html`) |
| **Financial Accounting — payables (AP)** | 🔴 | No supplier-bill tracking |
| **Financial Accounting — P&L / expense ledger** | 🔴 | No categorised income/expense, no monthly profit (mocked) |
| **Cost accounting / controlling** | 🟡 | `CashEntry.costType` gives per-order costing seed; not surfaced as reports |
| **HR & Payroll** | 🔴 | Mocked (`12-hr-payroll.html`); no model/route |
| **Asset / Fleet management** | 🔴 | Mocked (`13-vehicles.html`); no model/route |
| **Reporting / BI** | 🟡 | `/reports` exists but limited to order aggregates |
| **User / role administration** | 🟡 | Roles enforced in code; no admin UI to manage users |
| **Audit trail** | 🟡 | Strong for **orders** (`TimelineEntry`); absent for cash, master data, future modules |
| **Document management** | 🟡 | `Attachment` model + generated PDFs; no central document hub |

---

## 2.4 Reading the matrix

Three patterns stand out:

1. **The order-to-cash spine is genuinely complete** — sales, sampling, production
   tracking, and export documents are built to a depth most small firms never reach. IKON
   does not need work here to "become an ERP"; it needs the surrounding modules.

2. **The missing pieces are exactly the four disabled-but-mocked modules** — Inventory
   (+ Suppliers/Procurement), Accounts (AR/AP/P&L), HR & Payroll, and Fleet. They are
   *designed already* (the owner produced detailed mockups in `03-mockups/v2/`), which
   means scope is understood and risk is low.

3. **The cross-cutting layer is half-built** — audit, master-data administration, and
   consolidated reporting are strong for orders but must be generalised so the new modules
   inherit them rather than each re-inventing them.

The next chapter turns this matrix into a prioritised gap list and the right-sizing rules
that keep the build appropriate for a five-to-eight-person company.
