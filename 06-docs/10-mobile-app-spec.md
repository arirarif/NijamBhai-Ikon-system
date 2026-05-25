# IKON Mobile App — End-to-End Specification

**Hand-off document.** Paste this entire file into a new AI conversation and instruct: *"Build this mobile app according to the spec below. Ask only for clarifications that aren't in the doc."*

**Updated:** 2026-05-24
**Source-of-truth web app:** `arirarif/iKon-App` on GitHub (Next.js 15 + Prisma 7 + Postgres on Vercel + Railway)
**This mobile app reuses the same backend, same database, same business logic.**

---

## 1. Business context — what IKON is

IKON Garments Accessories is a Bangladesh-based supplier of garment accessories (buttons, zippers, labels, hang tags, elastic) to export-oriented apparel factories.

The software tracks a single business object — an **order** — through a fixed 10-stage pipeline that takes weeks to months per order:

```
1.  ORDER_RECEIVED       Buyer's merchandiser places an order
2.  SAMPLE_IN_PROGRESS   IKON makes a physical sample (in-house OR outsourced)
3.  SAMPLE_SENT          Sample dispatched to buyer for approval
4.  CORRECTION_NEEDED    Buyer rejects → loop back to step 2
5.  SAMPLE_APPROVED      Buyer accepts the sample
6.  BULK_PRODUCTION      Real production starts (cutting → sewing → finishing)
7.  CHALLAN_ISSUED       Delivery challan issued, goods dispatched
8.  PI_DONE              Proforma Invoice issued (export document)
9.  LC_OPEN              Buyer's bank opens a Letter of Credit (90-day term)
10. MATURED              LC matures, IKON gets paid (terminal state)
```

100+ orders are in flight at any time, each at a different stage. The owner needs to know where each one is, what's overdue, what needs feedback.

**Pain point the app solves:** today this is tracked in notebooks and Excel. Easy to lose track of the sample that needs feedback or the LC that matures in 14 days.

---

## 2. Mobile-specific value proposition

**Why a mobile app exists separately from the web app:**

| Use case | Why mobile beats web |
|---|---|
| Owner on the factory floor checking bulk production progress | Web requires sitting at a desk |
| Logging a buyer's correction feedback during a phone call | Tap "Mark Correction" with one thumb |
| Photographing a finished sample and attaching to the order | Camera access is native |
| Push notification: *"LC matures in 14 days"* | Web can't push |
| Sales rep visiting a buyer, demonstrating order status | Tablet/phone is portable |
| Reading the dashboard at 11pm before bed | Phones are by the bed |

**Owner's daily flow:**
1. Wake up → open app → see overnight overdue / urgent alerts on dashboard
2. Visit factory → tap any bulk order → adjust completion % from the floor
3. Buyer calls about R2 sample → mark "Correction Needed" with voice-to-text reason
4. Walk into office → all morning's mobile actions already synced to the web app his accountant uses

**Read-heavy on the go. Write actions are short and frequent (status changes, percentage updates, photo attachments, quick reason text).**

---

## 3. Recommended tech stack

| Layer | Choice | Why |
|---|---|---|
| Framework | **Expo (React Native) — SDK 53+** | Same TypeScript as the web app. Single codebase iOS + Android. Over-the-air updates without app-store re-submission. |
| Language | **TypeScript (strict)** | Identical to web. Share Zod schemas verbatim. |
| State | **TanStack Query (React Query) v5** | Server-state cache, automatic refetch, optimistic updates, offline-first behavior. |
| Auth | **expo-secure-store** + JWT bearer | Store the NextAuth JWT after login; send `Authorization: Bearer <token>` on every API call. |
| Forms | **react-hook-form + zod** | Share the existing Zod schemas from web. |
| Navigation | **Expo Router (file-based)** | Mirrors Next.js App Router structure → port screens almost 1:1. |
| Lists | **FlashList (Shopify)** | Performance for the 100+ order pipeline list. |
| Charts | **Victory Native** or **react-native-svg-charts** | Reports screen (revenue bars, stage breakdown). |
| Camera | **expo-camera** + **expo-image-picker** | Sample photo attachments. |
| Push | **expo-notifications** + **Expo Push Service** | LC maturity alerts, overdue order reminders. |
| PDF view | **expo-print** + WebBrowser | View challan / PI PDFs (fetch from existing `/api/.../pdf` endpoints). |
| Offline | **TanStack Query persistQueryClient** + **expo-sqlite** | Cache last seen state; queue mutations when offline. |
| Build | **Expo EAS Build** | Cloud-built `.ipa` and `.apk` without owning a Mac. |
| Updates | **Expo Updates** | OTA JS updates between native builds. |

