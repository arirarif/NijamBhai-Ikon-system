# IKON Garments Accessories — User Documentation

**System:** Order & Export Management System  
**Version:** 1.0  
**Last updated:** April 9, 2026

---

## Table of Contents

1. [System Overview](#1-system-overview)
2. [Data Flow — How Everything Connects](#2-data-flow--how-everything-connects)
3. [Getting Started — Where to Begin](#3-getting-started--where-to-begin)
4. [Step-by-Step Workflows](#4-step-by-step-workflows)
5. [Module Guide](#5-module-guide)
6. [Navigation Map](#6-navigation-map)
7. [Understanding the Pipeline](#7-understanding-the-pipeline)
8. [Document Generation Guide](#8-document-generation-guide)
9. [Alerts & What They Mean](#9-alerts--what-they-mean)
10. [Settings & System Configuration](#10-settings--system-configuration)
11. [Tips & Best Practices](#11-tips--best-practices)
12. [FAQ](#12-faq)

---

## 1. System Overview

### What is this software?

A single platform to manage everything in IKON Garments Accessories' daily operations — from the moment a buyer's merchandiser walks in to place an order, through sample making, revisions, bulk production, delivery, invoicing, and finally collecting payment through Letter of Credit (LC).

### Who is it for?

| Role | What they do in the system |
|---|---|
| **Owner** (Nezam bhai) | Everything — create orders, manage companies, generate documents, track finances |
| **Manager** | Daily operations — orders, samples, production, documents |
| **Staff** | Update sample status, log production progress on assigned orders |
| **Viewer** | Read-only access — check order status, view dashboard |

### The core idea

Every order moves through a **10-stage pipeline**. The system tracks where each order is, what needs attention, and what's coming next. Instead of remembering 100+ orders in your head, you open the dashboard and see everything at a glance.

---

## 2. Data Flow — How Everything Connects

### 2.1 The Big Picture

```
┌──────────────────────────────────────────────────────────────────────────┐
│                         IKON SYSTEM DATA FLOW                            │
│                                                                          │
│   SETUP (do once)           DAILY WORK              FINANCE & EXPORT     │
│   ─────────────           ──────────────           ──────────────────    │
│                                                                          │
│   ┌──────────┐            ┌──────────┐            ┌──────────────┐      │
│   │ Settings │            │ New Order│            │   Delivery   │      │
│   │ (IKON    │            │  Form    │            │   Challan    │      │
│   │  info,   │            └────┬─────┘            └──────┬───────┘      │
│   │  bank,   │                 │                         │              │
│   │  terms)  │                 ▼                         ▼              │
│   └──────────┘            ┌──────────┐            ┌──────────────┐      │
│                           │  Sample  │            │   Proforma   │      │
│   ┌──────────┐            │ Revision │            │   Invoice    │      │
│   │ Company  │──creates──▶│  Loop    │            │   (PI)       │      │
│   │ Register │            │ (R1→R2→  │            └──────┬───────┘      │
│   └────┬─────┘            │  R3→...) │                   │              │
│        │                  └────┬─────┘                   ▼              │
│        ▼                       │                  ┌──────────────┐      │
│   ┌──────────┐                 ▼                  │  LC Tracker  │      │
│   │Merchandis│            ┌──────────┐            │  (90 day     │      │
│   │er under  │──places───▶│  Bulk    │            │   countdown) │      │
│   │company   │            │Production│            └──────┬───────┘      │
│   └──────────┘            └──────────┘                   │              │
│                                                          ▼              │
│   ┌──────────┐                                    ┌──────────────┐      │
│   │ Vendor   │──linked to sample revisions        │  LC Matured  │      │
│   │ Register │  (who made the sample?)            │  = PAYMENT   │      │
│   └──────────┘                                    └──────────────┘      │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
```

### 2.2 Data Flow: Order Creation to Payment

Here's exactly how data moves through the system for a single order, step by step:

```
Step 1: REGISTER COMPANY (one-time)
         │
         │  Name, country, address, phone
         │
         ▼
Step 2: ADD MERCHANDISER under that company (one-time per merchandiser)
         │
         │  Name, phone, designation
         │
         ▼
Step 3: CREATE ORDER
         │
         │  Links to: Company + Merchandiser
         │  Fields: Style, product type, qty, unit, description
         │  System auto-generates: Order number (F-2026-039)
         │  Pipeline starts at: Stage 1 — Order Received
         │
         ▼
Step 4: ADD SAMPLE REVISION (repeat 1–10+ times)
         │
         │  Links to: Order + (optionally) Vendor
         │  Fields: Type (in-house/outsourced), dates, feedback, result
         │  Pipeline moves: Stage 2 → 3 → 4 → 2 → 3 (loop until approved)
         │
         ├── If CORRECTION NEEDED → loop back, add new revision
         │
         └── If APPROVED → pipeline moves to Stage 5
                │
                ▼
Step 5: BULK PRODUCTION (unlocks after approval)
         │
         │  Links to: Order
         │  Fields: Quantity, start date, deadline, completion %
         │  Pipeline: Stage 6 — Bulk Production
         │
         ▼
Step 6: DELIVERY CHALLAN
         │
         │  Links to: Order + Company (auto-fills buyer details)
         │  Fields: Line items (style, qty, unit), dispatch date
         │  Auto-populated: IKON letterhead, buyer name/address
         │  Pipeline: Stage 7 — Challan Issued
         │  Output: Printable/PDF document
         │
         ▼
Step 7: PROFORMA INVOICE (PI)
         │
         │  Links to: Order + Company (auto-fills buyer details)
         │  Fields: Line items (style, qty, unit price, total)
         │  Auto-populated: IKON letterhead, terms, bank details, BIN/VAT
         │  Auto-calculated: Row totals, grand total, amount in words
         │  Pipeline: Stage 8 — PI Done
         │  Output: Printable/PDF document
         │
         ▼
Step 8: LC RECORD
         │
         │  Links to: Order + PI
         │  Fields: LC number, open date, issuing bank
         │  Auto-calculated: Maturity date (open date + 90 days)
         │  Checklist: Commercial Invoice ☐  Packing List ☐
         │             Delivery Challan ☐    Bill of Exchange ☐
         │  Pipeline: Stage 9 — LC Open
         │
         ▼
Step 9: BANK FORWARDING
         │
         │  Update LC record: forwarding date, status → Forwarded
         │  Wait for maturity countdown...
         │
         ▼
Step 10: LC MATURED → PAYMENT RECEIVED
          │
          │  Pipeline: Stage 10 — Matured (final)
          │  Order is complete. ✓
```

### 2.3 How Entities Link Together

```
Company
  └── has many → Merchandisers
                    └── has many → Orders
                                     ├── has many → Sample Revisions ─── links to → Vendor
                                     ├── has one  → Bulk Production
                                     ├── has many → Delivery Challans ─── has many → Line Items
                                     ├── has one  → Proforma Invoice ─── has many → Line Items
                                     ├── has one  → LC Record
                                     └── has many → Activity Log entries

Settings (IKON info, bank, terms) ──── pre-fills ──→ PI, Challan documents
```

### 2.4 Where does data come from?

| Data | Source | Entered by | Frequency |
|---|---|---|---|
| Company details | Buyer's business card, email, or verbal | Owner/Manager | Once per company |
| Merchandiser details | Business card, phone contact | Owner/Manager | Once per merchandiser |
| Order details | Merchandiser visit (verbal or email/WhatsApp) | Owner/Manager | Every new order |
| Sample revision | Factory floor (sample made + sent) + merchandiser feedback | Owner/Staff | Multiple times per order |
| Bulk production | Factory floor progress | Staff | Updated weekly |
| Challan details | At time of delivery/dispatch | Owner/Manager | Once per delivery |
| PI details | Created when goods are ready for billing | Owner/Manager | Once per order |
| LC details | Physical LC document from bank | Owner | Once per order |
| Vendor directory | Known vendors from experience | Owner | As needed |
| Inventory stock | Physical stock count + supplier deliveries | Staff | Ongoing |
| Expenses/Income | Bills, receipts, bank statements | Owner | Ongoing |
| Employee data | Hire paperwork | Owner/Manager | Once per employee |
| Vehicle/Trip data | Driver reports, fuel receipts | Manager/Staff | Per trip |

---

## 3. Getting Started — Where to Begin

### Day 1: First-Time Setup (do this once)

```
┌──────────────────────────────────────────────────┐
│  START HERE                                       │
│                                                   │
│  Step 1 → Settings                               │
│           Fill in IKON company info, bank         │
│           details, terms & conditions             │
│                                                   │
│  Step 2 → Companies                              │
│           Add your top 5–10 buyer companies       │
│                                                   │
│  Step 3 → Merchandisers                          │
│           Add merchandisers under each company    │
│                                                   │
│  Step 4 → Vendors (optional)                     │
│           Add outsource vendors (Mirpur, etc.)    │
│                                                   │
│  Step 5 → Inventory (optional)                   │
│           Enter current stock of raw materials    │
│                                                   │
│  Step 6 → Employees (optional)                   │
│           Add staff for HR/Payroll module         │
│                                                   │
│  DONE! → Now go to Dashboard. You're ready.      │
└──────────────────────────────────────────────────┘
```

**Detailed first-time steps:**

#### Step 1 — Configure Settings
1. Go to **Settings** from the sidebar
2. Enter IKON company information:
   - Company name: IKON GARMENTS ACCESSORIES
   - Address: Uttara, Dhaka-1230
   - Phone, email
3. Enter banking details:
   - Bank: COMMUNITY BANK LTD, Uttara Branch
   - Swift: COYMBDDD
   - Account: 0100310654101
4. Enter BIN/VAT: 003543528-0102
5. Review and save standard PI Terms & Conditions
6. Save

> **Why first?** These details auto-fill into every PI and Challan. Set them once, never type again.

#### Step 2 — Register Buyer Companies
1. Go to **Companies** from the sidebar
2. Click **"+ Add Company"**
3. Enter: company name, country, contact person, phone, address
4. Save
5. Repeat for each buyer company (e.g., RIO DESIGN LIMITED, Noman Group, Bay Group, etc.)

> **Tip:** You don't need all companies right now. Add them as orders come in.

#### Step 3 — Add Merchandisers
1. On the Companies page, find the company
2. Click **"+ Add Merchandiser"** inside that company card
3. Enter: name, phone, designation
4. Save
5. Repeat for each merchandiser under that company

> **One merchandiser = one person.** Each belongs to one company. If a merchandiser moves to another company, you can transfer them.

#### Step 4 — Add Vendors (Optional)
1. Go to **Vendors** from the sidebar
2. Click **"+ Add Vendor"**
3. Enter: name, location (Mirpur/Gilistan/other), item types, contact, phone
4. Save

> **Why?** When you log an outsourced sample revision, you can link it to a vendor. This builds a history of who made what.

---

## 4. Step-by-Step Workflows

### 4.1 Workflow: New Order Arrives

**When:** A merchandiser comes in (or calls/WhatsApp) to place a new order.

```
YOU DO THIS                              SYSTEM DOES THIS
──────────────                           ──────────────────

1. Go to Dashboard                       
2. Click "+ New Order"                   
3. Select Company from dropdown          → Filters merchandisers for that company
4. Select Merchandiser                   
5. Enter Style Name (e.g., SH-204)      
6. Select Product Type                   → Suggests from catalogue
7. Enter description/specs               
8. Enter expected qty + unit             
9. Upload reference image (optional)     
10. Click "Create Order"                 → Generates order number F-2026-XXX
                                         → Sets pipeline: Stage 1 — Order Received
                                         → Logs activity: "Order created"
                                         → Appears on Dashboard
```

### 4.2 Workflow: Making & Sending a Sample

**When:** You've made a sample (in-house or outsourced) and are sending it to the merchandiser.

```
YOU DO THIS                              SYSTEM DOES THIS
──────────────                           ──────────────────

1. Go to Dashboard → find the order      
2. Click the order card                  → Opens Order Detail page
3. Click "+ Add Revision"                → Opens Sample Revision form
4. Select type: In-house or Outsourced   → If outsourced: shows vendor fields
5. (If outsourced) Select vendor         
6. Enter "Date Sample Made"             
7. Enter "Date Sent to Merchandiser"    
8. Set Result: "Pending"                
9. Add any internal notes               
10. Click "Save"                         → Revision R1 (or R2, R3...) created
                                         → Pipeline moves: Stage 2 → Stage 3
                                         → Activity log: "Sample R1 sent"
```

### 4.3 Workflow: Merchandiser Gives Feedback (Correction Needed)

**When:** Merchandiser says the sample needs changes.

```
YOU DO THIS                              SYSTEM DOES THIS
──────────────                           ──────────────────

1. Open Order Detail page                
2. Find the latest revision              
3. Click "Edit" on that revision         
4. Change Result: "Correction Needed"    
5. Enter merchandiser feedback           
   (what they want changed)             
6. Click "Save"                          → Pipeline moves: Stage 3 → Stage 4
                                         → Activity log: "R1 — correction needed"
                                         → Order card turns RED on dashboard

NOW: Make the corrected sample, then:

7. Click "+ Add Revision"                → Auto-increments to R2
8. Fill in new sample details            
9. Set Result: "Pending" or "Sent"       → Pipeline: Stage 4 → Stage 2 → Stage 3
10. Wait for next feedback...            → Loop continues until approved
```

### 4.4 Workflow: Sample Approved!

**When:** Merchandiser approves the sample.

```
YOU DO THIS                              SYSTEM DOES THIS
──────────────                           ──────────────────

1. Open Order Detail page                
2. Find the latest revision              
3. Click "Mark Approved"                 → Result changes to "Approved"
   (or edit → set result to Approved)    → Pipeline jumps: → Stage 5 (Approved)
                                         → Activity log: "R3 approved by merchandiser"
                                         → ⭐ BULK PRODUCTION section UNLOCKS
                                         → Dashboard: card moves to "Bulk" column
```

### 4.5 Workflow: Start Bulk Production

**When:** Sample is approved, time to produce the full order.

```
YOU DO THIS                              SYSTEM DOES THIS
──────────────                           ──────────────────

1. Open Order Detail page                
2. Scroll to Bulk Production section     → No longer locked!
3. Enter: Quantity + Unit                
4. Enter: Production Start Date          
5. Enter: Merchandiser Deadline          
6. Click "Save"                          → Pipeline: Stage 5 → Stage 6
                                         → Activity log: "Bulk production started"
                                         → Deadline tracking begins

AS PRODUCTION PROGRESSES:

7. Update Completion %                   → Status auto-calculates:
   (25% → 50% → 75% → 100%)             → "On Track" (green) or "At Risk" (orange)
8. Add milestone notes                   → If deadline near + low %: alert appears
```

### 4.6 Workflow: Delivery & Documents

**When:** Bulk production complete, time to ship and generate documents.

```
STEP A — CREATE DELIVERY CHALLAN

1. Go to Documents → Challans             
2. Click "+ New Challan"                 
3. Link to Order                         → Auto-fills buyer name/address
4. Add line items (style, qty, unit)     
5. Enter dispatch date                   
6. Click "Save"                          → Pipeline: Stage 6 → Stage 7
7. Click "Print" or "Download PDF"       → Challan ready for physical delivery

STEP B — CREATE PROFORMA INVOICE (PI)

1. Go to Documents → Proforma Invoices   
2. Click "+ New PI"                      
3. Link to Order                         → Auto-fills buyer, IKON letterhead,
                                           bank details, terms & conditions
4. Add line items:                       
   - Description (style)                 
   - Quantity                            
   - Unit Price                          → Auto-calculates row total
5. Review grand total                    → Auto-calculated + shown in words
6. Click "Finalize"                      → Pipeline: Stage 7 → Stage 8
7. Click "Print" or "Download PDF"       → PI ready to send to buyer/bank

STEP C — CREATE LC RECORD

1. Go to Documents → LC Tracker          
2. Click "+ New LC"                      
3. Enter LC number (from bank document)  
4. Enter Open Date                       → Auto-calculates maturity: +90 days
5. Enter Issuing Bank                    
6. Click "Save"                          → Pipeline: Stage 8 → Stage 9
                                         → Countdown starts: "X days to maturity"
```

### 4.7 Workflow: LC Document Submission & Maturity

**When:** Submitting documents to bank and waiting for LC maturity.

```
YOU DO THIS                              SYSTEM DOES THIS
──────────────                           ──────────────────

1. Open LC record                        
2. Check off documents as you submit:    
   ☑ Commercial Invoice                 
   ☑ Packing List                       
   ☑ Delivery Challan                   
   ☑ Bill of Exchange                   
3. Enter Bank Forwarding Date            → Status: Open → Forwarded
4. Add notes if needed                   

THEN WAIT...

5. System counts down daily              → Dashboard alert when < 14 days
6. On maturity date:                     
   Click "Mark as Matured"              → Pipeline: Stage 9 → Stage 10
                                         → ORDER COMPLETE ✓
                                         → Moves to completed/archive
```

---

## 5. Module Guide

### 5.1 Dashboard (`/dashboard`)

**What it shows:**
- **4 stat cards** at the top: Active Orders, Pending Corrections, Approved This Month, LC Maturing
- **Alert strip** (when there are urgent items): LC approaching maturity, overdue corrections, at-risk production
- **Pipeline columns** (4 columns showing orders grouped by stage)
- **Quick search** bar for finding any order instantly

**When to use it:** Every time you open the system. This is your home base.

**Key actions from dashboard:**
- Click any order card → go to order detail
- Click stat card → filter view to that category
- Click "+ New Order" → create order
- Click "+ Company" → add buyer company

---

### 5.2 Companies & Merchandisers (`/companies`)

**What it shows:**
- All buyer companies as cards
- Merchandisers nested under each company
- Order counts and active status per merchandiser

**When to use it:**
- First-time setup (register all your buyers)
- When a new buyer company contacts you
- When a new merchandiser starts working with you
- To look up a buyer's contact info

**Key actions:**
- "+ Add Company" → register new buyer
- "+ Add Merchandiser" → add a person under a company
- "All Orders" → see all orders for that company
- Click merchandiser → see their orders

---

### 5.3 Order Detail (`/orders/:id`)

**What it shows:** Everything about one specific order — the complete "file" for that job.

**Sections on this page:**
1. **Header** — style name, pipeline stage badge, days active
2. **Order Information** — all order fields (editable)
3. **Pipeline Progress Bar** — visual 10-stage progress indicator
4. **Sample Revisions** — history of every revision round
5. **Bulk Production** — locked until approved, then shows production tracker
6. **Activity Timeline** — chronological log of everything that happened
7. **Documents** — links to related Challan, PI, LC

**When to use it:** Whenever you need to update an order, check its status, or see its history.

---

### 5.4 New Order Form (`/orders/new`)

**What it shows:** Clean form to create a new order.

**Required fields:** Company, Merchandiser, Style Name, Product Type  
**Optional fields:** Description, Quantity, Unit, Reference Image, Order Date

**Tips:**
- Select company first — merchandiser dropdown will filter to that company's people
- Use "Save as Draft" if you're not ready to formally submit yet
- Drafts don't appear in the pipeline until you submit them

---

### 5.5 Sample Revision Form (`/orders/:id/revisions/new`)

**What it shows:** Form to log a new sample revision round.

**Key decisions on this form:**
- **In-house vs. Outsourced** — selecting "outsourced" reveals vendor fields
- **Result** — this drives pipeline movement:
  - "Pending" → no pipeline change
  - "Correction Needed" → pipeline moves to Stage 4
  - "Approved" → pipeline jumps to Stage 5, unlocks bulk production

---

### 5.6 Proforma Invoice (`/documents/pi`)

**What it shows:** Full PI document matching IKON's official format.

**Auto-populated fields (you don't type these):**
- IKON letterhead (from settings)
- Buyer name + address (from company record)
- Banking details (from settings)
- BIN/VAT number (from settings)
- Terms & Conditions (from settings)
- Row totals (auto-calculated)
- Grand total (auto-calculated)
- Amount in words (auto-generated)

**You only enter:** Line items (description, qty, unit price) and PI date.

---

### 5.7 LC Tracker (`/documents/lc`)

**What it shows:** LC lifecycle with countdown to maturity.

**Color coding for countdown:**
- 🟢 Green: > 30 days to maturity
- 🟡 Amber: 14–30 days to maturity
- 🔴 Red: < 14 days to maturity (also triggers dashboard alert)

**Document checklist:** Track which of the 4 required documents you've submitted to the bank.

---

### 5.8 Delivery Challan (`/documents/challan`)

**What it shows:** Dispatch document with IKON letterhead.

**Auto-populated:** IKON info, buyer details from company record.  
**You enter:** Line items, dispatch date.

---

### 5.9 Inventory (`/inventory`)

**What it shows:** Raw material stock register.

**Key features:**
- Visual stock level bars (green = OK, yellow = low, red = critical)
- Stock-in / Stock-out transaction logging
- Alert when stock falls below minimum level

**When to use it:** When materials arrive, when materials are used for production, for stock checks.

---

### 5.10 Accounts (`/accounts`)

**What it shows:** Income and expenses for the business.

**Key features:**
- Income vs. expense monthly bar chart
- Transaction ledger (all entries)
- Outstanding receivables (PIs issued but payment not yet received)

**When to use it:** To record expenses, track income from LC payments, review monthly P&L.

---

### 5.11 HR & Payroll (`/hr`)

**What it shows:** Employee directory and salary management.

**Key features:**
- Employee list with details
- Monthly salary register
- 6-month salary history
- Leave request approval

**When to use it:** Monthly payroll processing, adding new employees, managing leave.

---

### 5.12 Vehicles & Drivers (`/vehicles`)

**What it shows:** Fleet and logistics management.

**Key features:**
- Vehicle register with status
- Driver profiles
- Trip log
- Fuel cost tracking
- Maintenance records

**When to use it:** Logging deliveries, tracking fuel costs, scheduling maintenance.

---

## 6. Navigation Map

### 6.1 Sidebar Structure

```
📊 Dashboard                    ← Your home page. Start here every day.
│
📦 Orders                       ← All orders table with search/filter
│
🏢 Companies                    ← Buyer companies + their merchandisers
│
📄 Documents
│   ├── Challans               ← Delivery challan list + create new
│   ├── Proforma Invoices      ← PI list + create new
│   └── LC Tracker             ← LC lifecycle management
│
📦 Inventory                    ← Raw material stock register
│
💰 Accounts                     ← Income, expenses, receivables
│
👥 HR & Payroll                 ← Employees, salaries, leave
│
🚗 Vehicles                     ← Fleet, drivers, trips, fuel
│
🏭 Vendors                      ← Outsource vendor directory
│
📊 Reports                      ← Summary views and exports
│
⚙️ Settings                     ← IKON info, bank details, terms, catalogue
```

### 6.2 Where to Go For Common Tasks

| I want to... | Go to... |
|---|---|
| See what needs attention right now | **Dashboard** |
| Create a new order | Dashboard → **"+ New Order"** button |
| Add a new buyer company | Dashboard → **"+ Company"** button, or **Companies** page |
| Find a specific order | Dashboard → **Quick Search** bar (search by style, order #, merchandiser, or company) |
| Update a sample revision | **Dashboard** → click order card → **Order Detail** → Sample Revisions section |
| Mark a sample as approved | **Order Detail** → latest revision → **"Mark Approved"** |
| Check production progress | **Order Detail** → Bulk Production section |
| Create a Delivery Challan | **Documents → Challans** → "+ New Challan" |
| Create a PI | **Documents → Proforma Invoices** → "+ New PI" |
| Track an LC | **Documents → LC Tracker** |
| See which LCs are maturing soon | **Dashboard** (alert strip) or **LC Tracker** (sorted by maturity) |
| Check raw material stock | **Inventory** |
| Record an expense | **Accounts** → "+ Add Expense" |
| Process monthly payroll | **HR & Payroll** → Salary Register tab |
| Log a delivery trip | **Vehicles** → "+ Log Trip" |
| Generate a report | **Reports** → select report type |
| Change IKON bank details | **Settings** → Banking section |

### 6.3 Page-to-Page Flow

```
                    ┌──────────┐
                    │DASHBOARD │ ◄── Daily landing page
                    └─────┬────┘
                          │
            ┌─────────────┼─────────────┐
            │             │             │
            ▼             ▼             ▼
     ┌───────────┐  ┌──────────┐  ┌──────────┐
     │ Companies │  │  Orders  │  │Documents │
     │  & Merch  │  │  (list)  │  │          │
     └─────┬─────┘  └────┬─────┘  └────┬─────┘
           │              │             │
           │              ▼             ├──→ Challans
           │        ┌──────────┐       ├──→ PIs
           │        │  Order   │       └──→ LC Tracker
           │        │  Detail  │
           │        └────┬─────┘
           │             │
           │    ┌────────┼────────┐
           │    │        │        │
           │    ▼        ▼        ▼
           │  Sample   Bulk    Documents
           │  Revision Prod.   (linked)
           │  Form     Tracker
           │
           └──→ Merchandiser
                Orders List
```

---

## 7. Understanding the Pipeline

### 7.1 The 10 Stages Explained

| # | Stage | What it means | What to do next |
|---|---|---|---|
| **1** | Order Received | Order just created, no work started yet | Make the first sample |
| **2** | Sample In Progress | A sample is being made (in-house or outsourced) | Wait for sample to be ready, then send |
| **3** | Sample Sent | Sample shipped to merchandiser, waiting for feedback | Wait for merchandiser's reply |
| **4** | Correction Needed | Merchandiser wants changes | Make corrected sample (→ loops back to Stage 2) |
| **5** | Sample Approved | Merchandiser approved! Ready for bulk order | Start bulk production |
| **6** | Bulk Production | Full-scale manufacturing in progress | Track completion %, meet deadline |
| **7** | Challan Issued | Goods dispatched, delivery challan generated | Create PI |
| **8** | PI Done | Proforma Invoice generated and sent | Open LC with bank |
| **9** | LC Open | Letter of Credit active, 90-day countdown | Submit documents, wait for maturity |
| **10** | Matured | LC matured, payment received | Done! Archive order. |

### 7.2 The Sample Loop (Most Common Scenario)

Most of your daily work happens in Stages 2–4. Here's the loop visualized:

```
                    ┌──────────────────────────────┐
                    │                              │
                    ▼                              │
            ┌──────────────┐                       │
            │ 2. Sample In │                       │
            │   Progress   │                       │
            └──────┬───────┘                       │
                   │                               │
                   ▼                               │
            ┌──────────────┐                       │
            │ 3. Sample    │                       │
            │    Sent      │                       │
            └──────┬───────┘                       │
                   │                               │
          ┌────────┴────────┐                      │
          │                 │                      │
          ▼                 ▼                      │
   ┌──────────┐     ┌──────────────┐               │
   │ APPROVED │     │ 4. Correction│───────────────┘
   │  → S5 ✓  │     │    Needed    │  (make new sample,
   └──────────┘     └──────────────┘   go back to S2)

   Typical: 2–5 loops before approval
   Complex orders: 8–10+ loops
```

### 7.3 Dashboard Column Mapping

The dashboard groups the 10 stages into 4 visual columns:

```
┌─────────────┐ ┌──────────────┐ ┌─────────────┐ ┌──────────────┐
│  SAMPLE     │ │   BULK       │ │  PI /       │ │  LC &        │
│  STAGE      │ │   PRODUCTION │ │  CHALLAN    │ │  BANKING     │
│             │ │              │ │             │ │              │
│ S1: Received│ │ S5: Approved │ │ S7: Challan │ │ S9: LC Open  │
│ S2: Making  │ │ S6: Producing│ │ S8: PI Done │ │ S10: Matured │
│ S3: Sent    │ │              │ │             │ │              │
│ S4: Correct │ │              │ │             │ │              │
└─────────────┘ └──────────────┘ └─────────────┘ └──────────────┘

  Most active         After           Finance         End game
  (daily work)      approval         documents       (wait for $)
```

### 7.4 Status Badge Colors

| Badge | Color | Hex | Meaning |
|---|---|---|---|
| Order Received | Grey | `#6b7280` | New, no action taken yet |
| Sample In Progress | Blue | `#4d96f0` | Work happening |
| Sample Sent | Light Blue | `#60a5fa` | Waiting for reply |
| Correction Needed | Red | `#ef4444` | Action needed! |
| Sample Approved | Green | `#10b981` | Good to go |
| Bulk Production | Amber | `#f59e0b` | Manufacturing |
| Challan Issued | Purple | `#a855f7` | Goods shipped |
| PI Done | Light Purple | `#c084fc` | Invoice sent |
| LC Open | Orange | `#f97316` | Waiting for maturity |
| Matured | Dark Green | `#059669` | Complete ✓ |

---

## 8. Document Generation Guide

### 8.1 Delivery Challan

**What is it?** A dispatch receipt that accompanies goods when shipped to the buyer.

**Steps:**
1. Go to **Documents → Challans**
2. Click **"+ New Challan"**
3. Link to the order (auto-fills buyer name + address)
4. Add line items:
   - Style / Description
   - Quantity
   - Unit
5. Enter dispatch date
6. Review the preview
7. Click **"Print"** for paper copy or **"Download PDF"** for digital

**What auto-fills from the system:**
- IKON company letterhead (name, address, phone)
- Challan number (auto-generated: CH-2026-015)
- Buyer name and address (from company record)
- Signature blocks

---

### 8.2 Proforma Invoice (PI)

**What is it?** A detailed invoice listing all items, prices, and payment terms. Sent to the buyer and bank.

**Steps:**
1. Go to **Documents → Proforma Invoices**
2. Click **"+ New PI"**
3. Link to the order (auto-fills buyer details)
4. Add line items:
   - SL No. (auto)
   - Description (Style name)
   - Quantity
   - Unit Price (in USD)
   - Total (auto-calculated: qty × price)
5. Review:
   - Grand total (auto-summed)
   - Amount in words (auto-generated)
   - Terms & Conditions (pre-filled, editable)
   - Banking details (pre-filled)
   - BIN/VAT (pre-filled)
6. Click **"Finalize"**
7. **"Print"** or **"Download PDF"**

**Example PI line items (from real IKON PI):**

| SL | Description | Qty | Unit | Unit Price | Total |
|---|---|---|---|---|---|
| 1 | Satin Label (Style SH-204) | 500 | DOZ | $0.85 | $425.00 |
| 2 | Customer Care Label | 500 | DOZ | $0.45 | $225.00 |
| 3 | Elastic 2.5cm | 1,200 | YDS | $0.12 | $144.00 |
| 4 | Horn Button 18L | 50 | GROSS | $3.50 | $175.00 |

**Standard Terms (pre-filled):**
- Shipper's inspection shall be final
- Partial shipment: Allowed
- Transshipment: Prohibited
- Shipment from: Uttara factory premises
- Consignment takeover: Within 7 working days of delivery
- Payment: By Irrevocable L/C at 60/90 days sight
- Advising Bank: COMMUNITY BANK LTD, Uttara Branch
- Swift: COYMBDDD
- A/C: 0100310654101
- Currency: US Dollar
- BIN/VAT: 003543528-0102

---

### 8.3 LC Document Pack

**What the bank needs (checklist in LC Tracker):**

| Document | What it is | Where it comes from |
|---|---|---|
| ☐ Commercial Invoice | Official invoice with goods descriptions | Can be similar to PI or separate |
| ☐ Packing List | Details of how goods are packed (cartons, weights) | Manual entry |
| ☐ Delivery Challan | Proof of dispatch | Generated in the system |
| ☐ Bill of Exchange | Payment demand document | Manual entry (bank format) |

**Workflow:**
1. Prepare all 4 documents
2. Open LC record in system
3. Check off each document as you submit to bank
4. Enter bank forwarding date
5. System tracks until maturity (90 days)

---

## 9. Alerts & What They Mean

### 9.1 Dashboard Alert Strip

The alert strip at the top of the dashboard shows when something needs your attention:

| Alert | Meaning | Action Required |
|---|---|---|
| "**X LCs maturing within 14 days**" | LCs are approaching payment date | Go to LC Tracker, verify documents are submitted, coordinate with bank |
| "**X overdue sample corrections**" | Merchandiser asked for corrections Y+ days ago, no new revision logged | Make the corrected sample and log the new revision |
| "**X production deadlines at risk**" | Bulk production deadline is within 7 days but completion < 80% | Check factory progress, escalate if needed |
| "**X orders with no update in 7+ days**" | Orders are stale — no activity logged recently | Review and update status, or check with merchandiser |

### 9.2 Order Card Badges on Dashboard

| Badge | Color | Meaning |
|---|---|---|
| **Correction** | Red | Merchandiser wants changes — action needed |
| **Waiting** | Grey | Sent to merchandiser, waiting for response |
| **Sent** | Blue | Sample has been dispatched |
| **Bulk** | Yellow | In bulk production |
| **On Track** | Green | Production progressing well vs. deadline |
| **At Risk** | Orange | Production behind schedule |
| **Draft** | Grey outline | Order saved but not yet formally submitted |
| **Urgent** | Red pulse | Deadline within 3 days |
| **Soon** | Amber | LC maturing within 14–30 days |

---

## 10. Settings & System Configuration

### 10.1 What to Configure (Settings Page)

| Section | Fields | Used In |
|---|---|---|
| **Company Information** | Company name, address, phone, email, logo | PI letterhead, Challan letterhead |
| **Banking Details** | Bank name, branch, Swift code, account number | PI (auto-filled) |
| **Tax Information** | BIN/VAT number | PI (auto-filled) |
| **Terms & Conditions** | Standard PI terms text | PI (auto-filled, editable per PI) |
| **Product Catalogue** | List of product types (Satin Label, Elastic, etc.) | New Order form dropdown |
| **Unit Catalogue** | List of units (DOZ, YDS, PCS, GROSS, etc.) | New Order form, PI, Challan |

### 10.2 When to Update Settings

- **Banking details change** → update immediately (affects all new PIs)
- **New product type appears frequently** → add to catalogue
- **Terms & Conditions updated** → modify template (existing PIs keep their original terms)
- **New unit needed** → add to unit catalogue

---

## 11. Tips & Best Practices

### 11.1 Daily Routine

```
MORNING (5 minutes):
1. Open Dashboard
2. Check alert strip — anything urgent?
3. Scan pipeline columns — any order stuck too long?
4. Note which merchandisers to follow up with

DURING THE DAY:
- Merchandiser visits → create order or update revision immediately (don't wait)
- Sample sent → log it immediately (date accuracy matters)
- Feedback received → update revision result immediately

END OF DAY:
- Quick scan: did I log everything that happened today?
- Any orders that need a status update?
```

### 11.2 Data Entry Tips

| Tip | Why |
|---|---|
| **Log revisions the same day** you send a sample | Date tracking is only useful if dates are accurate |
| **Always enter merchandiser feedback** in revision notes | You'll forget what they said in 2 weeks |
| **Use internal notes** for factory-side details | Separate from merchandiser's feedback |
| **Upload reference images** when orders are complex | Words alone are ambiguous for garment specs |
| **Save as draft** when you don't have all details yet | Better than not logging at all |
| **Update completion %** weekly for bulk production | Keeps "at risk" alerts accurate |
| **Check off LC documents** as you submit them | Easy to forget which docs are pending |

### 11.3 Searching & Filtering

| To find... | Search by... |
|---|---|
| A specific order | Style name (e.g., "SH-204") or order number (e.g., "F-2026-039") |
| All orders from a buyer | Company name |
| All orders from one merchandiser | Merchandiser name |
| All orders needing correction | Filter by pipeline stage: "Correction Needed" |
| Overdue orders | Sort by "Days Active" descending |
| Orders about to be delivered | Filter by pipeline stage: "Bulk Production" + sort by deadline |

### 11.4 Common Mistakes to Avoid

| Mistake | What happens | How to avoid |
|---|---|---|
| Creating an order without selecting the right company | Merchandiser appears under wrong company; documents have wrong buyer name | Always double-check company selection before saving |
| Forgetting to mark a sample as "Sent" | Pipeline stays at "In Progress"; dashboard shows wrong status | Log it the moment you hand off the sample |
| Not entering the merchandiser's deadline | No deadline alerts; "at risk" detection doesn't work | Always ask the merchandiser for their timeline |
| Entering LC open date wrong | Maturity countdown is wrong (90-day calculation off) | Double-check against the physical LC document |
| Skipping the challan and going straight to PI | Pipeline stages get confused | Follow the order: Challan first, then PI, then LC |

---

## 12. FAQ

### General

**Q: Can I access it from my phone?**  
A: Yes, the system is web-based and works in any browser. Responsive design adapts to mobile screens. (Full mobile optimization depends on decision D-08.)

**Q: What happens if my internet goes down?**  
A: If deployed on cloud — the system is unavailable until internet returns. Your data is safe on the server. (Local deployment option being evaluated.)

**Q: Can two people use it at the same time?**  
A: Yes. Multiple users can be logged in simultaneously. Each person sees the same data in real-time.

### Orders

**Q: Can I delete an order?**  
A: Not if it has revisions, challans, PIs, or LCs attached. You can archive it instead. This prevents accidental data loss.

**Q: What if one merchandiser orders multiple products in one visit?**  
A: Create one order per style/product. Each order tracks separately through the pipeline. One merchandiser can have 10+ active orders.

**Q: Can I change an order number?**  
A: No. Order numbers are auto-generated and permanent. This ensures traceability.

**Q: What if I created an order under the wrong company?**  
A: Edit the order and change the company/merchandiser fields. The activity log will record the change.

### Samples

**Q: How many revisions is normal?**  
A: Simple items: 2–3 revisions. Complex items: 5–8. Some difficult orders: 10+. The system handles unlimited revisions.

**Q: What if the merchandiser approves verbally but hasn't seen the latest sample?**  
A: Don't mark as approved until they've actually seen and confirmed. Mark the revision as "Sent" and wait for formal approval.

### Documents

**Q: Can I edit a PI after printing it?**  
A: Yes, but the system keeps version history. The printed version doesn't change — only the digital record. For client-facing changes, create a new PI.

**Q: Where do PIs get their totals?**  
A: Auto-calculated from line items. You enter quantity × unit price per row; the system calculates everything else.

**Q: Can I create a challan for multiple orders at once?**  
A: Yes — add multiple line items from different styles/orders into one challan.

### LC

**Q: What if the LC maturity is not exactly 90 days?**  
A: The system defaults to 90 days (standard). If your buyer's LC terms differ, this will be configurable in a future update.

**Q: What happens when an LC matures?**  
A: The system alerts you starting 14 days before. On maturity day (or when you confirm payment), mark it as Matured. The order moves to Stage 10 (complete).

---

*End of User Documentation*

*This document should be updated as new features are added and as open design decisions (D-01 through D-10) are resolved.*
