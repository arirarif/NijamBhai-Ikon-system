# 09 — Open Decisions & References

Two things a reviewer needs: the **decisions still to be made** before building (so the plan
is honest about what isn't settled), and the **sources** behind the ERP framing.

---

## 9.1 ERP-transformation decision register

ADR-style. Each needs a yes/no from the product owner before the relevant phase. A
*recommendation* is given for each.

| ID | Decision | Options | Recommendation | Affects |
|---|---|---|---|---|
| **DE-1** | Generalise `CashEntry` into `LedgerEntry`, or keep Cash Book and add a separate ledger? | (a) Evolve CashEntry (b) New parallel table | **(a) Evolve** — CashEntry already has direction/amount/category/order-link/cost-type; one ledger avoids reconciliation | E1 Accounting |
| **DE-2** | Receivables: a dedicated `Receivable` table, or `PI` + `Payment[]`? | (a) New table (b) Payments on PIs | **(b)** — PIs are the source of truth; attach payments; aging computed | E1 |
| **DE-3** | Finance depth | (a) Categorised single-entry+ (b) Full double-entry GL | **(a)** — operable by the owner; double-entry is over-engineered (P1) | E1 |
| **DE-4** | `Employee` vs `User` | (a) Separate, optional link (b) One table | **(a) Separate** — most staff don't log in; merchandisers are buyer-side, not staff | E4 HR |
| **DE-5** | `Driver` as its own table or an `Employee(department=DRIVER)`? | (a) Employee + driver fields (b) Separate Driver | **(a)** — avoids duplicate person records | E5 Fleet |
| **DE-6** | Stock on-hand: derived from movements, or a stored column? | (a) Derived (b) Stored (c) Both (cache) | **(c)** — derive for truth, cache `onHand` for fast lists, recompute on write | E2 |
| **DE-7** | Is **Fleet** in scope for the minimum ERP, or deferred? | (a) Build (C1) (b) Defer | Owner's call — not required for "ERP-ness"; build if the vehicle-cost pain is real | E5 |
| **DE-8** | Legacy data import (existing project D-06) | (a) Import opening balances/employees/stock (b) Start fresh | **Hybrid** — import masters (items, employees, opening stock), start transactions fresh | Rollout |
| **DE-9** | Procurement depth | (a) PO + GRN only (b) + approvals/RFQ | **(a)** — approvals are over-engineering at 5–8 staff (P4) | E3 |
| **DE-10** | Fiscal year handling | Apr–Mar (per mockup) vs calendar | **Apr–Mar** — matches the Accounts mockup and BD norms | E1, E6 |
| **DE-11** | Audit log: generalise `TimelineEntry` or add a separate `AuditLog`? | (a) Extend Timeline (b) New AuditLog | **(b) New `AuditLog`** for non-order entities; keep `TimelineEntry` for the order story | E0 |

These also intersect with the existing project's still-open decisions **D-06** (data
import), **D-07** (vendor/outsource screen — note: *outsource vendors* differ from
*suppliers*; the ERP adds Suppliers, leaving D-07 about sample-maker vendors still open),
and **D-10** (alerts scope — relevant to reorder/expiry/receivable alerts).

---

## 9.2 Scope boundary (recorded for the reviewer)

**In scope (minimum ERP):** Accounting, Inventory + Suppliers, Procurement, HR & Payroll,
Fleet (optional), cross-cutting audit/master-data/reporting — all on the existing modular
monolith.

**Explicitly out of scope:** double-entry GL, MRP/BOM/forecasting, multi-warehouse, tax/VAT
return automation, banking/accounting-software integration, e-commerce, and the AI/WhatsApp
"Future Vision" automation layer (tracked in `03-mockups/v2/09-future-vision.html`).

---

## 9.3 References

Background sources for the ERP framing in chapter 01. (Standard works; cite per your
programme's required style.)

1. Davenport, T. H. (1998). *Putting the Enterprise into the Enterprise System.* Harvard
   Business Review, 76(4), 121–131.
2. Klaus, H., Rosemann, M., & Gable, G. G. (2000). *What is ERP?* Information Systems
   Frontiers, 2(2), 141–162.
3. Monk, E., & Wagner, B. (2013). *Concepts in Enterprise Resource Planning* (4th ed.).
   Cengage Learning.
4. Snider, B., da Silveira, G. J. C., & Balakrishnan, J. (2009). *ERP implementation at SMEs:
   analysis of five Canadian cases.* International Journal of Operations & Production
   Management, 29(1), 4–29.
5. Haddara, M., & Zach, O. (2011). *ERP Systems in SMEs: A Literature Review.* Proceedings of
   the 44th Hawaii International Conference on System Sciences (HICSS).
6. Esteves, J. (2009). *A benefits realisation road-map framework for ERP usage in small and
   medium-sized enterprises.* Journal of Enterprise Information Management, 22(1/2), 25–35.
7. Federici, T. (2009). *Factors influencing ERP outcomes in SMEs: a post-introduction
   assessment.* Journal of Enterprise Information Management, 22(1/2), 81–98.

### Internal project sources (primary evidence)
- `01-strategy/01-master-plan.md`, `01-strategy/02-screens.md`, `01-strategy/03-todo.md`
- `02-decisions/01-open-decisions.md`
- `06-docs/03-tech-stack.md` (authoritative stack ADRs), `06-docs/04-SRS.md`,
  `06-docs/11-operations-maintenance.md`
- Mockups: `03-mockups/v2/10-inventory.html`, `11-accounts.html`, `12-hr-payroll.html`,
  `13-vehicles.html`, `09-future-vision.html`
- Code: `ikon-app/prisma/schema.prisma` (current 13-entity data model) and the built
  `app/(dashboard)/*` routes.

---

## 9.4 Next step

This dossier is **analysis only — no code has been written.** Recommended path: the product
owner reviews and resolves the DE-1…DE-11 decisions, confirms whether Fleet is in scope
(DE-7), then the build proceeds phase-by-phase per
[`06-roadmap-and-phasing.md`](06-roadmap-and-phasing.md), starting with **E0 (foundation)**
and **E1 (Accounting)**.
