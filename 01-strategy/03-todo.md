# Project Todo Tracker
**IKON Garments Accessories Software**
Updated: 2026-05-22

---

## PHASE 0 — Strategy & Design Decisions ✅ done

### Discussions
- [x] **D-01** — UI language → **English only** (2026-05-22)
- [ ] **D-02** — UI aesthetic *(implicit: mockup style w/ dark+light toggle — needs formal lock)*
- [x] **D-03** — User roles → **4 roles + Vendor portal** (OWNER/MANAGER/STAFF/VIEWER + later Vendor) (2026-05-22)
- [x] **D-04** — Tech stack → see `06-docs/03-tech-stack.md` (Next 15 + Prisma + Postgres + NextAuth v5)
- [x] **D-05** — PDF generation → Puppeteer (locked in tech-stack)
- [ ] **D-06** — Existing data to import
- [ ] **D-07** — Vendor/outsource screen
- [x] **D-08** — Mobile access → yes, responsive done in mockups
- [x] **D-09** — Product catalogue → **12 fixed items + Other** (locked list in decisions doc) (2026-05-22)
- [ ] **D-10** — Notifications/alerts (LC maturity, overdue samples)

---

## PHASE 1 — UI Mockups ✅ done

All 13 screens built in `03-mockups/v2/`. Shared CSS, theme toggle, mobile drawer, sticky notes.

| # | Screen | File | Status |
|---|---|---|---|
| M-01 | Dashboard | `03-mockups/v2/01-dashboard.html` | ✅ |
| M-02 | Companies & Merchandisers | `02-companies.html` | ✅ |
| M-03 | Order Detail | `03-order-detail.html` | ✅ |
| M-04 | New Order | `04-new-order.html` | ✅ |
| M-05 | Sample Revision | `05-sample-revision.html` | ✅ |
| M-06 | PI | `06-pi.html` | ✅ |
| M-07 | LC Tracker | `07-lc-tracker.html` | ✅ |
| M-08 | Challan | `08-challan.html` | ✅ |
| M-09 | Future Vision | `09-future-vision.html` | ✅ |
| M-10 | Inventory | `10-inventory.html` | ✅ |
| M-11 | Accounts | `11-accounts.html` | ✅ |
| M-12 | HR & Payroll | `12-hr-payroll.html` | ✅ |
| M-13 | Vehicles | `13-vehicles.html` | ✅ |

---

## PHASE 2 — Tech Stack ✅ done

Locked in `06-docs/03-tech-stack.md`. Next.js 15 + React 19 + Prisma 7 + Postgres 16 + NextAuth v5 + Tailwind 4 + Zod + Puppeteer.

---

## PHASE 3 — Foundation 🟡 in progress

- [x] Prisma schema (12 models) + init migration
- [x] Seed (4 companies, 8 merch, 25 orders, revisions, bulk, timeline)
- [x] NextAuth credentials + edge-safe split + middleware
- [x] Sidebar + Topbar layout
- [x] UI primitives (Badge, Button, Card, FormField, StatCard)
- [x] Zod validations: company, order
- [x] All 9 page.tsx scaffolded (hardcoded demo data, no DB read yet)
- [ ] **B1** Login page hex → CSS vars
- [ ] **B2** Verify docker + migrate + seed clean run
- [ ] **B3** Verify login flow → dashboard

---

## PHASE 4 — Build sprints (per tech-stack.md)

### Sprint 1 — Dashboard (read-only from DB)
- [ ] C1 stat cards from Prisma counts
- [ ] C2 pipeline kanban from Order.stage groups
- [ ] C3 recent activity from TimelineEntry
- [ ] C4 top companies aggregation
- [ ] C5 overdue list

### Sprint 2 — Companies + Merchandisers CRUD
- [ ] D1 `GET /api/companies`
- [ ] D2 `POST /api/companies` (Zod validate)
- [ ] D3 `PATCH /api/companies/[id]` + soft-delete
- [ ] D4 `POST /api/companies/[id]/merchandisers`
- [ ] D5 Wire `companies/page.tsx` (list + add modal)
- [ ] D6 Integration tests

### Sprint 3 — New Order form wired
- [ ] E1 `POST /api/orders`
- [ ] E2 auto orderNo generator
- [ ] E3 redirect to `/orders/[id]`
- [ ] E4 integration test

### Sprint 4 — Orders list + detail + stage transitions
- [ ] F1 `GET /api/orders` filters
- [ ] F2 `GET /api/orders/[id]` full
- [ ] F3 `PATCH /api/orders/[id]/stage` + timeline write
- [ ] F4 wire pages

### Sprint 5 — Sample Revisions
- [ ] G1 `POST /api/orders/[id]/revisions`
- [ ] G2 `PATCH /api/revisions/[id]`
- [ ] G3 APPROVED → auto-advance stage
- [ ] G4 wire samples page

### Sprint 6 — Bulk Production
### Sprint 7 — Challan + PDF (Puppeteer)
### Sprint 8 — PI + PDF
### Sprint 9 — LC tracker + maturity alert
### Sprint 10 — Reports
### Sprint 11 — Settings page

---

## PHASE 5 — Quality & deploy
- [ ] E2E (Playwright) — login → order → approve → PDF
- [ ] Security audit (OWASP checklist from tech-stack.md)
- [ ] Vercel + Railway deploy
- [ ] Staff training docs (already drafted in `06-docs/05-USER-DOCUMENTATION.md`)

---

## Discussion log

| Date | Topic | Decision |
|---|---|---|
| 2026-04-08 | Business lifecycle | Mapped — 5 phases, 10 pipeline stages |
| 2026-04-08 | Data model | 8 core entities (grew to 12 in schema) |
| 2026-04-08 | Screens | 13 screens built |
| 2026-05-21 | Tech stack | Next 15 + Prisma + Postgres locked |
| 2026-05-22 | Repo hygiene | Folders renamed to numbered prefixes; ikon-app stays own repo |
| 2026-05-22 | D-01 | English only |
| 2026-05-22 | D-03 | 4 roles (OWNER/MANAGER/STAFF/VIEWER) + Vendor portal later |
| 2026-05-22 | D-09 | 12 fixed product types + Other free text |
