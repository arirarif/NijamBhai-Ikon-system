# IKON → ERP Transformation — Research & Planning Dossier

**Subject:** Designing a right-sized Enterprise Resource Planning (ERP) system for a micro-enterprise garment-accessories supplier
**Case organisation:** IKON Garments Accessories, Uttara, Dhaka-1230 (owner: Muhammad Nezam Uddin; ~5–8 staff)
**Author:** Md Arif (stackcraft) · **Status:** Planning / research draft · **Code changes:** none (analysis only)

---

## Abstract

IKON Garments Accessories runs an order-driven trims-and-accessories business whose
operations software (the *ikon-app*) currently automates the **order-to-cash pipeline**
— buyers, merchandisers, the 10-stage order lifecycle, export documents (Challan / PI /
LC), and a daily cash book. This dossier asks a focused research question:

> **What is the *minimum* set of additional, integrated modules that turns this
> order-management application into a genuine — if small — ERP system, without
> over-engineering it for a five-to-eight-person company?**

The central argument is that **an ERP is defined by integration, not by feature count**:
a single shared database in which a transaction in one module (e.g. a stock issue)
automatically propagates to others (job cost in accounting, consumption against an
order). IKON already possesses this integration backbone. The transformation is therefore
not a rebuild but the **incremental activation of four already-envisioned modules**
— Inventory & Procurement, Accounting, HR & Payroll, and Fleet — on top of the existing
integrated core, plus the cross-cutting concerns (master data, audit, reporting) that
bind them.

This dossier is a **plan and a design**, written to be cross-checked before any code is
written. It deliberately resists "big-ERP" patterns (double-entry GL, MRP/BOM, warehouse
bins, procurement approval chains, microservices) that would be inappropriate at this
scale.

---

## How to read this dossier

The documents are ordered to be read in sequence, but each stands alone.

| # | Document | What it answers |
|---|---|---|
| 00 | **This file** | Why this exists, how to read it, the glossary |
| 01 | [`01-erp-foundations.md`](01-erp-foundations.md) | What an ERP *is* (research background, module taxonomy, ERP-for-SMEs, the garments context) |
| 02 | [`02-current-state-assessment.md`](02-current-state-assessment.md) | What IKON has **today**, mapped onto ERP modules (capability matrix + current data model) |
| 03 | [`03-gap-analysis.md`](03-gap-analysis.md) | The **gap** to a minimum ERP; what's missing; MoSCoW prioritisation; the right-sizing principles |
| 04 | [`04-target-modules-spec.md`](04-target-modules-spec.md) | Specification of each module to add (purpose, entities, workflows, integration, value) |
| 05 | [`05-system-design.md`](05-system-design.md) | Architecture + **data-model extensions** that fit the existing schema; key design decisions |
| 06 | [`06-roadmap-and-phasing.md`](06-roadmap-and-phasing.md) | Phased delivery plan, sequencing, effort sizing, milestones |
| 07 | [`07-business-case.md`](07-business-case.md) | Benefit per module, ROI narrative, cost, risk, success metrics |
| 08 | [`08-engineering-workflow-and-test-strategy.md`](08-engineering-workflow-and-test-strategy.md) | Team roles, git-worktree dev workflow, test strategy, quality gates, definition of done |
| 09 | [`09-open-decisions-and-references.md`](09-open-decisions-and-references.md) | ERP-specific decision register (ADRs to resolve) + bibliography |

**Reading paths:**
- *Professor / reviewer:* 00 → 01 → 03 → 05 → 06 (the argument and the design).
- *Owner / business:* 00 → 02 → 03 → 07 (what we have, what's missing, what it's worth).
- *Engineer:* 02 → 04 → 05 → 08 (what to build and how).

---

## Glossary (IKON terms used throughout)

These match the existing project docs and code so the dossier is consistent with them.

| Term | Meaning |
|---|---|
| **Order** | One job/style tracked through the pipeline; numbered `F-YYYY-NNN`. |
| **Style** | The buyer's product code/name for the item (e.g. `MBJA W26 DENIM-06`). |
| **Company** | A **buyer** firm (customer), e.g. RIO Design, Atlas Group. |
| **Merchandiser** | The **buyer-side** representative who places orders and approves samples. *Not* IKON staff. |
| **Employee** | **IKON internal staff** (HR module). A separate concept from Merchandiser. |
| **Supplier** | A **raw-material vendor** (buttons, zippers, thread). Distinct from *Company* (buyer). |
| **Vendor / Outsource** | External **sample/production makers** (Mirpur, Gilistan). Distinct from Supplier. |
| **Sample / Revision** | One round of a physical sample + buyer feedback; orders run 3–10+ revisions. |
| **Bulk Production** | Full-scale production after sample approval. |
| **Challan** | Delivery challan (dispatch note); numbered `CH-YYYY-NNN`. |
| **PI** | Proforma Invoice; numbered `PI-YYYY/NN`. |
| **LC** | Letter of Credit; matures at `openDate + 90 days`. |
| **Cash Book / CashEntry** | The existing daily money-in/out ledger; also does per-order job costing via `CostType`. |
| **Pipeline** | The 10-stage order lifecycle (Order Received → … → Matured). |
| **Roles** | `OWNER`, `MANAGER`, `STAFF`, `VIEWER` (+ a future Vendor portal). |

> **Source of truth note.** Where existing project docs disagree (the SRS Appendix A still
> suggests a Python/FastAPI stack), this dossier follows the **authoritative** decisions in
> `06-docs/03-tech-stack.md`: a single-language TypeScript / Next.js 15 / Prisma 7 /
> PostgreSQL / NextAuth modular monolith, designed for a 10-year run at ~$20–30/month.
