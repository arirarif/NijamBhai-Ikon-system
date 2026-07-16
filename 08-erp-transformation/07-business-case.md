# 07 — Business Case

Why each module is worth building, what it changes for IKON, what it costs, and how success
is measured. Framed for the owner and for a reviewer assessing whether the plan is
proportionate to a five-to-eight-person firm.

---

## 7.1 The core argument

IKON already runs its **revenue engine** (orders → documents → LC) in software. What it
does **not** yet run in software is everything that tells the owner whether that engine is
*profitable and sustainable*: stock, costs, receivables, payroll, and expenses. Today those
live in notebooks, memory, and Excel (per the SRS current-state). The ERP modules close
that loop. The value is not "more screens" — it is **decision information the owner cannot
get today.**

---

## 7.2 Value per module

| Module | Manual pain today | What the module changes | Headline metric it unlocks |
|---|---|---|---|
| **Accounting** | "Did we make money this month?" answered by feel; overdue buyer payments tracked in the owner's head | Monthly P&L; receivables aging tied to PIs/LCs; categorised expenses | Net profit / month; total & overdue receivables |
| **Inventory + Suppliers** | Stockouts discovered mid-order; capital tied up in stock invisible | Live stock + reorder alerts; material cost per order | Stock value; low-stock count; material cost/order |
| **Procurement** | Ad-hoc buying; "what do I owe suppliers?" unknown | Tracked POs; auto-valued receipts; payables | Open PO value; total payables |
| **HR & Payroll** | Salary registers by hand each month | One-click payroll + slips; salary auto-posts to P&L | Monthly payroll; pending salaries |
| **Fleet** | Fuel/maintenance uncosted; insurance lapses risk fines | Trip/fuel/maintenance logs; expiry alerts | Transport cost/month; days-to-expiry |
| **Reporting/BI** | Numbers scattered across modules | One cockpit | All of the above, at a glance |

---

## 7.3 How it supports the business plan

- **Pricing & margin.** Per-order costing (materials from Inventory, labour from payroll,
  transport from Fleet, all in the ledger) gives a real cost base — so quotes to buyers are
  grounded, not guessed. For a trims supplier competing on price, this directly protects
  margin.
- **Cash-flow control.** Receivables aging + LC maturity (already tracked) + payables gives
  a forward view of cash — the single biggest survival factor for a small export-linked
  business on 60/90-day LC terms.
- **Working-capital efficiency.** Inventory value + reorder discipline frees cash otherwise
  frozen in over-stock or lost to rush-buying.
- **Owner leverage.** The owner currently *is* the system (memory + notebooks). The ERP
  moves that knowledge into software — reducing key-person risk and freeing the owner's time
  from clerical tracking to selling and relationships.
- **Credibility & growth.** A firm that can produce clean PIs, LC packs, P&Ls, and stock
  reports presents better to buyers and banks — and is in a position to take on more
  concurrent orders without proportionally more administrative effort.

---

## 7.4 Cost

- **Build cost:** the developer's time (~32–41 ideal dev-days for the full set; ~15–20 for
  the MUST core) — see roadmap. No new licences.
- **Run cost:** unchanged. The modules add tables to the *same* Postgres and routes to the
  *same* Next.js app. The project's existing ~**$20–30/month** hosting (Vercel/Railway)
  envelope holds; no new infrastructure (the whole point of the modular-monolith stance).
- **Operating cost:** near-zero added staff burden — the modules *remove* manual work
  (payroll registers, stock counts, receivable chasing) rather than add it.

This favourable cost profile is a direct consequence of the right-sizing charter: by
refusing enterprise complexity, the ERP is affordable to build *and* to run for a decade.

---

## 7.5 Risks & honest caveats

| Risk | Likelihood | Mitigation |
|---|---|---|
| Owner/staff don't adopt a module (behaviour change) | Medium | Each module mirrors a mockup the owner already designed; ship value module-at-a-time; keep forms plain (P8) |
| Finance scope drifts toward full accounting | Medium | MoSCoW + decision register hold the line; "WON'T" list is explicit |
| Data-entry burden (stock movements) exceeds benefit | Low–Med | Keep entry minimal; auto-post from Procurement so stock-in isn't double-typed |
| Single developer / bus-factor | Medium | Documentation (this dossier + README), one familiar language, conventional patterns |
| `CashEntry` migration disrupts the working cash book | Low | Reversible migration, tested totals, phased in E1 |

---

## 7.6 Success metrics (how we'll know it worked)

Operational (the system is used):
- ≥ 90% of money movements recorded in the ledger (vs notebooks) within 3 months of E1.
- Stock register reflects reality within an agreed tolerance after E2.
- Payroll run entirely in-app from the first month after E4.

Business (it created value):
- The owner can state monthly net profit and total overdue receivables **from the system**.
- Reduced rush-purchases / stockouts (fewer order delays attributable to missing material).
- Lapsed insurance/fitness incidents → zero (Fleet expiry alerts).

These are deliberately modest and measurable — appropriate to the scale, and the kind of
before/after evidence that makes the case study assessable.
