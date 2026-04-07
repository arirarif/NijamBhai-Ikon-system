# Screen Inventory
**IKON Garments Accessories Software**  
All screens that need to exist — with purpose, key elements, and open questions per screen.

---

## SCREEN 1 — Dashboard
**File:** `mockups/01-dashboard.html`  
**Purpose:** Daily command center. See all active orders at a glance, grouped by pipeline stage.

**Key elements (from sugested ui/03.png):**
- Header: date, "+ Company" and "+ New Order" quick buttons
- Alert strip: "X LCs maturing within 14 days — action required"
- 4 stat cards: Active orders / Pending corrections / Approved this month / LC maturing (90d)
- Pipeline view: 4 columns (Sample stage | Bulk production | PI/Challan | LC & banking)
  - Each column shows order cards with: Style name, Merchandiser + Company, Revision no., Days active, Status badge
- All Orders quick search table: Style | Merchandiser | Company | Stage | Days active | Last update
- Status badges: correction (red), waiting (grey), sent (blue), bulk (yellow), on track (green), at risk (orange), draft, urgent, soon, processing

**Open questions for this screen:**
- How many orders per column before "load more"? → 3–5 cards + "+X more" link seems right
- Should columns be collapsible?
- Should the alert strip only show when there's something urgent?

---

## SCREEN 2 — Companies & Merchandisers
**File:** `mockups/02-companies.html`  
**Purpose:** Register all buyer companies and their merchandisers. Entry point for all new work.

**Key elements (from sugested ui/06.png):**
- Page title + search bar + "+ Add company" button
- Company card: name, country, contact person, phone, total orders, active now count, Edit + All orders buttons
- Under each company: merchandiser mini-cards (avatar initials, name, designation, active order count, order status badges)
- "+ Add merchandiser" button inside each company card
- Pagination: "Showing X of Y companies — Load all"

**Open questions for this screen:**
- What fields does a merchandiser need? (name, phone, designation confirmed — email? WhatsApp?)
- Can one merchandiser move to a different company? (transfer/edit needed?)
- Status badges on merchandiser cards — show current active order stage badges

---

## SCREEN 3 — New Order Form
**File:** `mockups/03-new-order.html`  
**Purpose:** Create a new order when a merchandiser comes in.

**Key elements:**
- Select company (dropdown or search)
- Select or add merchandiser
- Style name / style number (text)
- Product type (dropdown: Satin Label / Customer Care / Elastic / Horn Button / Woven Label / other — or free text?)
- Description / spec notes (textarea — e.g. "2cm × 5cm, gold thread on black base")
- Expected quantity + unit (DOZ / YDS / GROSS / PCS / other)
- Reference image upload (optional)
- Order date (auto = today, editable)
- Save as draft / Submit button

**Open questions:**
- Is "product type" a fixed catalogue or always free text?
- Do you ever have multiple product types in ONE order, or always one style per order?
- What is a "style" exactly — the buyer's internal code (like SH-204, MBJA W26)?

---

## SCREEN 4 — Order Detail Page
**File:** `mockups/04-order-detail.html`  
**Purpose:** The single "file" for one order. You open this and update it over weeks/months.

**Key elements (from sugested ui/04.png + 05.png):**
- Breadcrumb: Dashboard → Company → Merchandiser → Order
- Style name as page title + pipeline status badge + Actions button
- Merchandiser name, company, order date, days active subtitle
- Order information card (style, product type, date, merchandiser, company, qty, description) + Edit button
- Sample revisions section: list of all revision rounds, each showing:
  - Revision number, type (in-house / outsourced), vendor (if outsourced), date made, date sent, result, merchandiser feedback
  - Status badge (sent / in progress / correction needed / approved)
  - "Mark as sent" / "Mark approved" action buttons
- "+ Add revision" button
- Order timeline (right side or bottom): chronological activity log, future locked stages shown greyed out
- Bulk production & docs section: **LOCKED** until sample is approved — shows "Unlocks after sample approval" message

**Open questions:**
- Should there be file attachments per revision? (reference images, sample photos)
- Can you add notes/comments at any point without creating a new revision?

---