**Reject these alternatives:**
- Flutter — splits the codebase from the TypeScript backend.
- Native iOS + Android — 2x dev time, no JS sharing.
- Capacitor / Cordova — webview wrappers feel sluggish for power users.
- Bare React Native (no Expo) — Expo's tooling is mature, EAS removes Mac dependency, no reason to drop down.

---

## 4. Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                  Mobile App (Expo / React Native)               │
│  ┌───────────────────────┐  ┌────────────────────────────────┐  │
│  │ UI (Expo Router)      │  │ Local State                    │  │
│  │ - Screens             │  │ - TanStack Query cache         │  │
│  │ - Native components   │  │ - SecureStore (auth token)     │  │
│  └───────────────────────┘  │ - SQLite (offline mutations)   │  │
│           │                 └────────────────────────────────┘  │
│           ▼                                                     │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ API client (axios or fetch wrapper)                         │ │
│  │ - Adds bearer token                                         │ │
│  │ - Retries on network error                                  │ │
│  │ - Queues writes when offline                                │ │
│  └────────────────────────────────────────────────────────────┘ │
└────────────────────────────────────────│────────────────────────┘
                                         ▼ HTTPS
┌─────────────────────────────────────────────────────────────────┐
│      Existing Next.js API on Vercel (NO CHANGES NEEDED)         │
│  /api/companies, /api/orders, /api/orders/[id]/stage, etc.      │
└────────────────────────────────────│────────────────────────────┘
                                     ▼
