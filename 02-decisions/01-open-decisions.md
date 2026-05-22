# Open Decisions
**IKON Garments Accessories Software**  
These must be answered before or during mockup phase. Some block design. Some block code.

---

## D-01 — UI Language
**Blocks:** Mockup work  
**Question:** What language should the interface be in?

| Option | Pros | Cons |
|---|---|---|
| English only | Cleaner, easier to build, universal for business terms | Staff may not be comfortable |
| Bangla only | More comfortable for daily users | Business terms (LC, PI, Challan) are English anyway |
| English UI + Bangla labels toggle | Best of both worlds | More work to build |
| English with Bangla where needed | Practical middle ground | Inconsistent feeling |

**Recommendation:** English UI with English business terms (LC, PI, Style, etc.) — these are already how you use them in real documents. Staff acclimates quickly.

**Decision:** ✅ **English only** (2026-05-22)

---

## D-02 — UI Visual Direction
**Blocks:** Mockup work  
**Question:** What should the software look and feel like?

Reference screenshots from `04-design-refs/` use a **dark theme** with colored status badges.

| Option | Description | Best for |
|---|---|---|
| Dark professional | Dark bg, colored badges, dense info layout (like the suggested screenshots) | Power users, data-heavy screens |
| Light clean | White bg, minimal, card-based | Easier on eyes for long sessions |
| Mixed | Dark sidebar + light main content | Common in modern admin tools |

**Recommendation:** Mixed — dark sidebar nav + light main content area. Comfortable for long sessions, professional look.

**Decision:** ⬜ Pending

---

## D-03 — User Roles
**Blocks:** Backend design  
**Question:** Who logs in? What can each role do?

| Role | Possible access |
|---|---|
| Owner (you) | Full access — everything |
| Manager | All operations, no settings/financials |
| Staff / Factory | Only see orders assigned, sample tracker |
| View only | Read-only dashboard |

**Questions to answer:**
- Is it just you using this, or do staff members also log in?
- Do outsource vendors need any visibility?

**Decision:** ✅ **All 4 roles + Vendor portal** (2026-05-22)
- `OWNER` — full access (you)
- `MANAGER` — all operations, no settings/HR/financial admin
- `STAFF` — orders + sample revisions only, read-only on docs/LC
- `VIEWER` — read-only dashboard + orders list
- `Vendor portal` (later phase) — outsource vendors (Mirpur/Gulistan) get read-only view of orders assigned to them. Separate `Vendor` model + scoped queries.

Every API mutation server-side checks role per tech-stack senior rule #2.

---

## D-04 — Tech Stack
**Blocks:** Phase 3 (backend build)  
**Question:** What technology to build the backend with?

### Frontend
| Option | Notes |
|---|---|
| Plain HTML + CSS + vanilla JS | Simplest, no build step, easy to maintain |
| React / Next.js | More powerful, better for complex UI |
| Vue.js | Lighter alternative to React |

### Backend
| Option | Notes |
|---|---|
| Node.js (Express) | JavaScript throughout, good ecosystem |
| Python (FastAPI / Django) | Fast API, clean code |
| PHP (Laravel) | Widely deployed in Bangladesh, easy cheap hosting |

### Database
| Option | Notes |
|---|---|
| PostgreSQL | Most powerful, best for complex queries |
| MySQL / MariaDB | Very common, cheap hosting available |
| SQLite | Zero setup, good for single-user/small team |

### Hosting
| Option | Notes |
|---|---|
| Local PC / server | No internet needed, works offline |
| Shared hosting (BD providers) | Cheap, accessible from anywhere |
| VPS (DigitalOcean / Vultr) | More control, scalable |

**Decision:** ⬜ Pending — will decide after mockups are finalized

---

## D-05 — PDF Generation
**Blocks:** Document screens (Phase 4)  
**Question:** Should the software generate printable PDF versions of:
- Delivery Challan
- Proforma Invoice (PI)
- LC document pack

This is possible but adds complexity. Alternative: design print-friendly HTML views.

**Decision:** ⬜ Pending

---

## D-06 — Existing Data to Import
**Blocks:** Phase 3/4  
**Question:** Do you have existing records in Excel, notebooks, or anywhere else that need to be entered into the system when it launches?

If yes: we need an import plan or bulk entry strategy.

**Decision:** ⬜ Pending

---

## D-07 — Vendor / Outsource Screen
**Blocks:** Screen 10 mockup  
**Question:** Do outsource vendors (Mirpur, Gilistan) need their own management screen?

Minimum needed: a simple vendor directory (name, location, what they make, phone).  
Optional: track which orders went to which vendor, cost per job.

**Decision:** ⬜ Pending

---

## D-08 — Mobile / Tablet Access
**Blocks:** UI layout decisions  
**Question:** Does this software need to work on a phone or tablet?

- If yes: responsive design is required from the start (more work)
- If no: desktop-only is fine (faster to build, cleaner UI for data-heavy screens)

**Decision:** ⬜ Pending

---

## D-09 — Product / Item Catalogue
**Blocks:** New Order form  
**Question:** When logging a new order, is "product type" selected from a fixed list or always typed free-form?

From the PI screenshot, product types seen are:
- Satin Label
- Customer Care label
- Elastic
- Horn Button (CH)
- Woven Label

Are these fixed standard items? Or does it vary by buyer?

**Decision:** ✅ **Fixed 12-item dropdown + "Other" free text** (2026-05-22)

```
1.  Button           (covers Metal/Snap/Shank/Flat/Horn variants — put variant in styleName/styleCode)
2.  Zipper Pull
3.  Hang Tag
4.  Woven Label
5.  Printed Label
6.  Main Label
7.  Care Label
8.  Satin Label
9.  Elastic Band
10. Ribbon
11. Buckle
12. Thread
13. Other            (selecting reveals free-text input)
```

Lives as constant in `lib/constants/products.ts`. New Order form + filters read from this list.

---

## D-10 — Alerts & Notifications
**Blocks:** Dashboard design  
**Question:** Should the software alert you about:
- LC maturing within 14 days
- Overdue sample corrections (no reply after X days)
- Bulk production deadline approaching

If yes: these show as banners on the dashboard (already in the mockup concept).  
More advanced: browser notifications or email/SMS alerts.

**Decision:** ⬜ Pending