## SCREEN 5 — Sample Revision Tracker (add/edit revision)
**File:** `mockups/05-sample-revision.html`  
**Purpose:** Form to log a new revision round OR edit an existing one.

**Key elements:**
- Revision number (auto-incremented)
- Type: In-house / Outsourced (radio)
- If outsourced: vendor name / location (Mirpur / Gilistan / other)
- Date sample made
- Date sent to merchandiser
- Result: Pending / Correction needed / Approved (radio/dropdown)
- Merchandiser feedback (textarea)
- Internal notes (textarea — for your own factory notes)
- Save / Mark approved

---

## SCREEN 6 — Bulk Production Tracker
**File:** `mockups/06-bulk-production.html`  
**Purpose:** Track production milestones after sample is approved. Unlocked state of the locked section.

**Key elements:**
- Quantity to produce + unit
- Production start date
- Merchandiser delivery deadline
- Completion % slider or manual entry
- Milestone notes
- Status: on track / at risk / completed

---

## SCREEN 7 — Delivery Challan
**File:** `mockups/07-challan.html`  
**Purpose:** Generate and print a Delivery Challan document.

**Key elements:**
- IKON letterhead (auto)
- Challan number + date
- Buyer name + address (from company record)
- Items table: style / description / quantity / unit
- Dispatch date
- Print/PDF button

---

## SCREEN 8 — PI (Proforma Invoice)
**File:** `mockups/08-pi-form.html`  
**Purpose:** Generate the PI document. Based on real PI seen in `img/Screenshot_104.png`.

**Key elements:**
- IKON letterhead (pre-filled from system settings)
- PI Number (e.g. PI-2025/02) + Date
- Buyer address block (from company record)
- Line items table: SL | Description (Style) | Qty | Unit price | Total
- Total row: "US DOLLAR [AMOUNT IN WORDS] ONLY"
- Terms & Conditions section (standard text — pre-filled):
  - Shipper inspection final
  - Partial shipment allowed, Transshipment prohibited
  - Shipment from Uttara factory
  - Consignment takeover within 7 days of delivery
  - Payment: Irrevocable L/C 60/90 days sight
  - Advising Bank: COMMUNITY BANK LTD, Uttara, Swift: COYMBDDD
  - A/C: 0100310654101
  - US Dollar currency
  - BIN/VAT: 003543528-0102
- Print/PDF button
- "Accepted by" + "Issued By" signature blocks

---

## SCREEN 9 — LC Tracker
**File:** `mockups/09-lc-tracker.html`  
**Purpose:** Track the Letter of Credit lifecycle — documents submitted, bank forwarding, maturity countdown.

**Key elements:**
- LC number + open date
- Auto-calculated maturity date (open date + 90 days)
- Countdown: "X days until maturity" — red if <14 days
- Documents checklist:
  - [ ] Commercial Invoice
  - [ ] Packing List
  - [ ] Delivery Challan
  - [ ] Bill of Exchange
- Bank name + forwarding date
- Status: Open / Forwarded / Matured
- Notes

---

## SCREEN 10 — Vendor / Outsource Management *(pending discussion D-07)*
**File:** `mockups/10-vendors.html`  
**Purpose:** Keep a directory of outsource vendors (Mirpur, Gilistan, etc.)

**Possible elements:**
- Vendor name, location, item types they handle
- Contact person + phone
- History: how many times used, which orders

---

## SCREEN 11 — Reports
**File:** `mockups/11-reports.html`  
**Purpose:** Summary views for business overview.

**Possible reports:**
- Orders by company (this month / this year)
- LC maturity calendar
- Revenue summary from PIs
- Pending corrections list
- Overdue deliveries

*(To be discussed in more detail)*

---

## Navigation structure (proposed)

```
Sidebar / Top nav:
├── Dashboard          ← default landing page
├── Orders             ← all orders table with filters
├── Companies          ← companies + merchandisers
├── Documents
│   ├── Challans
│   ├── Proforma Invoices
│   └── LC Tracker
├── Vendors            ← if D-07 confirmed
├── Reports
└── Settings           ← IKON company info, bank details, terms
```
