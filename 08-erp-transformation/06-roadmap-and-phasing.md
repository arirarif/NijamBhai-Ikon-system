# 06 — Roadmap & Phasing

A phased plan to deliver the minimum ERP **module-at-a-time** (charter P7), each phase
shipping independent value. Effort is in **ideal developer-days** for one developer working
part-time — relative sizing for planning, not a commitment. The sequence follows
dependency order: cross-cutting foundation → finance → materials → people → assets →
consolidation.

> Naming note: these ERP phases continue the existing project's roadmap, which has reached
> "Phase 3 — foundation/core build." Treat the work below as **Phase 5 (ERP expansion)**,
> after the core pipeline modules are finished and the pre-deploy hardening (separate doc)
> is done.

---

## Phasing overview

| Phase | Module(s) | MoSCoW | Depends on | Est. days | Ships value |
|---|---|---|---|---|---|
| **E0** | Foundation: generalised `AuditLog`, `lib/posting` scaffold, pagination helper, role-matrix update | M3 | — | 3–4 | Traceability + the integration seam everything else uses |
| **E1** | **Accounting** (ledger from CashEntry, P&L, AR on PIs) | M1 | E0 | 6–8 | "Who owes me / what did I make this month" |
| **E2** | **Inventory + Suppliers** | M2 | E0 | 6–8 | Stock visibility + reorder alerts |
| **E3** | **Procurement** (PO + Goods Receipt → stock + payable) | S1 | E1, E2 | 4–5 | Tracked purchasing, auto stock valuation, AP |
| **E4** | **HR & Payroll** (employees, payroll → salary expense, leave) | S2 | E0, E1 | 5–6 | Payroll register + salary in P&L |
| **E5** | **Fleet** (vehicles, drivers, trips/fuel, maintenance) | C1 | E0, E1, E4 | 4–5 | Transport cost capture + expiry alerts |
| **E6** | **Consolidated reporting/BI** + master-data admin polish | S3 | E1–E5 | 4–5 | The single management cockpit |

**Indicative total:** ~32–41 ideal dev-days for the full set; ~15–20 days for the MUST core
(E0–E2) that already makes it a defensible minimum ERP.

---

## Why this order

1. **E0 first** because every later cross-post writes to the audit log and runs through the
   posting services — building it once avoids retrofitting audit into five modules.
2. **Accounting (E1) before Inventory (E2)** because the ledger is the destination for most
   cross-posts; having it live means Inventory/Procurement/HR/Fleet can post real entries
   from day one rather than being wired up later.
3. **Procurement (E3) after both** because Goods Receipt posts to *both* stock and AP.
4. **HR (E4) and Fleet (E5)** are cost-feeders into Accounting; Fleet after HR because
   drivers are employees.
5. **Reporting (E6) last** because it consolidates everything that now exists.

Each phase is independently shippable: if the project stops after E1+E2, IKON still has a
real, integrated finance-and-stock ERP slice.

---

## Per-phase definition of done

A phase is "done" when: Prisma migration applied; Zod-validated API routes; UI matching the
existing mockup; role checks enforced; cross-posts run inside transactions and write audit;
unit + integration tests for money/stock math; the list paginated; and the relevant
question in §3.4 is answerable from the UI. (Full DoD in
[`08-engineering-workflow-and-test-strategy.md`](08-engineering-workflow-and-test-strategy.md).)

---

## Milestones the owner will see

| Milestone | After phase | Owner-visible outcome |
|---|---|---|
| **M-A: "I can see my money."** | E1 | Monthly P&L + receivables aging on screen |
| **M-B: "I can see my stock."** | E2 | Stock register + low-stock alerts; material cost per order |
| **M-C: "Buying is tracked."** | E3 | POs, auto stock valuation, what I owe suppliers |
| **M-D: "Payroll runs here."** | E4 | Salary register + slips; salary in the P&L |
| **M-E: "The full cockpit."** | E6 | One dashboard: cash, AR/AP, stock, payroll, fleet, alerts |

---

## Risks & sequencing safeguards

| Risk | Mitigation |
|---|---|
| `CashEntry` → `LedgerEntry` migration touches existing cash data | Do it in E1 behind a reversible migration; keep cash-book UI working throughout; integration-test totals before/after |
| Scope creep toward "real accounting" | Hold the P1 line (no double-entry); decisions logged in doc 09 |
| A phase slips and blocks the next | Phases E4/E5/E6 are independent of each other; only E0→E1→E2→E3 is a hard chain |
| Stock on-hand drift | Derive from movements + a periodic reconciliation job (design in §05) |

---

## Relationship to the "Future Vision" (AI/WhatsApp)

The owner's `09-future-vision.html` ideas (WhatsApp order bot, voice-to-form, QR samples,
LC OCR, Bangla AI chat) are **explicitly out of scope** for the minimum ERP and tracked
separately. They are *integration/automation layers over* the ERP, best attempted only
after E1–E6 give them clean data to read and write. Noting them here keeps the roadmap
honest about what is and isn't included.
