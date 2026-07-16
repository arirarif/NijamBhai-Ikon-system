# IKON Garments Accessories — Software Master Plan

**Business:** IKON Garments Accessories, Uttara, Dhaka-1230  
**Owner:** Muhammad Nezam Uddin  
**Project start:** April 2026  
**Status:** 🔴 Strategy phase — No code yet

---

## What we're building

A **pipeline tracker web application** for managing the full lifecycle of garment accessories orders — from the moment a merchandiser walks in, through sample revisions, bulk production, export documentation, and LC maturity.

This is NOT a simple CRUD app. It is a long-running, multi-party workflow manager where 100+ jobs run in parallel at different stages, across multiple weeks/months.

---

## The 5 operational phases (confirmed from business owner)

| Phase | What happens | Key pain point |
|---|---|---|
| **1. Order management** | Company → Merchandiser → Order placed | Currently manual, scattered |
| **2. Sample management** | In-house (4–6 types) or outsourced (Mirpur/Gilistan) → multiple revision loops until approved | Most complex phase, hardest to track |
| **3. Bulk production** | After sample approval → production with merchandiser timeline | Deadline tracking is missing |
| **4. Export documentation** | Delivery Challan → PI (SL, Style, Qty, Price, Total) → LC pack (Comm. Invoice, Packing List, Challan, Bill of Exchange) | Document generation is fully manual today |
| **5. Banking & LC lifecycle** | Bank forwarding → LC matures in 90 days | Maturity date tracking is missing |

---

## The single most important concept

Every order has **one status field** that moves through these 10 pipeline stages:

```
1-Order received → 2-Sample in progress → 3-Sample sent → 4-Correction needed →
5-Sample approved → 6-Bulk production → 7-Challan issued → 8-PI done →
9-LC open → 10-Matured
```

The dashboard = 100+ orders, each at a different stage, grouped and sorted so you know where to focus.

---

## Project phases (how we'll work)

### Phase 0 — Strategy & Design ← WE ARE HERE
- [x] Business lifecycle understood
- [x] Data model skeleton mapped
- [x] Screens identified
- [ ] UI direction decided (aesthetic, colors, language)
- [ ] All screens reviewed and signed off as mockups
- [ ] Open questions answered

### Phase 1 — UI Mockups (HTML templates, no backend)
- One `.html` file per screen
- Shared CSS in `03-mockups/_shared.css`
- Iterate until every screen feels right
- No data, no backend — just visual + UX

### Phase 2 — Tech Stack Decision
- Frontend framework (or plain HTML/CSS/JS?)
- Backend: Node.js / Python / PHP?
- Database: PostgreSQL / MySQL / SQLite?
- Hosting: local server / cloud?
- Language of UI: English / Bangla / both?

### Phase 3 — Database & Backend
- Schema implementation
- API design
- Authentication (who can log in?)

### Phase 4 — Build screen by screen
- One screen at a time, fully working
- Test with real data as you go

### Phase 5 — Delivery & training
- Deploy to server or local network
- Train staff

---

## What we know about the data model (from discussion)

**Core entities:**
- `Company` — ABC Ltd., Delta Garments, Apex Fashion, etc.
- `Merchandiser` — belongs to a company; has name, phone, designation
- `Order` — belongs to a merchandiser; has style name, description, product type, expected qty, status
- `SampleRevision` — belongs to an order; tracks type (in-house/outsourced), vendor, date sent, feedback, result
- `BulkProduction` — unlocks after sample approved; quantity, start date, deadline, completion %
- `DeliveryChallan` — dispatch record; challan number, date, items detail
- `PI (Proforma Invoice)` — PI number, date, line items (style/qty/price), total amount
- `LCRecord` — LC number, open date, maturity date (+90 days auto), bank name, docs submitted, status

**Key real data seen in PI screenshot (05-images/Screenshot_104.png):**
- Company: IKON GARMENTS ACCESSORIES
- Buyer: RIO DESIGN LIMITED, Mirpur 1216
- PI No.: PI-2025/02, Date: 17.03.2025
- Items: Satin Label, Customer Care, Elastic, Horn Button (22 line items)
- Units: DOZ, YDS, GROSS, PCS
- Bank: COMMUNITY BANK LTD, Uttara Branch, Swift: COYMBDDD
- A/C: 0100310654101
- Payment: Irrevocable L/C 60/90 days sight
- BIN/VAT No.: 003543528-0102

---

## Screens identified (full list)

See `01-strategy/02-screens.md` for the complete inventory with status.

---

## Open questions / decisions pending

See `02-decisions/` folder for each open decision.

---

## Reference files
- `05-images/Screenshot_104.png` — Real PI document (IKON letterhead)
- `05-images/Screenshot 2026-04-06 161444.png` — Real order email (style MBJA W26 DENIM-06 from JBC)
- `04-design-refs/01.png` — Business lifecycle flowchart
- `04-design-refs/02.png` — Data model skeleton + pipeline stages
- `04-design-refs/03.png` — Dashboard UI concept
- `04-design-refs/04.png` — Order detail page concept
- `04-design-refs/05.png` — Order timeline + locked bulk section concept
- `04-design-refs/06.png` — Companies & merchandisers screen concept
