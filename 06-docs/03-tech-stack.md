# Tech Stack — IKON Fullstack (Final Decision)

**Decision date:** May 2026  
**Horizon:** 10-year production system  
**Rule:** One language (TypeScript) throughout. No split-brain.

---

## Stack

| Layer | Technology | Version |
|---|---|---|
| Framework | Next.js (App Router) | 15+ |
| Language | TypeScript (strict mode) | 5+ |
| Database | PostgreSQL | 16+ |
| ORM | Prisma | 5+ |
| Styling | Tailwind CSS | 3+ |
| Auth | NextAuth v5 (Auth.js) | 5+ |
| Validation | Zod | 3+ |
| PDF Generation | Puppeteer (via API route) | latest |
| File Storage | Cloudflare R2 | — |
| Alerts | Resend (email) | — |
| Frontend Hosting | Vercel | — |
| Database Hosting | Railway | — |
| CI/CD | GitHub Actions | — |

---

## Why Each Choice

- **Next.js App Router** — Full-stack TS. API routes replace separate backend. SSR + Server Components = fast by default. Mockups port directly to React components.
- **TypeScript strict** — Type safety = self-documenting. Catches bugs at build time. Essential for 10-year codebase.
- **PostgreSQL** — Relational data: orders → companies → LCs → revisions. All linked. Rock solid since 1996.
- **Prisma** — Schema = single source of truth. Types auto-generated. Migrations version-controlled. No raw SQL.
- **Tailwind** — No custom CSS to maintain. Consistent with existing mockup aesthetic.
- **NextAuth v5** — Self-hosted auth. No SaaS dependency. Credentials + session. Free forever.
- **Zod** — One schema validates both frontend form and API route input. No duplication.
- **Puppeteer** — Renders existing IKON HTML designs pixel-perfect to PDF. No redesign.
- **Cloudflare R2** — Cheapest S3-compatible storage. PDFs, LC docs, sample images.
- **Vercel + Railway** — Vercel = perfect for Next.js. Railway = managed PostgreSQL. Simple, affordable.

### Why NOT FastAPI (Python)

Two languages = two dependency trees, two mental models, two deploy pipelines.
One developer or small team over 10 years cannot sustain that well.
TypeScript API routes inside Next.js handle all data needs for this scale.

---

## Architecture

```
ikon-app/                         ← single monorepo
├── app/
│   ├── (auth)/                   ← login (no sidebar layout)
│   ├── (dashboard)/              ← all protected pages
│   │   ├── dashboard/
│   │   ├── orders/
│   │   ├── companies/
│   │   ├── documents/
│   │   │   ├── pi/
│   │   │   ├── challan/
│   │   │   └── lc/
│   │   └── settings/
│   └── api/                      ← REST API routes (backend)
│       ├── orders/
│       ├── companies/
│       ├── documents/
│       └── pdf/
├── components/
│   ├── ui/                       ← Button, Badge, Input, Modal, Table
│   ├── layout/                   ← Sidebar, Topbar, PageHeader
│   └── features/                 ← OrderCard, RevisionList, PipelineBar
├── lib/
│   ├── db.ts                     ← Prisma client singleton
│   ├── auth.ts                   ← NextAuth config
│   ├── validations/              ← Zod schemas
│   └── pdf/                      ← Puppeteer helpers
├── prisma/
│   ├── schema.prisma             ← data model (single source of truth)
│   └── migrations/               ← version-controlled schema history
├── types/                        ← shared TypeScript interfaces
├── hooks/                        ← custom React hooks
└── tests/
    ├── unit/                     ← pure functions (Vitest)
    ├── integration/              ← API routes + real DB (Vitest)
    └── e2e/                      ← critical user flows (Playwright)
```

---

## SDLC Build Phases

```
Phase 0 (done)   → Requirements + SRS
Phase 1 (done)   → HTML mockups — 03-mockups/v2/
Phase 2          → Foundation: repo setup, Prisma schema, auth, sidebar layout, CI/CD
Phase 3          → Core screens: Dashboard, Companies, Orders, Sample revisions
Phase 4          → Documents: Challan, PI, LC Tracker — with PDF export
Phase 5          → Alerts, Reports, Settings
Phase 6          → E2E tests, security audit, staging sign-off
Phase 7          → Production deploy + staff training
Phase 8+         → Day-by-day feature updates
```

### Screen Build Order

| Sprint | Screen | Reason |
|---|---|---|
| 1 | Login + Dashboard (read-only) | Daily entry point |
| 2 | Companies + Merchandisers CRUD | Entry point for all data |
| 3 | New Order form | Core input |
| 4 | Order Detail + stage transitions | Core tracker |
| 5 | Sample Revision add/edit | Most complex flow |
| 6 | Bulk Production tracker | Unlocks after approval |
| 7 | Delivery Challan + PDF | Document output |
| 8 | Proforma Invoice + PDF | Document output |
| 9 | LC Tracker + maturity alerts | Finance critical |
| 10 | Reports + analytics | Visibility |
| 11 | Settings (company info, bank, terms) | Config |

---

## Security (OWASP-aligned, built in)

| Risk | Solution |
|---|---|
| Auth bypass | NextAuth session check on every API route |
| Role abuse | Server-side role check on every mutation |
| SQL injection | Prisma ORM — no raw SQL ever |
| Bad input | Zod validates every API request body |
| Data leaks | HTTPS only (Vercel enforces), all secrets in env vars |
| XSS | React escapes by default; sanitize any rich text |
| CSRF | NextAuth SameSite cookies |
| Brute force | Rate limit on login route |

---

## Testing Strategy

| Type | Tool | Covers |
|---|---|---|
| Unit | Vitest | Date calc, LC maturity, stage logic, pure fns |
| Integration | Vitest + test DB | API routes with real PostgreSQL queries |
| E2E | Playwright | Login → order → approve → PDF generation |

Rule: every API route ships with at least one integration test.

---

## CI/CD Pipeline

```
feature/* → PR → GitHub Actions:
  - tsc --noEmit (type check)
  - ESLint
  - Vitest (unit + integration)
  - Next.js build check
→ merge to develop → auto-deploy to Staging (Vercel preview)
→ merge to main    → auto-deploy to Production (Vercel)
```

Merge to main only if all checks pass. No exceptions.

---

## Senior Engineer Rules

1. Server Components default — `"use client"` only for real browser interactivity
2. Validate at boundary — Zod on every API input, dies at the door
3. Prisma schema = contract — types generated from it, never duplicated manually
4. One Prisma client — singleton from `lib/db.ts`, never `new PrismaClient()` in components
5. Select only needed fields — no `findMany()` dumping full objects to client
6. Feature folders — page + server actions + components grouped together
7. PostgreSQL in dev too — no SQLite, no "works on my machine"
8. Migration discipline — `prisma migrate dev` in dev, `prisma migrate deploy` in prod
9. Proper HTTP status codes — 200/201/400/401/403/404/500, no silent failures
10. No premature optimization — add Redis/queue/cache only when real problem appears

---

## What NOT to Build

- No microservices — one Next.js app handles everything
- No GraphQL — REST API routes fine for this scale
- No Redis — PostgreSQL handles query load easily at this scale
- No Docker in production — Vercel + Railway handles infra
- No message queues — not needed
- No separate admin panel — settings built into the app
