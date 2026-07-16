# Software Requirements Specification (SRS)

## IKON Garments Accessories — Order & Export Management System

| Field | Detail |
|---|---|
| **Document version** | 1.0 |
| **Date** | April 9, 2026 |
| **Prepared for** | Muhammad Nezam Uddin, Proprietor — IKON Garments Accessories |
| **Business address** | Uttara, Dhaka-1230, Bangladesh |
| **Project codename** | Zeno (used in prototypes) |
| **Current phase** | Strategy & Mockup (Phase 0–1) |

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Overall Description](#2-overall-description)
3. [System Features & Functional Requirements](#3-system-features--functional-requirements)
4. [Data Model & Entity Definitions](#4-data-model--entity-definitions)
5. [External Interface Requirements](#5-external-interface-requirements)
6. [Non-Functional Requirements](#6-non-functional-requirements)
7. [Pipeline & Workflow Definitions](#7-pipeline--workflow-definitions)
8. [Screen Specifications](#8-screen-specifications)
9. [Business Rules & Constraints](#9-business-rules--constraints)
10. [Future Enhancements (Phase 2+)](#10-future-enhancements-phase-2)
11. [Assumptions & Dependencies](#11-assumptions--dependencies)
12. [Glossary](#12-glossary)
13. [Appendices](#13-appendices)

---

## 1. Introduction

### 1.1 Purpose

This document defines the complete software requirements for the **IKON Garments Accessories Order & Export Management System** — a web-based application designed to manage the full lifecycle of garment accessories orders from initial placement through sample revisions, bulk production, export documentation, and LC (Letter of Credit) maturity.

This SRS serves as the authoritative reference for developers, designers, testers, and stakeholders throughout the project.

### 1.2 Scope

The system will:

- Track **100+ concurrent orders** from multiple buyer companies and merchandisers, each at different pipeline stages spanning weeks to months.
- Replace the current manual, paper-based, and memory-dependent workflow with a single digital platform.
- Manage the complete order lifecycle: Order → Sample (multiple revision loops) → Approval → Bulk Production → Delivery Challan → Proforma Invoice (PI) → LC tracking → Bank forwarding → LC maturity.
- Generate printable/PDF export documents: Delivery Challans, Proforma Invoices, Commercial Invoices, Packing Lists, and Bills of Exchange.
- Track vendor/outsource relationships for sample making.
- Provide operational modules for Inventory, Accounts, HR & Payroll, and Vehicle/Fleet Management.
- Send alerts for approaching deadlines (LC maturity, overdue samples, production deadlines).

The system will **NOT** (in Phase 1):
- Integrate with external accounting software (e.g., Tally, QuickBooks).
- Provide e-commerce or online ordering capability.
- Integrate with Bangladesh Bank or any banking API directly.

### 1.3 Intended Audience

| Audience | Use of this document |
|---|---|
| Business owner (Nezam bhai) | Validate that all business requirements are captured |
| UI/UX designer | Screen specifications and workflow definitions |
| Frontend developer | Screen list, field definitions, validation rules |
| Backend developer | Data model, business rules, API scope |
| QA/Tester | Acceptance criteria, pipeline state transitions |

### 1.4 Definitions & Abbreviations

| Term | Meaning |
|---|---|
| LC | Letter of Credit — a bank-guaranteed payment instrument used in export trade |
| PI | Proforma Invoice — a preliminary bill sent to the buyer before shipment |
| Challan | Delivery Challan — a dispatch/delivery receipt document |
| Merchandiser | A buyer's representative who places orders, reviews samples, and approves production |
| Pipeline | The sequence of stages an order moves through from placement to completion |
| Revision | One round of sample creation + feedback. Orders may go through 3–10+ revisions |
| Bulk | Full-scale production after sample approval |
| BIN | Business Identification Number (Bangladesh tax ID) |
| DOZ / YDS / PCS / GROSS | Units of measurement: Dozen, Yards, Pieces, Gross (144 pieces) |

---

## 2. Overall Description

### 2.1 Product Perspective

This is a **new, standalone** web application. There is no predecessor digital system. The business currently operates with:
- Paper notebooks and memory for order tracking.
- WhatsApp conversations for merchandiser communication.
- Manual Excel/Word for PI and Challan documents.
- No centralized system for tracking pipeline status, LC maturity, or production progress.

The application must function as a **long-running, multi-party pipeline workflow manager**, not a simple CRUD application.

### 2.2 Product Functions (High-Level)

| Function Group | Description |
|---|---|
| **Company & Merchandiser Management** | Register buyer companies; assign merchandisers under companies; maintain contact records |
| **Order Management** | Create orders; track through 10-stage pipeline; assign to merchandiser/company |
| **Sample Revision Tracking** | Log each revision round (in-house or outsourced); track send dates, feedback, corrections; mark final approval |
| **Bulk Production Tracking** | Track production quantity, start/end dates, completion %, deadline adherence |
| **Document Generation** | Generate Delivery Challan, PI, Commercial Invoice, Packing List, Bill of Exchange with IKON letterhead |
| **LC Lifecycle Tracking** | Record LC details, track document submission checklist, calculate maturity date, countdown alerts |
| **Inventory Management** | Track raw material stock levels, SKUs, suppliers, stock-in/stock-out transactions |
| **Accounts & Finance** | Income vs. expense tracking, monthly summaries, outstanding receivables |
| **HR & Payroll** | Employee directory, monthly salary register, leave request management |
| **Vehicle & Fleet Management** | Vehicle register, driver profiles, trip logs, fuel costs, maintenance records |
| **Dashboard & Alerts** | Real-time pipeline overview, KPI stat cards, urgent alerts for LC maturity and overdue items |
| **Reporting** | Orders by company, LC maturity calendar, revenue summary, overdue deliveries, pending corrections |

### 2.3 User Classes & Characteristics

| User Role | Description | Access Level |
|---|---|---|
| **Owner** | Muhammad Nezam Uddin. Full system control | Full access — all modules, settings, financials, user management |
| **Manager** | Senior staff handling daily operations | All operational modules; no system settings or sensitive financial data |
| **Staff / Factory** | Workers involved in sample making and production | View assigned orders, update sample status, log production progress |
| **View Only** | External stakeholders or temporary access | Read-only dashboard and order views; no edit capability |

> **Decision pending (D-03):** Confirm whether multi-user access is needed for Phase 1, or if the system will initially be single-user (owner only).

### 2.4 Operating Environment

| Aspect | Specification |
|---|---|
| **Platform** | Web application accessible via modern browsers |
| **Browsers** | Chrome (latest), Edge (latest), Firefox (latest), Safari (latest) |
| **Devices** | Desktop primary; responsive design for tablet/mobile access (pending D-08) |
| **Hosting** | Cloud-based (Vercel + Railway) or local server (pending D-04) |
| **Network** | Internet connection required for cloud deployment; option for local network deployment |
| **OS** | Cross-platform via browser (Windows, macOS, Linux, Android, iOS) |

### 2.5 Design & Implementation Constraints

- All business documents (PI, Challan) must follow IKON's existing letterhead format and include legally required fields (BIN/VAT, bank details).
- LC maturity calculation is fixed at **90 days from LC open date** (standard in Bangladesh garments export).
- Payment terms are **Irrevocable L/C at 60/90 days sight** — this must be pre-filled in PI templates.
- IKON's banking details are fixed: **COMMUNITY BANK LTD, Uttara Branch, Swift: COYMBDDD, A/C: 0100310654101**.
- BIN/VAT Number: **003543528-0102**.
- Product types include but are not limited to: Satin Label, Customer Care Label, Elastic, Horn Button, Woven Label, Zipper Pull.

---

## 3. System Features & Functional Requirements

### 3.1 Company Management

#### 3.1.1 Description
Register and manage all buyer companies that place orders with IKON.

#### 3.1.2 Functional Requirements

| ID | Requirement | Priority |
|---|---|---|
| **FR-CM-01** | System shall allow creating a new company with fields: name, country, contact person, phone, email, address | Must |
| **FR-CM-02** | System shall display a searchable list of all registered companies | Must |
| **FR-CM-03** | System shall display total orders and active orders count per company | Must |
| **FR-CM-04** | System shall allow editing company details | Must |
| **FR-CM-05** | System shall prevent deletion of a company that has associated orders (soft-delete or archive only) | Must |
| **FR-CM-06** | System shall support pagination when company count exceeds 20 | Should |

### 3.2 Merchandiser Management

#### 3.2.1 Description
Track individual merchandisers (buyer representatives) who are assigned under buyer companies.

#### 3.2.2 Functional Requirements

| ID | Requirement | Priority |
|---|---|---|
| **FR-MM-01** | System shall allow adding a merchandiser under a specific company with fields: name, phone, designation, email (optional), WhatsApp number (optional) | Must |
| **FR-MM-02** | System shall display all merchandisers grouped under their parent company | Must |
| **FR-MM-03** | System shall show active order count and current stage badges per merchandiser | Must |
| **FR-MM-04** | System shall allow editing merchandiser details | Must |
| **FR-MM-05** | System shall allow transferring a merchandiser from one company to another (with order history preserved) | Should |
| **FR-MM-06** | System shall display merchandiser avatar using name initials | Should |

### 3.3 Order Management

#### 3.3.1 Description
Create and manage garment accessories orders. This is the core entity — every other module connects to an order.

#### 3.3.2 Functional Requirements

| ID | Requirement | Priority |
|---|---|---|
| **FR-OM-01** | System shall allow creating a new order with fields: company (select), merchandiser (select/add), style name/number, product type (select from catalogue or free text), description/spec notes, expected quantity, unit (DOZ/YDS/GROSS/PCS/other), reference image upload (optional), order date (default: today) | Must |
| **FR-OM-02** | Each order shall have a unique auto-generated order number (format: `F-YYYY-NNN`, e.g., F-2026-039) | Must |
| **FR-OM-03** | System shall track a **status field** for each order that moves through 10 pipeline stages (see §7) | Must |
| **FR-OM-04** | System shall allow saving an order as **Draft** before formal submission | Must |
| **FR-OM-05** | System shall display all orders in a searchable, filterable, sortable table | Must |
| **FR-OM-06** | System shall allow filtering orders by: company, merchandiser, pipeline stage, date range, product type | Must |
| **FR-OM-07** | System shall calculate and display **days active** (days since order was created) | Must |
| **FR-OM-08** | System shall allow editing order details at any pipeline stage (with audit log) | Must |
| **FR-OM-09** | System shall support attaching files/images to an order (reference images, buyer specs) | Should |
| **FR-OM-10** | System shall display a full **activity timeline** showing every status change, revision, and update with timestamps | Must |

### 3.4 Sample Revision Tracking

#### 3.4.1 Description
The most complex operational process. A single order can go through 3–10+ revision rounds before sample approval. Each round involves making a sample (in-house or outsourced), sending it to the merchandiser, receiving feedback, and iterating.

#### 3.4.2 Functional Requirements

| ID | Requirement | Priority |
|---|---|---|
| **FR-SR-01** | System shall allow adding a new revision to an order with fields: revision number (auto-incremented), type (in-house / outsourced), vendor name and location (if outsourced), date sample made, date sent to merchandiser, result (pending / correction needed / approved), merchandiser feedback (text), internal notes (text) | Must |
| **FR-SR-02** | System shall display revision history for an order as a chronological list, newest first | Must |
| **FR-SR-03** | System shall show status badge per revision: In Progress, Sent, Correction Needed, Approved | Must |
| **FR-SR-04** | System shall auto-transition order pipeline from "Sample in progress" → "Sample sent" when a revision is marked as sent | Must |
| **FR-SR-05** | System shall auto-transition order pipeline from "Sample sent" → "Correction needed" when a revision is marked with corrections | Must |
| **FR-SR-06** | When any revision is marked **"Approved"**, the system shall transition the order pipeline to **"Sample approved"** and unlock the bulk production section | Must |
| **FR-SR-07** | System shall support attaching photos/files to each revision (sample photos, feedback screenshots) | Should |
| **FR-SR-08** | System shall track total number of revisions per order and display it on the order card | Must |
| **FR-SR-09** | System shall allow editing a previously submitted revision (with timestamp update in activity log) | Must |
| **FR-SR-10** | System shall track which outsource vendor was used per revision (linking to vendor records) | Should |

### 3.5 Bulk Production Tracking

#### 3.5.1 Description
After sample approval, the order enters bulk production. This section is **locked** until sample approval occurs.

#### 3.5.2 Functional Requirements

| ID | Requirement | Priority |
|---|---|---|
| **FR-BP-01** | Bulk production section shall be **locked** and display "Unlocks after sample approval" message until a sample revision is marked as approved | Must |
| **FR-BP-02** | System shall allow entering bulk production details: quantity to produce, unit, production start date, merchandiser delivery deadline, completion %, milestone notes | Must |
| **FR-BP-03** | System shall auto-calculate production status: On Track (deadline > 7 days away + completion progressing), At Risk (deadline approaching + low completion), Completed (100%) | Must |
| **FR-BP-04** | System shall allow updating completion % progressively (e.g., 25% → 50% → 75% → 100%) | Must |
| **FR-BP-05** | System shall transition order pipeline to "Bulk production" stage when production details are first entered | Must |
| **FR-BP-06** | System shall send an alert when production deadline is within 7 days and completion < 80% | Should |

### 3.6 Delivery Challan Generation

#### 3.6.1 Description
Generate and print dispatch/delivery challan documents with IKON letterhead.

#### 3.6.2 Functional Requirements

| ID | Requirement | Priority |
|---|---|---|
| **FR-DC-01** | System shall generate a Delivery Challan document with: IKON letterhead (auto), challan number (auto-generated), date, buyer name and address (from company record), items table (style / description / quantity / unit), dispatch date | Must |
| **FR-DC-02** | System shall auto-populate buyer details from the linked company record | Must |
| **FR-DC-03** | System shall allow adding multiple line items to a single challan | Must |
| **FR-DC-04** | System shall provide a **print-friendly** view (CSS print layout) | Must |
| **FR-DC-05** | System shall generate a **downloadable PDF** of the challan | Should |
| **FR-DC-06** | System shall transition order pipeline to "Challan issued" stage when a challan is created for that order | Must |
| **FR-DC-07** | System shall include signature blocks for "Received by" and "Issued by" | Must |

### 3.7 Proforma Invoice (PI) Generation

#### 3.7.1 Description
Generate PI documents matching IKON's established format (as seen in real PI document `05-images/Screenshot_104.png`).

#### 3.7.2 Functional Requirements

| ID | Requirement | Priority |
|---|---|---|
| **FR-PI-01** | System shall generate a PI with: IKON letterhead, PI number (format: `PI-YYYY/NN`), date, buyer address block (from company record) | Must |
| **FR-PI-02** | System shall include a line items table with columns: SL No., Description (Style), Quantity, Unit Price, Total Amount | Must |
| **FR-PI-03** | System shall auto-calculate row totals (qty × unit price) and grand total | Must |
| **FR-PI-04** | System shall display the grand total in words (e.g., "US DOLLAR TWENTY-FIVE THOUSAND THREE HUNDRED FIFTY ONLY") | Must |
| **FR-PI-05** | System shall pre-fill standard Terms & Conditions: shipper inspection final, partial shipment allowed, transshipment prohibited, shipment from Uttara factory, consignment takeover within 7 days, Payment: Irrevocable L/C 60/90 days sight | Must |
| **FR-PI-06** | System shall pre-fill banking details: COMMUNITY BANK LTD, Uttara Branch, Swift: COYMBDDD, A/C: 0100310654101 | Must |
| **FR-PI-07** | System shall include BIN/VAT: 003543528-0102 | Must |
| **FR-PI-08** | System shall include "Accepted by" and "Issued By" signature blocks | Must |
| **FR-PI-09** | System shall provide print-friendly view and PDF download | Should |
| **FR-PI-10** | System shall transition order pipeline to "PI done" stage when a PI is created for that order | Must |
| **FR-PI-11** | System shall allow editing a PI after creation (with version history) | Should |

### 3.8 LC (Letter of Credit) Tracking

#### 3.8.1 Description
Track the LC lifecycle from opening to maturity (90 days).

#### 3.8.2 Functional Requirements

| ID | Requirement | Priority |
|---|---|---|
| **FR-LC-01** | System shall allow recording LC details: LC number, open date, issuing bank name, associated PI/order | Must |
| **FR-LC-02** | System shall **auto-calculate maturity date** as `open_date + 90 days` | Must |
| **FR-LC-03** | System shall display a **countdown timer** showing days until maturity | Must |
| **FR-LC-04** | System shall display countdown in **red** when maturity is within 14 days | Must |
| **FR-LC-05** | System shall provide a documents submitted **checklist**: Commercial Invoice, Packing List, Delivery Challan, Bill of Exchange — each toggleable independently | Must |
| **FR-LC-06** | System shall track bank forwarding date and forwarding status | Must |
| **FR-LC-07** | System shall support LC status values: Open → Forwarded → Matured | Must |
| **FR-LC-08** | System shall transition order pipeline to "LC open" when an LC is created, and "Matured" when LC status changes to Matured | Must |
| **FR-LC-09** | System shall display an alert on the dashboard for all LCs maturing within 14 days | Must |
| **FR-LC-10** | System shall allow adding notes to an LC record | Should |

### 3.9 Dashboard

#### 3.9.1 Description
The daily command center. Provides at-a-glance visibility of all active orders, pipeline distribution, and urgent items.

#### 3.9.2 Functional Requirements

| ID | Requirement | Priority |
|---|---|---|
| **FR-DB-01** | Dashboard shall display 4 stat cards: Active Orders (total), Pending Corrections (orders awaiting sample revision), Approved This Month (sample approvals), LC Maturing (within 90 days) | Must |
| **FR-DB-02** | Dashboard shall display an **alert strip** showing urgent items: LCs maturing within 14 days, overdue sample returns, production deadlines at risk | Must |
| **FR-DB-03** | Dashboard shall display a **pipeline column view** with 4 groupings: Sample Stage, Bulk Production, PI/Challan, LC & Banking — each column showing relevant order cards | Must |
| **FR-DB-04** | Each order card in the pipeline view shall show: style name, merchandiser + company, revision number, days active, status badge | Must |
| **FR-DB-05** | Dashboard shall include a **quick search** bar that searches across all orders by style name, merchandiser name, company name, or order number | Must |
| **FR-DB-06** | Dashboard shall include quick-action buttons: "+ Company" and "+ New Order" | Must |
| **FR-DB-07** | Pipeline columns shall show 3–5 order cards with a "+X more" link when overflow occurs | Should |
| **FR-DB-08** | Alert strip shall only display when there are actionable urgent items | Should |

### 3.10 Inventory Management

#### 3.10.1 Description
Track raw material stock for accessories production.

#### 3.10.2 Functional Requirements

| ID | Requirement | Priority |
|---|---|---|
| **FR-IN-01** | System shall maintain a stock register with: SKU code, item name, category, current quantity, unit, minimum stock level, supplier name | Must |
| **FR-IN-02** | System shall display visual stock level bars (green/yellow/red based on min threshold) | Should |
| **FR-IN-03** | System shall allow logging stock-in and stock-out transactions with date, quantity, reference (order number or supplier), and notes | Must |
| **FR-IN-04** | System shall alert when stock falls below minimum level | Should |
| **FR-IN-05** | System shall display transaction history per item | Must |

### 3.11 Accounts & Finance

#### 3.11.1 Description
Basic income and expense tracking for the business.

#### 3.11.2 Functional Requirements

| ID | Requirement | Priority |
|---|---|---|
| **FR-AC-01** | System shall allow recording income entries (linked to PI/order/LC payments) with: date, amount, source, category, reference | Must |
| **FR-AC-02** | System shall allow recording expense entries with: date, amount, payee, category, reference, notes | Must |
| **FR-AC-03** | System shall display monthly income vs. expense summary with bar chart visualization | Should |
| **FR-AC-04** | System shall maintain a transaction ledger (all entries, sortable and filterable) | Must |
| **FR-AC-05** | System shall track outstanding receivables (PI issued but not yet paid / LC not yet matured) | Must |
| **FR-AC-06** | System shall display total receivables amount and aging breakdown | Should |

### 3.12 HR & Payroll

#### 3.12.1 Description
Employee directory and basic payroll management.

#### 3.12.2 Functional Requirements

| ID | Requirement | Priority |
|---|---|---|
| **FR-HR-01** | System shall maintain employee directory with: name, designation, department, phone, join date, salary amount, status (active/inactive) | Must |
| **FR-HR-02** | System shall generate monthly salary register showing all employees, their salary, deductions, and net pay | Must |
| **FR-HR-03** | System shall maintain a 6-month salary history grid per employee | Should |
| **FR-HR-04** | System shall support leave request creation and approval workflow | Should |
| **FR-HR-05** | System shall track attendance summary per month | Could |

### 3.13 Vehicle & Fleet Management

#### 3.13.1 Description
Track delivery vehicles, drivers, trips, and associated costs.

#### 3.13.2 Functional Requirements

| ID | Requirement | Priority |
|---|---|---|
| **FR-VH-01** | System shall maintain a vehicle register with: registration number, type, make/model, year, status (active/maintenance/retired) | Must |
| **FR-VH-02** | System shall maintain driver profiles with: name, phone, license number, assigned vehicle | Must |
| **FR-VH-03** | System shall allow logging trips with: date, driver, vehicle, origin, destination, purpose, km/mileage | Must |
| **FR-VH-04** | System shall track fuel costs per vehicle with: date, litres, cost, odometer reading | Should |
| **FR-VH-05** | System shall log maintenance/repair records per vehicle with: date, description, cost, vendor | Should |

### 3.14 Vendor / Outsource Management

#### 3.14.1 Description
Maintain a directory of outsource vendors used for sample making and specialized production.

#### 3.14.2 Functional Requirements

| ID | Requirement | Priority |
|---|---|---|
| **FR-VN-01** | System shall maintain a vendor directory with: vendor name, location (Mirpur / Gilistan / other), item types they handle, contact person, phone | Must |
| **FR-VN-02** | System shall display order history per vendor (which orders used this vendor, dates, outcomes) | Should |
| **FR-VN-03** | System shall allow linking a sample revision to a vendor record | Should |
| **FR-VN-04** | System shall track cost per job (if provided) | Could |

### 3.15 Reporting

#### 3.15.1 Description
Summary views and exportable reports.

#### 3.15.2 Functional Requirements

| ID | Requirement | Priority |
|---|---|---|
| **FR-RP-01** | System shall provide an "Orders by Company" report (filterable by date range: this month / this year / custom) | Must |
| **FR-RP-02** | System shall provide an "LC Maturity Calendar" view showing upcoming maturities | Must |
| **FR-RP-03** | System shall provide a "Revenue Summary" from PI amounts | Should |
| **FR-RP-04** | System shall provide a "Pending Corrections" report listing all orders in correction-needed status | Must |
| **FR-RP-05** | System shall provide an "Overdue Deliveries" report listing orders past their merchandiser deadline | Must |
| **FR-RP-06** | All reports shall be exportable as CSV or printable | Should |

### 3.16 Search & Navigation

#### 3.16.1 Functional Requirements

| ID | Requirement | Priority |
|---|---|---|
| **FR-SN-01** | System shall provide a **global search** accessible from every screen that searches across orders, companies, merchandisers, and LC records | Must |
| **FR-SN-02** | System shall provide a persistent sidebar navigation with sections: Dashboard, Orders, Companies, Documents (Challans, PIs, LC Tracker), Inventory, Accounts, HR & Payroll, Vehicles, Vendors, Reports, Settings | Must |
| **FR-SN-03** | System shall maintain breadcrumb navigation on all detail pages (e.g., Dashboard → Company → Merchandiser → Order) | Should |

### 3.17 Settings

#### 3.17.1 Functional Requirements

| ID | Requirement | Priority |
|---|---|---|
| **FR-ST-01** | System shall store IKON company information (name, address, phone, email) used in all generated documents | Must |
| **FR-ST-02** | System shall store banking details (bank name, branch, Swift code, account number) pre-filled in PIs | Must |
| **FR-ST-03** | System shall store standard Terms & Conditions text pre-filled in PIs | Must |
| **FR-ST-04** | System shall store BIN/VAT number | Must |
| **FR-ST-05** | System shall allow managing the product type catalogue (add/edit/remove items) | Should |
| **FR-ST-06** | System shall allow managing the unit catalogue (DOZ, YDS, PCS, GROSS, custom) | Should |

---

## 4. Data Model & Entity Definitions

### 4.1 Entity Relationship Overview

```
Company (1) ──── (M) Merchandiser
                       │
                       └──── (M) Order
                                   │
                                   ├──── (M) SampleRevision ──── (0..1) Vendor
                                   │
                                   ├──── (0..1) BulkProduction
                                   │
                                   ├──── (M) DeliveryChallan
                                   │
                                   ├──── (0..1) ProformaInvoice ──── (M) PILineItem
                                   │
                                   ├──── (0..1) LCRecord
                                   │
                                   └──── (M) ActivityLog
```

### 4.2 Entity Field Definitions

#### 4.2.1 Company

| Field | Type | Required | Notes |
|---|---|---|---|
| id | UUID/Serial | Auto | Primary key |
| name | String(255) | Yes | e.g., "RIO DESIGN LIMITED" |
| country | String(100) | No | Default: Bangladesh |
| contact_person | String(255) | No | Primary contact name |
| phone | String(20) | No | |
| email | String(255) | No | |
| address | Text | No | Full address |
| created_at | Timestamp | Auto | |
| updated_at | Timestamp | Auto | |
| is_active | Boolean | Auto | Default: true (for soft-delete) |

#### 4.2.2 Merchandiser

| Field | Type | Required | Notes |
|---|---|---|---|
| id | UUID/Serial | Auto | Primary key |
| company_id | FK → Company | Yes | Parent company |
| name | String(255) | Yes | |
| phone | String(20) | No | |
| designation | String(100) | No | e.g., "Senior Merchandiser" |
| email | String(255) | No | |
| whatsapp | String(20) | No | |
| created_at | Timestamp | Auto | |
| updated_at | Timestamp | Auto | |
| is_active | Boolean | Auto | Default: true |

#### 4.2.3 Order

| Field | Type | Required | Notes |
|---|---|---|---|
| id | UUID/Serial | Auto | Primary key |
| order_number | String(20) | Auto | Format: F-YYYY-NNN |
| merchandiser_id | FK → Merchandiser | Yes | |
| style_name | String(255) | Yes | Buyer's style code/name |
| product_type | String(255) | Yes | From catalogue or free text |
| description | Text | No | Specs, dimensions, materials |
| expected_qty | Decimal | No | |
| unit | String(20) | No | DOZ / YDS / PCS / GROSS |
| pipeline_stage | Enum(1–10) | Auto | Default: 1 (Order Received) |
| is_draft | Boolean | Auto | Default: false |
| order_date | Date | Yes | Default: today |
| reference_image_url | String(500) | No | |
| created_at | Timestamp | Auto | |
| updated_at | Timestamp | Auto | |

#### 4.2.4 SampleRevision

| Field | Type | Required | Notes |
|---|---|---|---|
| id | UUID/Serial | Auto | Primary key |
| order_id | FK → Order | Yes | |
| revision_number | Integer | Auto | Auto-increment per order (R1, R2, R3…) |
| type | Enum | Yes | "in_house" / "outsourced" |
| vendor_id | FK → Vendor | Conditional | Required if type = outsourced |
| vendor_location | String(255) | No | e.g., "Mirpur" / "Gilistan" |
| date_made | Date | No | When sample was produced |
| date_sent | Date | No | When sent to merchandiser |
| result | Enum | Yes | "pending" / "correction_needed" / "approved" |
| merchandiser_feedback | Text | No | |
| internal_notes | Text | No | Factory-side notes |
| attachment_urls | JSON/Array | No | Photos, files |
| created_at | Timestamp | Auto | |
| updated_at | Timestamp | Auto | |

#### 4.2.5 BulkProduction

| Field | Type | Required | Notes |
|---|---|---|---|
| id | UUID/Serial | Auto | Primary key |
| order_id | FK → Order | Yes | Unique (one bulk per order) |
| quantity | Decimal | Yes | |
| unit | String(20) | Yes | |
| start_date | Date | No | |
| deadline | Date | Yes | Merchandiser's deadline |
| completion_pct | Integer | Auto | Default: 0, range 0–100 |
| status | Enum | Auto | "on_track" / "at_risk" / "completed" |
| milestone_notes | Text | No | |
| created_at | Timestamp | Auto | |
| updated_at | Timestamp | Auto | |

#### 4.2.6 DeliveryChallan

| Field | Type | Required | Notes |
|---|---|---|---|
| id | UUID/Serial | Auto | Primary key |
| order_id | FK → Order | Yes | |
| challan_number | String(30) | Auto | Auto-generated |
| date | Date | Yes | |
| dispatch_date | Date | No | |
| buyer_name | String(255) | Auto | From company record |
| buyer_address | Text | Auto | From company record |
| notes | Text | No | |
| created_at | Timestamp | Auto | |

#### 4.2.7 ChallanLineItem

| Field | Type | Required | Notes |
|---|---|---|---|
| id | UUID/Serial | Auto | Primary key |
| challan_id | FK → DeliveryChallan | Yes | |
| style | String(255) | Yes | |
| description | String(500) | No | |
| quantity | Decimal | Yes | |
| unit | String(20) | Yes | |

#### 4.2.8 ProformaInvoice

| Field | Type | Required | Notes |
|---|---|---|---|
| id | UUID/Serial | Auto | Primary key |
| order_id | FK → Order | Yes | |
| pi_number | String(20) | Auto | Format: PI-YYYY/NN |
| date | Date | Yes | |
| buyer_name | String(255) | Auto | From company record |
| buyer_address | Text | Auto | From company record |
| total_amount | Decimal | Auto | Sum of line items |
| total_in_words | String(500) | Auto | Generated from total_amount |
| terms_text | Text | Auto | From settings |
| created_at | Timestamp | Auto | |
| updated_at | Timestamp | Auto | |

#### 4.2.9 PILineItem

| Field | Type | Required | Notes |
|---|---|---|---|
| id | UUID/Serial | Auto | Primary key |
| pi_id | FK → ProformaInvoice | Yes | |
| sl_no | Integer | Yes | |
| description | String(500) | Yes | Style / product description |
| quantity | Decimal | Yes | |
| unit | String(20) | Yes | |
| unit_price | Decimal | Yes | |
| total | Decimal | Auto | quantity × unit_price |

#### 4.2.10 LCRecord

| Field | Type | Required | Notes |
|---|---|---|---|
| id | UUID/Serial | Auto | Primary key |
| order_id | FK → Order | Yes | |
| lc_number | String(50) | Yes | |
| open_date | Date | Yes | |
| maturity_date | Date | Auto | open_date + 90 days |
| issuing_bank | String(255) | No | |
| forwarding_date | Date | No | |
| status | Enum | Auto | "open" / "forwarded" / "matured" |
| doc_commercial_invoice | Boolean | Auto | Default: false |
| doc_packing_list | Boolean | Auto | Default: false |
| doc_delivery_challan | Boolean | Auto | Default: false |
| doc_bill_of_exchange | Boolean | Auto | Default: false |
| notes | Text | No | |
| created_at | Timestamp | Auto | |
| updated_at | Timestamp | Auto | |

#### 4.2.11 Vendor

| Field | Type | Required | Notes |
|---|---|---|---|
| id | UUID/Serial | Auto | Primary key |
| name | String(255) | Yes | |
| location | String(255) | No | Mirpur / Gilistan / etc. |
| item_types | Text | No | What they produce |
| contact_person | String(255) | No | |
| phone | String(20) | No | |
| created_at | Timestamp | Auto | |
| is_active | Boolean | Auto | Default: true |

#### 4.2.12 ActivityLog

| Field | Type | Required | Notes |
|---|---|---|---|
| id | UUID/Serial | Auto | Primary key |
| order_id | FK → Order | Yes | |
| action | String(255) | Yes | e.g., "Sample R3 sent", "Pipeline → Bulk production" |
| details | Text | No | Additional context |
| performed_by | FK → User | No | |
| created_at | Timestamp | Auto | |

#### 4.2.13 InventoryItem

| Field | Type | Required | Notes |
|---|---|---|---|
| id | UUID/Serial | Auto | Primary key |
| sku | String(50) | Yes | Unique |
| name | String(255) | Yes | |
| category | String(100) | No | |
| current_qty | Decimal | Auto | Calculated from transactions |
| unit | String(20) | Yes | |
| min_stock_level | Decimal | No | Alert threshold |
| supplier_name | String(255) | No | |
| created_at | Timestamp | Auto | |

#### 4.2.14 StockTransaction

| Field | Type | Required | Notes |
|---|---|---|---|
| id | UUID/Serial | Auto | Primary key |
| inventory_item_id | FK → InventoryItem | Yes | |
| type | Enum | Yes | "stock_in" / "stock_out" |
| quantity | Decimal | Yes | |
| date | Date | Yes | |
| reference | String(255) | No | Order number or supplier name |
| notes | Text | No | |
| created_at | Timestamp | Auto | |

#### 4.2.15 Employee

| Field | Type | Required | Notes |
|---|---|---|---|
| id | UUID/Serial | Auto | Primary key |
| name | String(255) | Yes | |
| designation | String(100) | No | |
| department | String(100) | No | |
| phone | String(20) | No | |
| join_date | Date | No | |
| salary_amount | Decimal | No | Monthly |
| status | Enum | Auto | "active" / "inactive" |
| created_at | Timestamp | Auto | |

#### 4.2.16 SalaryRecord

| Field | Type | Required | Notes |
|---|---|---|---|
| id | UUID/Serial | Auto | Primary key |
| employee_id | FK → Employee | Yes | |
| month | Date | Yes | First of the month |
| base_salary | Decimal | Yes | |
| deductions | Decimal | No | Default: 0 |
| net_pay | Decimal | Auto | base_salary - deductions |
| paid_date | Date | No | |
| notes | Text | No | |

#### 4.2.17 Vehicle

| Field | Type | Required | Notes |
|---|---|---|---|
| id | UUID/Serial | Auto | Primary key |
| registration_no | String(30) | Yes | |
| type | String(50) | No | e.g., "Truck", "Van", "Pickup" |
| make_model | String(100) | No | |
| year | Integer | No | |
| status | Enum | Auto | "active" / "maintenance" / "retired" |
| created_at | Timestamp | Auto | |

#### 4.2.18 Driver

| Field | Type | Required | Notes |
|---|---|---|---|
| id | UUID/Serial | Auto | Primary key |
| name | String(255) | Yes | |
| phone | String(20) | No | |
| license_number | String(50) | No | |
| assigned_vehicle_id | FK → Vehicle | No | |

#### 4.2.19 TripLog

| Field | Type | Required | Notes |
|---|---|---|---|
| id | UUID/Serial | Auto | Primary key |
| vehicle_id | FK → Vehicle | Yes | |
| driver_id | FK → Driver | No | |
| date | Date | Yes | |
| origin | String(255) | No | |
| destination | String(255) | No | |
| purpose | Text | No | |
| distance_km | Decimal | No | |

#### 4.2.20 User (Authentication)

| Field | Type | Required | Notes |
|---|---|---|---|
| id | UUID/Serial | Auto | Primary key |
| username | String(100) | Yes | Unique |
| password_hash | String(255) | Yes | Bcrypt/Argon2 hashed |
| full_name | String(255) | Yes | |
| role | Enum | Yes | "owner" / "manager" / "staff" / "viewer" |
| is_active | Boolean | Auto | Default: true |
| created_at | Timestamp | Auto | |
| last_login | Timestamp | Auto | |

---

## 5. External Interface Requirements

### 5.1 User Interfaces

| Screen | File Reference | Primary Function |
|---|---|---|
| Dashboard | `03-mockups/v2/01-dashboard.html` | Pipeline overview, stat cards, alerts, quick search |
| Companies & Merchandisers | `03-mockups/v2/02-companies.html` | Company directory with nested merchandiser cards |
| Order Detail | `03-mockups/v2/03-order-detail.html` | Full order file — info, revisions, timeline, locked sections |
| New Order Form | `03-mockups/v2/04-new-order.html` | Order creation form |
| Sample Revision Form | `03-mockups/v2/05-sample-revision.html` | Add/edit revision for an order |
| Proforma Invoice | `03-mockups/v2/06-pi.html` | PI generation and print view |
| LC Tracker | `03-mockups/v2/07-lc-tracker.html` | LC lifecycle management |
| Delivery Challan | `03-mockups/v2/08-challan.html` | Challan generation and print view |
| Future Vision | `03-mockups/v2/09-future-vision.html` | Phase 2+ feature roadmap |
| Inventory | `03-mockups/v2/10-inventory.html` | Raw material stock management |
| Accounts | `03-mockups/v2/11-accounts.html` | Income/expense tracking |
| HR & Payroll | `03-mockups/v2/12-hr-payroll.html` | Employee and salary management |
| Vehicles & Drivers | `03-mockups/v2/13-vehicles.html` | Fleet management |

### 5.2 Hardware Interfaces

None. The system is a web application accessed through standard browsers.

### 5.3 Software Interfaces

| Interface | Purpose |
|---|---|
| PostgreSQL | Primary data storage |
| Cloudflare R2 / AWS S3 | File storage for uploaded images, sample photos, and generated PDFs |
| WeasyPrint / react-pdf | PDF generation for PI, Challan, and LC documents |
| Clerk / NextAuth.js | Authentication and session management |

### 5.4 Communication Interfaces

| Protocol | Usage |
|---|---|
| HTTPS | All client-server communication (TLS 1.2+) |
| REST API | Frontend ↔ Backend data exchange (JSON) |
| SMTP (future) | Email notifications for alerts |

---

## 6. Non-Functional Requirements

### 6.1 Performance

| ID | Requirement |
|---|---|
| **NFR-P-01** | Dashboard shall load within **2 seconds** with up to 500 active orders |
| **NFR-P-02** | Order search shall return results within **500ms** for up to 10,000 records |
| **NFR-P-03** | PDF generation (PI/Challan) shall complete within **3 seconds** |
| **NFR-P-04** | Database queries shall be optimized with proper indexing on: order_number, pipeline_stage, company_id, merchandiser_id, lc_maturity_date |

### 6.2 Security (OWASP-Aligned)

| ID | Requirement | OWASP Risk |
|---|---|---|
| **NFR-S-01** | All passwords shall be hashed using bcrypt or Argon2 with salt. Never stored in plaintext. | A07 — Identification & Auth Failures |
| **NFR-S-02** | All database queries shall use parameterized queries / ORM. No raw SQL concatenation. | A03 — Injection |
| **NFR-S-03** | JWT tokens shall have **short expiry** (15 min access + 7 day refresh). Refresh tokens stored httpOnly. | A07 — Identification & Auth Failures |
| **NFR-S-04** | Server-side role checks on **every API route**. Frontend UI hiding is NOT sufficient authorization. | A01 — Broken Access Control |
| **NFR-S-05** | All communication over HTTPS. HTTP shall redirect to HTTPS. | A02 — Cryptographic Failures |
| **NFR-S-06** | CSRF protection via SameSite cookies + CSRF tokens on all state-changing requests. | A05 — Security Misconfiguration |
| **NFR-S-07** | All user inputs shall be validated on both client and server side. Rich-text inputs sanitized against XSS. | A03 — Injection |
| **NFR-S-08** | Environment variables for all secrets (API keys, DB credentials, JWT secret). Never committed to source control. | A05 — Security Misconfiguration |
| **NFR-S-09** | File uploads shall be validated for type, size (max 10MB), and content. Stored in external object storage, never served from application directory. | A08 — Software & Data Integrity |
| **NFR-S-10** | Rate limiting on authentication endpoints (max 5 failed attempts per 15 minutes per IP). | A07 — Identification & Auth Failures |

### 6.3 Reliability & Availability

| ID | Requirement |
|---|---|
| **NFR-R-01** | System shall have **99.5% uptime** (cloud deployment) or be available during business hours (local deployment) |
| **NFR-R-02** | Database shall be backed up **daily** with 30-day retention |
| **NFR-R-03** | System shall handle graceful degradation — if PDF generation fails, a print-friendly HTML view remains available |

### 6.4 Usability

| ID | Requirement |
|---|---|
| **NFR-U-01** | UI language: English with standard business terms (LC, PI, Challan, Style). Pending D-01. |
| **NFR-U-02** | System shall be learnable by a new user within **1 hour** of guided training |
| **NFR-U-03** | All clickable elements shall have `cursor: pointer` and visible hover states (150–300ms transition) |
| **NFR-U-04** | Text contrast shall meet **WCAG AA** minimum (4.5:1 ratio) |
| **NFR-U-05** | System shall respect `prefers-reduced-motion` for users who disable animations |
| **NFR-U-06** | All form fields shall show validation errors inline next to the field, not as a generic top-of-page message |
| **NFR-U-07** | Keyboard navigation shall be supported for all forms and primary actions |

### 6.5 Scalability

| ID | Requirement |
|---|---|
| **NFR-SC-01** | System shall support up to **50 concurrent users** without performance degradation |
| **NFR-SC-02** | Database shall support up to **50,000 orders** without query degradation |
| **NFR-SC-03** | File storage shall scale independently from application server |

### 6.6 Maintainability

| ID | Requirement |
|---|---|
| **NFR-M-01** | Codebase shall follow consistent code style enforced by linter (ESLint for JS, Black/Ruff for Python) |
| **NFR-M-02** | Database schema changes shall use migration scripts (Alembic for Python, Prisma for JS) |
| **NFR-M-03** | All API endpoints shall be documented via OpenAPI/Swagger (auto-generated if using FastAPI) |

### 6.7 Responsive Design

| ID | Requirement |
|---|---|
| **NFR-RD-01** | System shall be tested and functional at breakpoints: 375px (mobile), 768px (tablet), 1024px (laptop), 1440px (desktop) |
| **NFR-RD-02** | Dashboard pipeline columns shall collapse to a single column on mobile |
| **NFR-RD-03** | Document print views (PI, Challan) shall be optimized for A4 paper size |

---

## 7. Pipeline & Workflow Definitions

### 7.1 Order Pipeline Stages

Every order has exactly one `pipeline_stage` at any time. The stages and their transitions:

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│  1. Order Received                                                  │
│       │                                                             │
│       ▼                                                             │
│  2. Sample In Progress ◄──────┐                                     │
│       │                       │                                     │
│       ▼                       │                                     │
│  3. Sample Sent               │  (loop: correction → new revision)  │
│       │                       │                                     │
│       ├──► 4. Correction ─────┘                                     │
│       │         Needed                                              │
│       ▼                                                             │
│  5. Sample Approved                                                 │
│       │                                                             │
│       ▼                                                             │
│  6. Bulk Production                                                 │
│       │                                                             │
│       ▼                                                             │
│  7. Challan Issued                                                  │
│       │                                                             │
│       ▼                                                             │
│  8. PI Done                                                         │
│       │                                                             │
│       ▼                                                             │
│  9. LC Open                                                         │
│       │                                                             │
│       ▼                                                             │
│  10. Matured (Complete)                                             │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 7.2 Stage Definitions & Triggers

| Stage | Value | Entry Trigger | Exit Trigger | Allowed Actions |
|---|---|---|---|---|
| **1 — Order Received** | `order_received` | New order created (non-draft) | First sample revision created | Edit order details |
| **2 — Sample In Progress** | `sample_in_progress` | New revision added to order | Revision marked as "sent" | Add revision, edit order |
| **3 — Sample Sent** | `sample_sent` | Revision date_sent is set | Feedback received (correction or approved) | Wait for feedback, add notes |
| **4 — Correction Needed** | `correction_needed` | Revision marked "correction_needed" | New revision created (loops back to stage 2) | Add new revision, view feedback |
| **5 — Sample Approved** | `sample_approved` | Any revision marked "approved" | Bulk production started | Unlock bulk section, create production record |
| **6 — Bulk Production** | `bulk_production` | Bulk production record created | Delivery challan created | Update completion %, log milestones |
| **7 — Challan Issued** | `challan_issued` | Delivery challan generated | PI created | Edit challan, create PI |
| **8 — PI Done** | `pi_done` | PI generated | LC record created | Edit PI, create LC |
| **9 — LC Open** | `lc_open` | LC record created | LC matures (90 days) or manually marked | Update docs checklist, add bank forwarding |
| **10 — Matured** | `matured` | LC maturity date reached or manual mark | None (terminal state) | Archive, view history |

### 7.3 Stage Color Coding (UI)

| Stage | Badge Color | Hex |
|---|---|---|
| Order Received | Grey | `#6b7280` |
| Sample In Progress | Blue | `#4d96f0` |
| Sample Sent | Blue (light) | `#60a5fa` |
| Correction Needed | Red | `#ef4444` |
| Sample Approved | Green | `#10b981` |
| Bulk Production | Amber/Yellow | `#f59e0b` |
| Challan Issued | Purple | `#a855f7` |
| PI Done | Purple (light) | `#c084fc` |
| LC Open | Orange | `#f97316` |
| Matured | Green (solid) | `#059669` |

### 7.4 Pipeline Grouping for Dashboard Columns

| Dashboard Column | Stages Included |
|---|---|
| **Sample Stage** | 1 (Order Received), 2 (Sample In Progress), 3 (Sample Sent), 4 (Correction Needed) |
| **Bulk Production** | 5 (Sample Approved), 6 (Bulk Production) |
| **PI / Challan** | 7 (Challan Issued), 8 (PI Done) |
| **LC & Banking** | 9 (LC Open), 10 (Matured) |

---

## 8. Screen Specifications

### 8.1 SCR-01: Dashboard

| Aspect | Detail |
|---|---|
| **URL** | `/` or `/dashboard` |
| **Access** | All roles |
| **Mockup** | `03-mockups/v2/01-dashboard.html` |

**Layout:**
1. **Header bar** — current date, "+ Company" button, "+ New Order" button
2. **Alert strip** — conditional banner: "X LCs maturing within 14 days", "Y overdue corrections", "Z production deadlines at risk"
3. **4 Stat cards:**
   - Active Orders (total non-matured orders)
   - Pending Corrections (orders at stage 4)
   - Approved This Month (orders that reached stage 5 in current month)
   - LC Maturing (LCs maturing within 90 days)
4. **Pipeline column view** — 4 columns (see §7.4), each with order cards
5. **All Orders quick search table** — columns: Style | Merchandiser | Company | Stage | Days Active | Last Update

**Interactions:**
- Click any order card → navigate to Order Detail (SCR-03)
- Click "+ Company" → navigate to Company form
- Click "+ New Order" → navigate to New Order form (SCR-04)
- Click stat card → filter All Orders table to that category

---

### 8.2 SCR-02: Companies & Merchandisers

| Aspect | Detail |
|---|---|
| **URL** | `/companies` |
| **Access** | All roles (edit: owner/manager only) |
| **Mockup** | `03-mockups/v2/02-companies.html` |

**Layout:**
1. Page title + search bar + "+ Add Company" button
2. Company cards (one per company): name, country, contact person, phone, total orders, active orders, "Edit" + "All Orders" buttons
3. Under each company: merchandiser mini-cards (avatar initials, name, designation, active order count, stage badges)
4. "+ Add Merchandiser" button inside each company card
5. Pagination: show 20 companies per page

**Interactions:**
- Click "Edit" → inline edit or modal for company fields
- Click "All Orders" → navigate to Orders list filtered by that company
- Click merchandiser → navigate to Orders list filtered by that merchandiser
- Click "+ Add Merchandiser" → expand inline form or modal

---

### 8.3 SCR-03: Order Detail

| Aspect | Detail |
|---|---|
| **URL** | `/orders/:id` |
| **Access** | All roles (edit: owner/manager/staff) |
| **Mockup** | `03-mockups/v2/03-order-detail.html` |

**Layout:**
1. **Breadcrumb:** Dashboard → Company Name → Merchandiser Name → Order #
2. **Header:** Style name (large), pipeline stage badge, "Actions" dropdown (Edit, Delete, Archive)
3. **Subtitle:** Merchandiser name, Company, Order date, Days active
4. **Order Information card:** Style, Product type, Date, Merchandiser, Company, Quantity, Description — with "Edit" button
5. **Pipeline progress bar:** Visual 10-stage bar with current stage highlighted
6. **Sample Revisions section:**
   - List of all revision rounds (chronological, newest first)
   - Each: revision number, type (in-house/outsourced), vendor, date made, date sent, result, feedback, status badge
   - Action buttons: "Mark as Sent", "Mark Approved"
   - "+ Add Revision" button
7. **Activity Timeline** (right side or bottom): chronological log of all actions
8. **Bulk Production section:** LOCKED until stage ≥ 5, shows "Unlocks after sample approval" when locked
9. **Documents section:** Links to related Challan, PI, LC records (created from this screen or linked)

---

### 8.4 SCR-04: New Order Form

| Aspect | Detail |
|---|---|
| **URL** | `/orders/new` |
| **Access** | Owner, Manager |
| **Mockup** | `03-mockups/v2/04-new-order.html` |

**Fields:**
1. Company (searchable dropdown — required)
2. Merchandiser (searchable dropdown filtered by company — required; option to "+ Add new")
3. Style Name / Number (text — required)
4. Product Type (searchable dropdown from catalogue or free text — required)
5. Description / Spec Notes (textarea — optional)
6. Expected Quantity (number — optional)
7. Unit (dropdown: DOZ / YDS / GROSS / PCS / other — optional)
8. Reference Image Upload (file upload — optional, max 10MB, image types only)
9. Order Date (date picker — default: today)

**Buttons:** "Save as Draft" | "Create Order"

**Validation:**
- Company: must exist in system
- Style Name: required, max 255 characters
- Quantity: if provided, must be positive number

---

### 8.5 SCR-05: Sample Revision Form

| Aspect | Detail |
|---|---|
| **URL** | `/orders/:id/revisions/new` or `/orders/:id/revisions/:rid/edit` |
| **Access** | Owner, Manager, Staff |
| **Mockup** | `03-mockups/v2/05-sample-revision.html` |

**Fields:**
1. Revision Number (auto — read-only)
2. Order reference (auto — read-only, linked from order)
3. Type (radio: In-house / Outsourced — required)
4. Vendor Name (shown if Outsourced — searchable dropdown or free text)
5. Vendor Location (shown if Outsourced — dropdown: Mirpur / Gilistan / Other + custom)
6. Date Sample Made (date picker)
7. Date Sent to Merchandiser (date picker)
8. Result (radio: Pending / Correction Needed / Approved — required)
9. Merchandiser Feedback (textarea)
10. Internal Notes (textarea)
11. Attachments (file upload — multiple, images + PDFs, max 10MB each)

**Buttons:** "Save" | "Save & Mark Approved" (shown only when result = Approved)

---

### 8.6 SCR-06: Proforma Invoice (PI)

| Aspect | Detail |
|---|---|
| **URL** | `/documents/pi/new` or `/documents/pi/:id` |
| **Access** | Owner, Manager |
| **Mockup** | `03-mockups/v2/06-pi.html` |

**Layout (document view):**
1. IKON letterhead (company name, address, phone — from settings)
2. PI Number + Date
3. Buyer info block: company name + address (from company record)
4. Line items table: SL | Description (Style) | Quantity | Unit Price | Total
5. Grand total row + amount in words
6. Terms & Conditions (pre-filled from settings, editable per PI)
7. Banking details (pre-filled from settings)
8. BIN/VAT number (pre-filled from settings)
9. Signature blocks: "Accepted by ___" | "Issued By ___"

**Buttons:** "Add Line Item" | "Save Draft" | "Finalize" | "Print" | "Download PDF"

---

### 8.7 SCR-07: LC Tracker

| Aspect | Detail |
|---|---|
| **URL** | `/documents/lc` or `/documents/lc/:id` |
| **Access** | Owner, Manager |
| **Mockup** | `03-mockups/v2/07-lc-tracker.html` |

**Layout:**
1. LC Number + Open Date + Maturity Date (auto-calculated)
2. Countdown: "X days until maturity" — green (>30 days), amber (14–30), red (<14)
3. Document checklist (toggleable):
   - [ ] Commercial Invoice
   - [ ] Packing List
   - [ ] Delivery Challan
   - [ ] Bill of Exchange
4. Bank name + forwarding date
5. Status: Open → Forwarded → Matured (selectable)
6. Notes section
7. Linked PI and Order reference

---

### 8.8 SCR-08: Delivery Challan

| Aspect | Detail |
|---|---|
| **URL** | `/documents/challan/new` or `/documents/challan/:id` |
| **Access** | Owner, Manager |
| **Mockup** | `03-mockups/v2/08-challan.html` |

**Layout (document view):**
1. IKON letterhead
2. Challan number + date
3. Buyer name + address (from company record)
4. Items table: Style / Description / Quantity / Unit
5. Dispatch date
6. Signature blocks: "Received by ___" | "Issued by ___"

**Buttons:** "Add Line Item" | "Save" | "Print" | "Download PDF"

---

### 8.9 SCR-09: Future Vision

| Aspect | Detail |
|---|---|
| **URL** | `/vision` |
| **Mockup** | `03-mockups/v2/09-future-vision.html` |

Informational page showing the Phase 2+ roadmap (WhatsApp bot, QR stickers, voice-to-form, LC OCR scanning). No functional requirements — display only.

---

### 8.10 SCR-10: Inventory

| Aspect | Detail |
|---|---|
| **URL** | `/inventory` |
| **Access** | Owner, Manager, Staff |
| **Mockup** | `03-mockups/v2/10-inventory.html` |

**Layout:**
1. Stock register table: SKU | Item Name | Category | Qty | Unit | Stock Level Bar | Supplier
2. "+ Add Item" button
3. Search and filter by category / stock status (low/ok/high)
4. Click item → detail view with transaction history (stock-in, stock-out entries)
5. "+ Stock In" / "+ Stock Out" buttons per item

---

### 8.11 SCR-11: Accounts

| Aspect | Detail |
|---|---|
| **URL** | `/accounts` |
| **Access** | Owner only |
| **Mockup** | `03-mockups/v2/11-accounts.html` |

**Layout:**
1. Top summary: Total Income | Total Expense | Net P/L (current month)
2. Monthly bar chart: income vs. expense (last 6 or 12 months)
3. Transaction ledger table: Date | Type | Amount | Category | Reference | Notes
4. "+ Add Income" / "+ Add Expense" buttons
5. Outstanding receivables section: PI Reference | Amount | Days Outstanding

---

### 8.12 SCR-12: HR & Payroll

| Aspect | Detail |
|---|---|
| **URL** | `/hr` |
| **Access** | Owner, Manager |
| **Mockup** | `03-mockups/v2/12-hr-payroll.html` |

**Layout:**
1. Employee directory table: Name | Designation | Department | Phone | Salary | Status
2. "+ Add Employee" button
3. Monthly salary register: tab per month, shows all employees + deductions + net pay
4. 6-month salary history grid per employee (expandable row)
5. Leave request section: pending requests, approve/reject actions

---

### 8.13 SCR-13: Vehicles & Drivers

| Aspect | Detail |
|---|---|
| **URL** | `/vehicles` |
| **Access** | Owner, Manager |
| **Mockup** | `03-mockups/v2/13-vehicles.html` |

**Layout:**
1. Vehicle register cards: Reg No | Type | Make/Model | Status badge | Assigned Driver
2. "+ Add Vehicle" button
3. Click vehicle → detail: trip log, fuel cost log, maintenance log
4. Driver profiles section: Name | Phone | License | Assigned Vehicle
5. "+ Log Trip" / "+ Log Fuel" / "+ Log Maintenance" buttons

---

## 9. Business Rules & Constraints

### 9.1 Order Lifecycle Rules

| ID | Rule |
|---|---|
| **BR-01** | An order's pipeline stage can only move **forward** through the defined sequence, except for the correction loop (Stage 3 → 4 → 2 → 3) |
| **BR-02** | An order **cannot** be deleted if it has associated revisions, challans, PIs, or LC records. It can only be archived. |
| **BR-03** | Bulk production section is **inaccessible** until at least one sample revision is marked "approved" |
| **BR-04** | PI and Challan documents **auto-populate** buyer details from the linked company record — no manual re-entry |
| **BR-05** | LC maturity date is **always** calculated as `open_date + 90 days`. Manual override not permitted. |
| **BR-06** | Every status change on an order **automatically** creates an entry in the Activity Log |
| **BR-07** | An order number, once generated, **cannot** be changed |
| **BR-08** | A company **cannot** be deleted while it has active (non-matured) orders |
| **BR-09** | Marking an LC as "Matured" is **irreversible** — the order is considered complete |
| **BR-10** | PI total amount shall be **auto-calculated** from line items. Manual override of total not allowed. |

### 9.2 Document Numbering Rules

| Document | Format | Example | Sequence |
|---|---|---|---|
| Order Number | `F-YYYY-NNN` | F-2026-039 | Sequential per year, resets Jan 1 |
| PI Number | `PI-YYYY/NN` | PI-2025/02 | Sequential per year, resets Jan 1 |
| Challan Number | `CH-YYYY-NNN` | CH-2026-015 | Sequential per year, resets Jan 1 |
| LC Number | User-entered | Per issuing bank | N/A — matches bank-issued number |

### 9.3 Validation Rules

| Field | Rule |
|---|---|
| Phone numbers | 11 digits for BD numbers (01XXXXXXXXX), international format accepted |
| Email | Standard RFC 5322 email format |
| Quantities | Must be positive, max 2 decimal places |
| Unit prices | Must be positive, max 4 decimal places |
| Dates | Cannot be in the future for "date_made" or "date_sent" fields |
| File uploads | Max 10MB per file. Allowed types: JPG, PNG, PDF, WEBP |
| Text fields | Sanitized for XSS (no script tags, event handlers) |

---

## 10. Future Enhancements (Phase 2+)

These features are documented for planning but are explicitly **out of scope** for Phase 1.

| # | Feature | Description | Priority |
|---|---|---|---|
| **FE-01** | WhatsApp Bot | Order creation and status updates via WhatsApp messages. Buyer sends order text → bot creates draft → owner confirms. | High |
| **FE-02** | QR Code on Samples | Print QR stickers on physical sample packages. Scan to instantly open order, one-tap to update status. | High |
| **FE-03** | Voice-to-Form | Microphone button on new order form. Speak in Bangla/English → AI fills form fields. | Medium |
| **FE-04** | LC Document OCR | Photograph physical LC paper → OCR extracts LC number, bank, amount, dates → auto-fills LC tracker. | Medium |
| **FE-05** | Business Card Scan | Scan merchandiser's business card → auto-create merchandiser record. | Low |
| **FE-06** | Smart Suggestions | System learns patterns (e.g., "Noman Group always uses 90-day LC") and pre-fills fields. | Medium |
| **FE-07** | AI Chat Assistant | Natural language query: "Noman Group er sob orders ki status e ache?" → system responds with summary. | Low |
| **FE-08** | Auto WhatsApp Reminders | Auto-send follow-up messages to buyers when sample feedback is overdue (3+ days). | Medium |
| **FE-09** | WhatsApp Challan Delivery | After marking delivery → auto-send challan PDF to buyer on WhatsApp. | Low |
| **FE-10** | Multi-language Toggle | English / Bangla UI toggle. | Low |
| **FE-11** | Mobile App (PWA) | Progressive Web App for offline access and mobile-optimized experience. | Medium |

---

## 11. Assumptions & Dependencies

### 11.1 Assumptions

1. The business owner (Nezam bhai) will be the primary user during Phase 1. Multi-user access may be added later.
2. Internet connectivity is available at the office in Uttara, Dhaka.
3. Users have access to a modern web browser (Chrome/Edge preferred).
4. IKON's banking details and BIN/VAT number will not change frequently (stored in settings, editable by owner).
5. The 90-day LC maturity period is the standard used by all of IKON's buyer companies.
6. Product types are semi-fixed — the catalogue covers 80%+ of orders, with free-text for exceptions.
7. All monetary values in PIs and LCs are in **USD** (US Dollars) unless otherwise specified.

### 11.2 Dependencies

| Dependency | Type | Impact if Unavailable |
|---|---|---|
| Cloud hosting (Vercel + Railway) | External service | Application inaccessible; mitigated by local deployment option |
| PostgreSQL | Infrastructure | No data persistence; critical |
| Cloudflare R2 / AWS S3 | External service | File uploads fail; mitigated by local storage fallback |
| Clerk / NextAuth | External service | Authentication fails; mitigated by local auth fallback |
| WeasyPrint / react-pdf | Library | PDF generation fails; print-friendly HTML view as fallback |

### 11.3 Open Decisions (Pending Confirmation)

| ID | Decision | Status | Impact |
|---|---|---|---|
| **D-01** | UI Language (English / Bangla / Both) | Pending | Blocks mockup text finalization |
| **D-02** | Visual Direction (Dark / Light / Mixed) | Pending | Blocks CSS finalization |
| **D-03** | User Roles needed for Phase 1 | Pending | Blocks auth system design |
| **D-04** | Final Tech Stack | Pending | Blocks backend development |
| **D-05** | PDF Generation (native PDF vs print-friendly HTML) | Pending | Blocks document screen finalization |
| **D-06** | Existing data to import | Pending | Blocks data migration planning |
| **D-07** | Vendor screen needed | Pending | Blocks Screen 10 |
| **D-08** | Mobile / Tablet access required | Pending | Blocks responsive design scope |
| **D-09** | Product catalogue: fixed list or free text | Pending | Blocks order form design |
| **D-10** | Alerts & notifications scope | Pending | Blocks dashboard alert system |

---

## 12. Glossary

| Term | Definition |
|---|---|
| **Accessories** | Garment trims and accessories: labels, buttons, elastics, zippers, woven labels, etc. |
| **Bill of Exchange** | A written order binding one party to pay a fixed sum to another party on demand or at a future date |
| **Bulk Production** | Full-scale manufacturing of an order after sample approval |
| **Challan** | A delivery/dispatch document listing items shipped to a buyer |
| **Commercial Invoice** | A legal document between seller and buyer listing goods, quantities, and prices for customs |
| **GROSS** | A unit of 144 pieces |
| **LC (Letter of Credit)** | A bank guarantee instrument ensuring the seller receives payment upon meeting documentary conditions |
| **Maturity** | The date when payment under an LC becomes due |
| **Merchandiser** | A buyer's representative who manages procurement, reviews samples, and approves production |
| **Outsource** | Work sent to external vendors (e.g., in Mirpur or Gilistan) instead of produced in-house |
| **Packing List** | A document detailing the contents of each package in a shipment |
| **PI (Proforma Invoice)** | A preliminary invoice sent before shipment, detailing goods and prices |
| **Pipeline** | The sequential stages an order passes through from creation to completion |
| **Revision** | One iteration of sample creation + feedback. Multiple revisions are normal. |
| **Sample** | A prototype/example of the ordered product, made for buyer approval before bulk production |
| **Style** | The buyer's internal product code/name (e.g., SH-204, MBJA W26 DENIM-06) |
| **Transshipment** | Transfer of goods from one vessel/carrier to another during transport |

---

## 13. Appendices

### Appendix A — Recommended Tech Stack

| Layer | Technology | Justification |
|---|---|---|
| Frontend | Next.js (React) | HTML mockups port directly into components; SSR capability |
| Backend / API | FastAPI (Python) | Fast API development, clean business logic, great for reports |
| Database | PostgreSQL | Proper relational model for linked entities (orders → companies → LCs) |
| Auth | Clerk or NextAuth.js | Handles login, sessions, multi-role without custom auth code |
| File Storage | Cloudflare R2 or AWS S3 | Cheap object storage for PDFs, sample photos, uploaded documents |
| PDF Generation | WeasyPrint (Python) or react-pdf | Generates professional PDF documents from HTML templates |
| Frontend Hosting | Vercel | Optimized for Next.js, fast global CDN |
| Backend + DB Hosting | Railway or Render | Affordable, simple deploys, supports Python + PostgreSQL |

### Appendix B — Build Phases

| Phase | Scope | Status |
|---|---|---|
| **Phase 0** | Strategy, data model, screen inventory, open decisions | ✅ Complete |
| **Phase 1** | HTML/CSS mockups for all screens — iterate until approved | 🔄 In Progress |
| **Phase 2** | Next.js frontend — convert mockups to React components | Not started |
| **Phase 3** | FastAPI backend + PostgreSQL — wire up forms with real data | Not started |
| **Phase 4** | Auth + roles, PDF generation for PI / Challan / LC docs | Not started |
| **Phase 5** | Deploy on Railway + Vercel, go live with real data | Not started |

### Appendix C — Reference Documents & Artifacts

| Document | Location | Purpose |
|---|---|---|
| Real PI document | `05-images/Screenshot_104.png` | IKON letterhead, field layout, terms |
| Real order email | `05-images/Screenshot 2026-04-06 161444.png` | Style code format, buyer communication |
| Business lifecycle flowchart | `04-design-refs/01.png` | Process flow visualization |
| Data model skeleton | `04-design-refs/02.png` | Entity relationships |
| Dashboard concept | `04-design-refs/03.png` | UI concept for main screen |
| Order detail concept | `04-design-refs/04.png` | UI concept for order page |
| Timeline + locked bulk concept | `04-design-refs/05.png` | Staged unlock UX pattern |
| Companies screen concept | `04-design-refs/06.png` | Company + merchandiser layout |
| Master Plan | `01-strategy/01-master-plan.md` | Project scope and phasing |
| Screen Inventory | `01-strategy/02-screens.md` | All screens with field details |
| Open Decisions | `02-decisions/01-open-decisions.md` | Pending design decisions |
| Tech Stack | `06-docs/03-tech-stack.md` | Technology choices and rationale |
| V2 Mockups | `03-mockups/v2/*.html` | Working HTML prototypes (13 screens) |

---

*End of SRS Document*

*This document should be reviewed and updated as open decisions (D-01 through D-10) are resolved. All functional requirements marked "Should" or "Could" are candidates for descoping if timeline is constrained.*