┌─────────────────────────────────────────────────────────────────┐
│              PostgreSQL (Railway) — shared with web             │
└─────────────────────────────────────────────────────────────────┘
```

**Key principle:** the mobile app is a **second client** to the existing backend. The same Prisma database. The same routes. The same role checks. **Do not** duplicate business logic on the device.

---

## 5. Authentication

The web app uses NextAuth credentials provider with JWT session cookies. For mobile we adapt to JWT bearer tokens (no cookies).

### One-time backend change needed
Add a new route `POST /api/auth/mobile-login` that:
- Accepts `{ email, password }`
- Validates against `User` model with `bcrypt.compare`
- Rate-limits via existing `lib/rate-limit.ts` (5 attempts per 5 min per email)
- Returns `{ token: string, user: { id, name, email, role } }` on success
- Token is a JWT signed with the same `AUTH_SECRET`, payload `{ sub: userId, role, exp }`
- 30-day expiry

Then add a JWT middleware so all existing `/api/*` routes accept either:
1. NextAuth session cookie (web)
2. `Authorization: Bearer <jwt>` header (mobile)

### Mobile login flow
1. App opens → checks `expo-secure-store` for stored token
2. Token absent or expired → show Login screen
3. User enters email + password → POST `/api/auth/mobile-login`
4. On success → store token in SecureStore → navigate to Dashboard
5. Every API call from `api-client.ts` reads the token from SecureStore and adds `Authorization: Bearer ...`
6. On 401 response → clear stored token, force re-login

---

## 6. Data model (mirror of `prisma/schema.prisma`)

The mobile app does **not** define a schema — it consumes the API. But its TypeScript types must match. Here are the 12 entities and their fields.

### `User`
```
id: string (cuid)
name: string
email: string (unique)
role: 'OWNER' | 'MANAGER' | 'STAFF' | 'VIEWER'
active: boolean
createdAt: Date
```

### `Company`
```
id, name, country, contactName?, phone?, email?, address?
active: boolean
createdAt: Date
merchandisers: Merchandiser[]
_count: { orders, merchandisers }
```

### `Merchandiser`
```
id, name, phone?, whatsapp?, email?, designation?, active
companyId: string
_count: { orders }
```

### `Order` ★ the central entity
```
id
orderNo: string (auto "ORD-YYYY-NNN")
styleName: string
styleCode?: string
productType: string                  // see list below
description?: string
quantity?: number
unit?: 'PCS' | 'DOZ' | 'GROSS' | 'YDS' | 'MTR' | 'SET'
stage: OrderStage                    // 10-value enum (see §1)
priority: 'NORMAL' | 'URGENT'
notes?: string
cancelledAt?: Date
cancelReason?: string
companyId, merchandiserId
revisions: SampleRevision[]
bulkProduction?: BulkProduction
challan?: Challan
pi?: PI
lc?: LCRecord
timeline: TimelineEntry[]
```

### `SampleRevision`
```
id, revisionNo (1, 2, 3…)
type: 'IN_HOUSE' | 'OUTSOURCED'
vendorName?, vendorLocation?
dateMade?, dateSent?
result: 'PENDING' | 'CORRECTION_NEEDED' | 'APPROVED'
merchandiserFeedback?
internalNotes?
orderId
```

### `BulkProduction` (one per order)
```
id, quantity, unit
startDate?, deadline?
completionPct: 0..100
status: 'ON_TRACK' | 'AT_RISK' | 'DELAYED' | 'COMPLETED'
notes?
orderId (unique)
```

### `Challan` (one per order)
```
id, challanNo (auto "DC-YYYY-NNN")
date, dispatchDate?
items: { description, quantity, unit, remarks? }[]
notes?
orderId (unique), companyId
```

### `PI` (one per order)
```
id, piNo (auto "PI-YYYY-NNN")
date
lineItems: { styleCode?, description, quantity, unit, unitPrice }[]
totalAmount: Decimal(12,2)
currency: string (default "USD")
terms?
bankDetails?: { bankName, bankBranch, bankSwift, bankAccount }
binVat?
finalized: boolean        // when true, edits blocked
orderId (unique), companyId
```

### `LCRecord` (one per order)
```
id, lcNo (unique string)
openDate, maturityDate (default open + 90 days)
bankName?, forwardDate?
status: 'OPEN' | 'FORWARDED' | 'MATURED'
notes?
hasCommercialInvoice, hasPackingList, hasDeliveryChallan, hasBillOfExchange: boolean
orderId (unique), piId?
```

### `TimelineEntry`
```
id, action, detail?
createdAt: Date
orderId, userId?       // who did it
```

### `Attachment`
```
id, fileName, fileUrl, fileSize, mimeType
orderId? OR sampleRevisionId?
createdAt
```

### `SystemSettings` (singleton, id="singleton")
```
companyName, address?, phone?, binVat?
bankName?, bankBranch?, bankSwift?, bankAccount?
piTerms?
```

### Product types (locked list, from `lib/constants/products.ts`)
```
Button, Zipper Pull, Hang Tag, Woven Label, Printed Label,
Main Label, Care Label, Satin Label, Elastic Band, Ribbon,
Buckle, Thread, Other (free text)
```

### Stage transition rules (from `lib/constants/stages.ts`)
```
ORDER_RECEIVED       → SAMPLE_IN_PROGRESS
SAMPLE_IN_PROGRESS   → SAMPLE_SENT
SAMPLE_SENT          → SAMPLE_APPROVED | CORRECTION_NEEDED
CORRECTION_NEEDED    → SAMPLE_IN_PROGRESS         (bounce-back loop)
SAMPLE_APPROVED      → BULK_PRODUCTION
BULK_PRODUCTION      → CHALLAN_ISSUED
CHALLAN_ISSUED       → PI_DONE
PI_DONE              → LC_OPEN
LC_OPEN              → MATURED
MATURED              → (terminal — no further transitions)
```

The mobile UI should show **only** legal next stages as action buttons. Never let the user pick an illegal jump.

### Role permissions
| Role | Can do |
|---|---|
| OWNER | Everything. Delete companies/merch. Cancel orders. Edit settings. |
| MANAGER | Create + edit orders, revisions, bulk, challan, PI, LC. Cannot delete or edit settings. |
| STAFF | Create + edit orders, revisions, bulk. Read-only on docs/LC. |
| VIEWER | Read-only everywhere. |

---

## 7. API contract (every endpoint the mobile app calls)

Base URL: `https://<your-vercel-domain>`. Always set:
- `Authorization: Bearer <jwt>` (except `/api/auth/mobile-login`)
- `Content-Type: application/json` on POST/PATCH

All write endpoints return `400` with `{ error, details: { fieldErrors: { field: [msg] } } }` on validation failure. The mobile app should map `fieldErrors` to per-field red highlighting (same pattern as web).

### Auth
| Method | Path | Body | Returns |
|---|---|---|---|
| POST | `/api/auth/mobile-login` | `{ email, password }` | `{ token, user }` or 401 |
| POST | `/api/auth/mobile-logout` | — | `{ ok: true }` (server-side token invalidation if you store a tokens table; otherwise client just deletes the token) |

### Companies
| Method | Path | Notes |
|---|---|---|
| GET | `/api/companies?q=&includeInactive=1` | List, search by name |
| POST | `/api/companies` | OWNER/MANAGER. Dup-check on name + email. |
| GET | `/api/companies/[id]` | Returns merchandisers + counts |
| PATCH | `/api/companies/[id]` | OWNER/MANAGER |
| DELETE | `/api/companies/[id]` | OWNER only. Soft-delete (active=false). |

### Merchandisers
| Method | Path | Notes |
|---|---|---|
| POST | `/api/companies/[id]/merchandisers` | OWNER/MANAGER. Dup-check on name/phone/email within company. |
| PATCH | `/api/merchandisers/[id]` | OWNER/MANAGER |
| DELETE | `/api/merchandisers/[id]` | OWNER only. Soft-delete. |

### Orders
| Method | Path | Notes |
|---|---|---|
| GET | `/api/orders?stage=&company=&q=&includeCancelled=&includeMatured=` | Filtered list. |
| POST | `/api/orders` | Auto orderNo. STAFF can create. |
| GET | `/api/orders/[id]` | Full file with revisions, bulk, challan, PI, LC, timeline (last 30). |
| PATCH | `/api/orders/[id]/stage` | Body `{ stage, note? }`. Enforces transition allow-list. |
| POST | `/api/orders/[id]/cancel` | Body `{ reason }`. Blocked if challan/PI/LC exist. |
| DELETE | `/api/orders/[id]/cancel` | Restore. |

### Sample revisions
| Method | Path | Notes |
|---|---|---|
| POST | `/api/orders/[id]/revisions` | Body type/dates. Auto revisionNo. Side-effect: advance order stage. |
| PATCH | `/api/revisions/[id]` | Body result/feedback. APPROVED→SAMPLE_APPROVED, CORRECTION→bounce. |

### Bulk production
| Method | Path | Notes |
|---|---|---|
| POST | `/api/orders/[id]/bulk` | Start. Body qty/unit/dates. Advances SAMPLE_APPROVED→BULK_PRODUCTION. |
| PATCH | `/api/orders/[id]/bulk` | Update progress. pct=100 → status=COMPLETED → stage CHALLAN_ISSUED. |

### Challan
| Method | Path | Notes |
|---|---|---|
| POST | `/api/orders/[id]/challan` | Auto DC-YYYY-NNN. Body line items. |
| GET | `/api/challans/[id]` | Detail |
| PATCH | `/api/challans/[id]` | OWNER/MANAGER |
| GET | `/api/challans/[id]/pdf` | Returns `application/pdf` byte stream. Mobile: download with `FileSystem.downloadAsync`, view with `WebBrowser.openBrowserAsync` or `expo-print`. |

### PI
| Method | Path | Notes |
|---|---|---|
| POST | `/api/orders/[id]/pi` | Auto PI-YYYY-NNN. Total computed from line items × unit price. Advances CHALLAN_ISSUED→PI_DONE. |
| GET / PATCH | `/api/pis/[id]` | Finalize-lock: when `finalized=true`, only `finalized=false` toggle is allowed (re-open). |
| GET | `/api/pis/[id]/pdf` | PDF byte stream. DRAFT stamp when not finalized. |

### LC
| Method | Path | Notes |
|---|---|---|
| POST | `/api/orders/[id]/lc` | Default maturity = open + 90 days. Advances PI_DONE→LC_OPEN. |
| GET / PATCH | `/api/lcs/[id]` | Status changes (OPEN→FORWARDED→MATURED). Doc checkboxes. MATURED → order MATURED stage. |

### Settings
| Method | Path | Notes |
|---|---|---|
| GET | `/api/settings` | Any role. |
| PATCH | `/api/settings` | OWNER only. |

---

## 8. Screen-by-screen UI spec

Use file-based Expo Router. Match these paths.

### `(auth)/login.tsx`
- Logo + "IKON Garments Accessories"
- Email + password fields (validation: email format, password ≥ 6 chars)
- "Sign in" button → POST `/api/auth/mobile-login` → store token → replace stack to Dashboard
- Forgot password link (placeholder for now)

### `(tabs)/dashboard.tsx`  ← entry tab
Layout (vertical scroll):
1. **Greeting** — *"Good morning, Nezam"* + today's date
2. **Alert strip** (red) — only if `overdueCount > 0`: *"3 orders overdue — tap to review"* → goes to `/orders?stage=sample&overdue=1`
3. **4 stat cards** in 2×2 grid:
   - Active Orders (blue)
   - Sample / Revisions (orange) — subtitle: *"3 need feedback"*
   - Bulk Production (red) — subtitle: *"2 delayed"*
   - Delivered This Month (green) — subtitle: *"↑ +4 vs last month"*
4. **Pipeline kanban** — horizontal scroll, 4 columns (Sample / Bulk / Docs / LC). Each column shows 3 latest orders + count. Tap order → detail screen.
5. **Recent activity** — last 10 timeline entries. Each row: dot + action + orderNo + meta + relative time.
6. **Upcoming LC maturity** — list of LCs maturing in 30 days, color-coded.
7. **Pull-to-refresh** → refetches all dashboard queries.

Data source: same as web's dashboard — many parallel queries via `useQueries`.

### `(tabs)/orders/index.tsx`
- Top: filter chips (All / Sample / Bulk / Docs / LC / Matured)
- Search bar (debounced, calls `/api/orders?q=`)
- FlashList of order cards:
  - Order no (mono font, accent color)
  - Style + product type
  - Company · merchandiser
  - Stage badge (color from STAGE_COLOR)
  - Priority indicator if URGENT
  - Relative updated time
- Floating action button bottom-right: **+ New Order**
- Pull-to-refresh

### `(tabs)/orders/new.tsx`
Step-free single form (mobile likes scroll, not wizards):
- **Company** — searchable picker → fetches `/api/companies`
- **Merchandiser** — picker scoped to selected company
- **Style name** *
- **Style code** (optional)
- **Product type** — picker from locked list, "Other" reveals free text
- **Quantity** + **unit** picker
- **Priority** (toggle: Normal / Urgent)
- **Description** (multiline)
- **Internal notes** (multiline)
- Sticky **Create Order** button at the bottom → POST `/api/orders`
- On success: navigate to order detail of newly created order

Per-field red highlighting on 400 response (map `details.fieldErrors`).

### `(tabs)/orders/[id].tsx`  ← the heart of the app
Vertical sections, each collapsible (default expanded for active sections):

1. **Hero**
   - Order no (big)
   - Stage badge (color-coded)
   - Urgent badge if URGENT
   - Created date
   - Company · merchandiser
   - **Action buttons row** — only allowed next stages from `NEXT_STAGES`:
     - e.g. at SAMPLE_SENT: [→ Approve] [→ Correction] [Cancel Order]
     - Tap → confirms with bottom sheet → calls PATCH `/api/orders/[id]/stage`
   - On cancel-eligible order: small "Cancel" red link
   - If cancelled: full-width red banner with reason + "Restore" button

2. **Stage progress strip** — horizontal scrollable dots bar showing all 10 stages, current highlighted, past green, future grey.

3. **Order info card** — style/code/qty/priority/description/notes in 2-col grid.

4. **Sample Revisions** section (visible if revisions exist or stage allows new revision)
   - List of revision cards (R1, R2, R3 …) with: type badge, dates, result badge, feedback/notes
   - On the latest PENDING revision: [Approve] [Correction] buttons
   - "+ New Revision" button at the bottom (only when stage allows)
   - Tapping a revision opens a modal/sheet with full detail + edit if pending

5. **Bulk Production** section (visible if stage ≥ SAMPLE_APPROVED)
   - If not started: **Start Bulk Production** form (qty/unit/deadline/notes)
   - If started: 4 stat tiles (qty/start/deadline/status) + completion bar + progress slider + status picker + "Mark Complete" button

6. **Documents** section (visible if stage ≥ BULK_PRODUCTION or any doc exists)
   - **Challan card** — if exists: number, date, "📄 View PDF" button. If absent and stage allows: "+ Issue Challan" button.
   - **PI card** — same pattern. Shows currency + total. Draft/Final badge. PDF button.
   - **LC card** — if absent: "+ Open LC" button. If present: separate full LC panel below.

7. **LC panel** (visible if LC exists) — full-screen-takeover-worthy:
   - LC no (mono), open date, maturity date, days-left count (red if ≤14)
   - Bank name + forward date
   - Status track buttons (Open / Forwarded / Matured) — tap to advance
   - 4 document checkboxes (Commercial Invoice / Packing List / Delivery Challan / Bill of Exchange) — tap to toggle, optimistic update
   - Notes

8. **Timeline** — vertical list of TimelineEntry rows (action + detail + relative time + who did it). Latest 30 entries.

9. **Contact** — merchandiser card with phone (tap to dial), email (tap to mail), company location.

### `(tabs)/samples.tsx`
List of latest revision per active order, filterable by status (active/pending/correction/approved/all). Each card has inline [Approve] [Correction] buttons. Tap card → goes to order detail.

### `(tabs)/companies.tsx`
- List of active companies (with toggle to show archived)
- Each card: initial avatar, name, contact info, stat strip (active/sample/bulk/docs/LC/total)
- Expanded merchandiser list per company
- 🗑 archive button on each (OWNER only, with confirm)
- Floating "+ Add Company" button → modal form with name/country/contact/phone/email/address

### `(tabs)/reports.tsx`
- 5 stat cards (Total / Active / Completed / Pending Samples / Need Correction)
- 6-month revenue bar chart per currency
- Stage breakdown horizontal bars
- Top companies ranked bars
- Active bulk production list with progress
- Upcoming LC maturity list with countdown

### `(tabs)/settings.tsx`
- Profile (name, email, role)
- Sign Out button
- OWNER only sections:
  - Company info form
  - Bank details form
  - PI Terms textarea
- Push notification preferences (toggles)
- About / version / build number

### `documents/challan.tsx`, `documents/pi.tsx`, `documents/lc.tsx`
List screens mirroring web — useful for browsing all docs in one place. Each row tappable → order detail.

---

## 9. Offline + sync strategy

Mobile users frequently lose signal on the factory floor. Critical for usability.

### Read side
- **TanStack Query** with `staleTime: 5 minutes` and `gcTime: 24 hours`.
- Persist query cache to AsyncStorage with `@tanstack/query-async-storage-persister`.
- Last successfully fetched data is shown when offline, with a banner *"Showing cached data — offline since 14:32"*.

### Write side
- All mutations go through a wrapper that:
  1. Optimistically updates the cache (so UI feels instant).
  2. Tries the API call.
  3. On success → commit cache update.
  4. On network failure → enqueue the mutation in SQLite with payload + path + method + idempotency key.
  5. When connectivity restored (via `NetInfo` listener) → replay queued mutations in order.
- Show a status pill in the header: *"3 pending uploads"* with tap → list of pending writes.

### Conflict resolution
Most IKON mutations are state advances (which only allow specific transitions). If a user marks R2 APPROVED offline and meanwhile someone else cancels the order, the queued mutation will fail server-side. Show the user a banner *"Some offline changes couldn't sync — review"* with the failed item + dismiss/retry.

### What to NOT cache for too long
- LC days-left countdowns (time-sensitive)
- Overdue calculations (depends on `now()`)
Recompute these on the client from cached `updatedAt` / `maturityDate`.

---

## 10. Push notifications

Use Expo Push.

### Registration
On first login on a device:
1. Request `Notifications.requestPermissionsAsync()`
2. Get the Expo push token: `Notifications.getExpoPushTokenAsync()`
3. POST it to a new backend route `/api/devices` storing `{ userId, token, platform, lastSeen }` in a new `Device` table.

### Server-side triggers (new backend cron job)
A Vercel Cron (or Railway scheduled task) running every hour computes and pushes:

| Trigger | Notification text |
|---|---|
| LC maturity ≤ 14 days | *"⚠ LC LC-2026-009 matures in 12 days. Prepare docs."* |
| Bulk production status = DELAYED | *"🏭 Order ORD-2026-031 is now DELAYED. Tap to review."* |
| Sample revision PENDING > 7 days | *"🔄 R2 on ORD-2026-038 has been waiting 8 days for buyer feedback."* |
| Order updatedAt > 5 days and stage in sample group | *"⏰ ORD-2026-041 has had no movement in 6 days."* |

### Local-only notifications (no server needed)
- LC maturity reminder set when LC opens (`scheduleNotificationAsync` 14 days before `maturityDate`)
- Sample feedback reminder (3 days after dateSent)

### Settings screen
Toggles per category. Persist in `User.notificationPrefs` JSON column (small backend addition).

---

## 11. Attachments (camera)

A frequently used flow: photograph a finished sample, attach to its revision.

### Flow
1. On `SampleRevision` detail sheet → "📷 Add Photo" button
2. `expo-image-picker` → camera or gallery
3. Image uploaded via new `POST /api/upload` endpoint that:
   - Accepts multipart/form-data
   - Stores to **Cloudflare R2** (env vars already in .env.example)
   - Returns `{ id, fileUrl, fileSize, mimeType }`
4. Mobile then calls `PATCH /api/revisions/[id]` with the attachment id linked

R2 SDK setup is small but **not currently implemented in the web backend** — flag this as a Phase-2 backend change.

---

## 12. State machine summary (port verbatim)

```
NEXT_STAGES = {
  ORDER_RECEIVED:     [SAMPLE_IN_PROGRESS],
  SAMPLE_IN_PROGRESS: [SAMPLE_SENT],
  SAMPLE_SENT:        [SAMPLE_APPROVED, CORRECTION_NEEDED],
  CORRECTION_NEEDED:  [SAMPLE_IN_PROGRESS],
  SAMPLE_APPROVED:    [BULK_PRODUCTION],
  BULK_PRODUCTION:    [CHALLAN_ISSUED],
  CHALLAN_ISSUED:     [PI_DONE],
  PI_DONE:            [LC_OPEN],
  LC_OPEN:            [MATURED],
  MATURED:            [],
}

STAGE_LABEL = { ORDER_RECEIVED: 'Order Received', SAMPLE_IN_PROGRESS: 'Sample Making', ... }
STAGE_COLOR = { ORDER_RECEIVED: '#8b9ab8', SAMPLE_IN_PROGRESS: '#fb923c', ... }
```

The web app's `lib/constants/stages.ts` is the source of truth. Port the file as-is.

---

## 13. Design system

**Match the web app's dark/light theme.** Web uses CSS variables; mobile use a `ThemeProvider` with the same colour names:

```
bg:      #0a0d14 (dark) | #fafbfc (light)
bg2:     #10141f | #ffffff
text:    #f0f4ff | #0f172a
text2:   #8b9ab8 | #475569
text3:   #4a5578 | #94a3b8
accent:  #4f8ef7
green:   #34d399
red:     #f87171
orange:  #fb923c
yellow:  #fbbf24
purple:  #c084fc
teal:    #2dd4bf
```

System font (San Francisco / Roboto). Sizes: 11/12/13/14/16/18/22/26. Border radius scale: 6/10/14.

The mobile app should default to **dark mode** (matches factory environments / dim lighting) with a system-preference toggle.

---

## 14. Build sprints (1 developer, 1 month total)

### Sprint 1 — Foundation (3 days)
- `npx create-expo-app ikon-mobile -t expo-template-blank-typescript`
- Add: Expo Router, react-query, axios, expo-secure-store, react-native-paper or NativeWind, zod
- Set up `app/_layout.tsx` with Stack + Tabs
- Build `api-client.ts` with bearer token injection from SecureStore
- Build `(auth)/login.tsx` screen + wire to `/api/auth/mobile-login` (which doesn't exist yet — see Sprint 2)
- Empty placeholder tabs

### Sprint 2 — Backend mobile-auth (1 day, on web repo)
- Add `POST /api/auth/mobile-login` to existing Next.js backend
- Add JWT verifier alongside existing NextAuth session check
- All existing routes accept either auth method
- Deploy via push (auto via Vercel)

### Sprint 3 — Dashboard + Orders list (4 days)
- Dashboard screen with parallel React Query hooks
- Orders list with FlashList + filter chips + search
- Stage badge component
- Order card component

### Sprint 4 — Order detail (5 days)
- Full order detail screen with all sections
- Stage transition action buttons
- Hero + stage strip + info card + timeline

### Sprint 5 — Sample revisions + bulk production (3 days)
- Revisions list + add modal + approve/correction sheets
- Bulk production panel (start form + progress controls)

### Sprint 6 — Documents (challan, PI, LC) + PDF viewer (3 days)
- Issue challan / PI / LC modals
- PDF viewing via `expo-print` or `WebBrowser.openBrowserAsync`
- LC details panel with status track + doc checklist

### Sprint 7 — Companies + Settings + Reports (3 days)
- Companies tab with archive toggle + add modal
- Settings tab with role-gated edits
- Reports tab with Victory Native charts

### Sprint 8 — Offline + Push notifications (4 days)
- TanStack Query persistence to AsyncStorage
- Mutation queue with SQLite
- Expo Push registration
- Backend cron for LC/overdue notifications

### Sprint 9 — Polish + QA (3 days)
- Empty states for every list
- Loading skeletons
- Form validation parity with web
- Per-field red highlighting
- Accessibility (screen reader labels)

### Sprint 10 — Build + distribute (2 days)
- `eas build -p ios` + `eas build -p android`
- TestFlight invite for owner
- Google Play internal track
- Set up `expo-updates` for OTA

---

## 15. Testing strategy

| Layer | Tool | Covers |
|---|---|---|
| Unit | Jest + react-native-testing-library | Pure functions (date math, stage transitions), reducer logic |
| Integration | MSW (Mock Service Worker) | Mock the API, render screens, assert UI states |
| E2E | Maestro or Detox | Login flow, full pipeline walk on iOS Simulator + Android Emulator |
| Manual | TestFlight + internal Play track | Owner uses on real device for a week before public release |

Aim for the same coverage as web: every mutation has at least one integration test. Re-use the same Zod schemas as web.

---

## 16. Deployment + distribution

| Platform | Channel | URL/Cost |
|---|---|---|
| iOS | TestFlight (private) → App Store | $99/yr Apple Developer |
| Android | Google Play internal track → public | $25 one-time Google Play |
| OTA JS updates | Expo Updates | Free on EAS |

**Tip for solo dev without Mac:** EAS Build runs in the cloud. You upload to App Store Connect from the EAS dashboard. No Mac needed for the actual builds.

---

## 17. Handoff checklist for the AI building this

Before writing code, the AI implementing this spec should:

- [ ] Confirm Expo SDK version with `npx create-expo-app` (must be 53+)
- [ ] Set up monorepo or separate repo decision (recommend: separate `ikon-mobile` repo)
- [ ] Confirm the user has Apple Developer + Google Play accounts (not required for dev, required for distribution)
- [ ] Confirm the backend URL the app will hit (Vercel production URL)
- [ ] Pull `lib/constants/stages.ts` and `lib/constants/products.ts` from web repo as the source of truth
- [ ] Pull `lib/validations/*.ts` (Zod schemas) and share verbatim — these are the API contracts
- [ ] Set up `app.json` with proper bundle ID (`com.ikon.garments` or similar) — required for both iOS and Android

When unclear about UI specifics, **match the web app's behavior**. The web app lives at `https://github.com/arirarif/iKon-App`.

---

## 18. What this mobile app intentionally does NOT do (yet)

- Vendor portal (vendors logging in to see their assigned orders) — future
- Bangla language toggle — D-01 was locked to English only
- Voice-to-text for reasons — nice-to-have, defer
- Barcode scanning of physical samples — defer
- Print-from-phone (Bluetooth thermal printer for challans on delivery) — defer
- Real-time multi-device sync via WebSockets — defer (React Query refetch on focus is enough at this scale)
- In-app messaging between OWNER/STAFF — defer (WhatsApp suffices for now)

---

## 19. End-state success criteria

The mobile app is "done" when the OWNER (Nezam) can do all of these from his phone, with no PC:

1. ✅ See pipeline status at a glance from his bed
2. ✅ Mark a sample APPROVED while walking the buyer through the office
3. ✅ Adjust bulk production % from the factory floor
4. ✅ Issue a challan on his phone and email the PDF to the buyer
5. ✅ Get a push notification 14 days before any LC matures
6. ✅ Add a new order during a buyer visit — within 60 seconds
7. ✅ Photograph a finished sample and attach it to its revision
8. ✅ See last month's revenue chart while explaining the business to his accountant

If those 8 work end-to-end, the mobile app has reached parity with what the owner needs.

---

**End of specification. Total effort estimate: ~30 working days for 1 senior React Native developer using Expo + this backend.**
