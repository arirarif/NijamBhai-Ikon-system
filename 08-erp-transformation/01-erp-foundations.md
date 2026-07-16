# 01 — ERP Foundations (Research Background)

This chapter establishes the conceptual ground: what an ERP system *is*, what its
canonical modules are, how the literature treats ERP for small and medium enterprises
(SMEs), and how those ideas apply to a garment-accessories micro-enterprise. It frames
the design decisions taken in later chapters.

---

## 1.1 What is an ERP system?

Enterprise Resource Planning (ERP) software integrates an organisation's core business
processes — sales, procurement, inventory, production, finance, and human resources —
into **one system built on a single shared database**, so that data entered once in one
process is available, consistently, to every other process (Davenport, 1998; Klaus,
Rosemann & Gable, 2000).

Three properties distinguish an ERP from a collection of separate business apps:

1. **Single source of truth.** One database; no re-keying between systems; no
   reconciliation between a "sales spreadsheet" and an "accounts spreadsheet."
2. **Process integration.** A transaction in one module *propagates* to others. The
   textbook example: receiving stock simultaneously raises inventory, records a payable
   to the supplier, and (later) lets that material be costed against a production order.
3. **A common data and security model.** Shared master data (partners, items, users),
   shared roles/permissions, and a shared audit trail.

The corollary — and the thesis of this dossier — is that **integration, not the number
of features, is what makes software an ERP.** A small system with five modules that share
one database and post to one another is *more* of an ERP than a large system of ten
disconnected apps.

---

## 1.2 The canonical ERP module map

Classic ERP references (e.g. the SAP/Oracle functional decomposition; Monk & Wagner,
2013) group functionality into a recurring set of modules:

| ERP module | Core purpose |
|---|---|
| **Sales & Distribution / Order Management** | Quote → order → deliver → invoice (order-to-cash) |
| **Materials Management — Inventory** | Stock levels, valuation, movements, reorder |
| **Materials Management — Procurement** | Suppliers, purchase orders, goods receipt (procure-to-pay) |
| **Production / Manufacturing** | Convert materials to finished goods; track progress |
| **Financial Accounting** | General ledger, receivables (AR), payables (AP), bank/cash |
| **Controlling / Cost Accounting** | Cost per order/job/cost-centre, profitability |
| **Human Resources & Payroll** | Employee master, attendance/leave, salary |
| **Asset Management** | Fixed assets / fleet / equipment, maintenance |
| **Reporting / Business Intelligence** | Cross-module dashboards and analytics |
| **Master Data & Basis (cross-cutting)** | Partners, items, users, roles, audit, documents |

Not every business needs every module, and the *depth* of each varies enormously with
size. This map is a **menu, not a mandate** — §1.4 and chapter 03 select the subset that
is genuinely required for IKON.

---

## 1.3 ERP for SMEs and micro-enterprises

The ERP literature repeatedly warns that **SME ERP failure is usually caused by adopting
enterprise-scale complexity that the organisation cannot absorb** — long implementations,
heavy customisation, and modules nobody uses (Snider, da Silveira & Balakrishnan, 2009;
Haddara & Zach, 2011). The recommendations that emerge for small organisations are
consistent:

- **Scope to the pain, not to the product.** Implement only modules that remove a real,
  current manual burden.
- **Prefer simplicity over accounting/operational "correctness" that the staff can't
  operate.** A categorised single-entry ledger that a non-accountant can run beats a
  double-entry GL that needs a bookkeeper.
- **One integrated system over best-of-breed.** A micro-enterprise cannot maintain
  interfaces between separate tools; a modular monolith on one database is the right
  shape.
- **Incremental rollout.** Add one module at a time, each delivering value on its own.

These principles are not a compromise; for a five-to-eight-person firm they are the
*correct* engineering. They directly justify the right-sizing rules in chapter 03.

---

## 1.4 The garment-accessories context

IKON is **not** a garment manufacturer; it is a **supplier of accessories/trims**
(buttons, zippers, woven and printed labels, elastics, threads, hang-tags) to garment
buyers and factories. This shapes which ERP modules matter:

- **Order-to-cash is the spine.** The business is defined by buyer orders moving through
  sampling → bulk → export documentation → LC payment. (IKON already automates this.)
- **Light manufacturing, not full MRP.** Production is "make the approved trim in bulk to
  a deadline." There is **no** need for multi-level Bills of Materials, demand
  forecasting, or shop-floor routing. A simple production-status tracker (which IKON has)
  suffices.
- **Inventory is raw-material + simple finished goods**, single location, reorder-level
  driven — not multi-warehouse bin management.
- **Procurement is lightweight**: a handful of trusted suppliers, simple purchase orders
  and goods receipts; no tendering/approval hierarchies.
- **Finance centres on cash, receivables, and LC maturities** — exactly the pressure
  points the owner already feels — plus categorised expenses (salary, purchase, rent,
  transport) to produce a monthly P&L.
- **Export-documentation rigor is unusually high** for a firm this size (PI, LC pack,
  challan), because the buyers and banks demand it. IKON's document-generation strength
  is a genuine differentiator and is already built.

The garments-trade specifics (LC 60/90-day terms, merchandiser-driven sampling loops,
outsourced sample makers in Mirpur/Gilistan) mean a generic off-the-shelf ERP would fit
poorly — which is the practical motivation for a **bespoke, right-sized ERP** and the
research interest of this case.

---

## 1.5 Working definition for this dossier

> **A "minimum ERP" for IKON** = the existing order-to-cash core **plus** the smallest set
> of integrated modules (Inventory + Procurement, Accounting, HR & Payroll, and — by owner
> preference — Fleet) such that (a) all core business transactions are captured in one
> database, (b) money and material flows cross-link automatically (stock ↔ cost ↔ order ↔
> ledger), and (c) the owner can answer "what do I have, who owes me, what did it cost,
> and what did I make this month?" from the system rather than from notebooks.

Chapters 02–03 measure IKON against this definition; chapters 04–06 design and sequence
the build.

*(Full citations in [`09-open-decisions-and-references.md`](09-open-decisions-and-references.md).)*
