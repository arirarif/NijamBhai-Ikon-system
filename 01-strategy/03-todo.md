# Project Todo Tracker
**IKON Garments Accessories Software**  
Updated: April 8, 2026

---

## PHASE 0 — Strategy & Design Decisions

### Discussions to complete
- [ ] **D-01** — UI language: English only? Bangla only? Both (bilingual toggle)?
- [ ] **D-02** — UI aesthetic: Dark professional / Light clean / Mixed?
- [ ] **D-03** — Who uses this software? Owner only? Staff also? Multiple user roles?
- [ ] **D-04** — Tech stack decision (see `decisions/tech-stack.md`)
- [ ] **D-05** — Should the software generate printable PDFs of PI, Challan, LC docs?
- [ ] **D-06** — Any existing data to import? (Excel files, notebooks?)
- [ ] **D-07** — Does vendor/outsource management need its own screen?
- [ ] **D-08** — Mobile access needed? (phone/tablet friendly?)
- [ ] **D-09** — Product/item catalogue — do you have fixed item types or free text?
- [ ] **D-10** — Notifications/alerts needed? (LC maturity, deadlines, etc.)

---

## PHASE 1 — UI Mockups (HTML, no backend)

### Screen mockups to build — one by one, discuss after each

| # | Screen | File | Status | Notes |
|---|---|---|---|---|
| M-01 | Dashboard | `mockups/01-dashboard.html` | ⬜ Not started | Pipeline view + quick search |
| M-02 | Companies & Merchandisers | `mockups/02-companies.html` | ⬜ Not started | Company cards + merchandiser sub-cards |
| M-03 | New Order form | `mockups/03-new-order.html` | ⬜ Not started | Style, description, qty, product type |
| M-04 | Order Detail page | `mockups/04-order-detail.html` | ⬜ Not started | Full order file + timeline |
| M-05 | Sample Revision tracker | `mockups/05-sample-revision.html` | ⬜ Not started | Revision history + add new revision |
| M-06 | Bulk Production tracker | `mockups/06-bulk-production.html` | ⬜ Not started | Unlocks after sample approval |
| M-07 | Delivery Challan form | `mockups/07-challan.html` | ⬜ Not started | Generate + print challan |
| M-08 | PI (Proforma Invoice) form | `mockups/08-pi-form.html` | ⬜ Not started | Line items, totals, print view |
| M-09 | LC Tracker | `mockups/09-lc-tracker.html` | ⬜ Not started | LC docs checklist + maturity countdown |
| M-10 | Vendor / Outsource management | `mockups/10-vendors.html` | ⬜ Not started | Pending discussion D-07 |
| M-11 | Reports / Export | `mockups/11-reports.html` | ⬜ Not started | Pending discussion |

### Shared assets
- [ ] `mockups/_shared.css` — colors, typography, spacing system
- [ ] `mockups/_components.html` — reusable button, badge, card patterns

---

## PHASE 2 — Tech Stack

- [ ] Finalize tech stack (after mockups look right)
- [ ] Document final decision in `decisions/tech-stack.md`

---

## PHASE 3 — Database & Backend

- [ ] Write final schema SQL
- [ ] Set up project skeleton
- [ ] Build API layer

---

## PHASE 4 — Build (screen by screen)

*(Will expand after Phase 1–2 complete)*

---

## PHASE 5 — Deployment

- [ ] Decide hosting (local server / cloud VPS / shared hosting)
- [ ] Deploy and test

---

## Discussion log

| Date | Topic | Decision |
|---|---|---|
| Apr 8 2026 | Business lifecycle | Fully mapped — 5 phases, 10 pipeline stages |
| Apr 8 2026 | Data model | 8 core entities identified |
| Apr 8 2026 | Screens | 11 screens identified |
| Apr 8 2026 | Project structure | Folders created, strategy-first approach confirmed |
