# Deploy — IKON

**Stack:** Vercel (web) + Railway (Postgres) per `06-docs/03-tech-stack.md`.

---

## Architecture in production

```
Browser → Vercel Edge (Next 15)
                ↓
          Vercel Node runtime (API routes, Puppeteer for PDFs)
                ↓
          Railway Postgres 16 (private network or pooled URL)
                ↓
          R2 (file storage — when attachments land, Sprint 12+)
```

Puppeteer note: PDF routes are marked `runtime = 'nodejs'`. Vercel Node functions have 1-vCPU / 1024 MB / 10s timeout on the free plan. PDF rendering fits comfortably under 5s for the templates we ship. Upgrade to Pro for `maxDuration: 30` if needed.

---

## Required env vars

Set in **Vercel Project Settings → Environment Variables** (apply to Production + Preview):

| Name | Required | Notes |
|---|---|---|
| `DATABASE_URL` | ✅ | Railway connection string. Use **pooled** URL for Vercel serverless. |
| `AUTH_SECRET` | ✅ | `openssl rand -base64 32` — never reuse the dev secret. |
| `AUTH_URL` | ✅ | `https://yourdomain.com` (no trailing slash). |
| `AUTH_TRUST_HOST` | ✅ | `true` — required by NextAuth on Vercel. |
| `NODE_ENV` | auto | Vercel sets this to `production`. |

Optional (later sprints):
| Name | When |
|---|---|
| `R2_ACCOUNT_ID`, `R2_ACCESS_KEY_ID`, `R2_SECRET_ACCESS_KEY`, `R2_BUCKET_NAME`, `R2_PUBLIC_URL` | When file attachments ship. |
| `RESEND_API_KEY` | When email alerts ship (D-10). |

---

## Vercel project setup

1. **Connect repo** → `vercel.com/new` → import `ikon-app/` as the project root.
2. **Framework preset:** Next.js (auto-detected).
3. **Build command:** `prisma migrate deploy && next build`
4. **Output directory:** `.next` (default).
5. **Install command:** `npm ci`
6. **Add env vars** (see table above).
7. **Domains:** add custom domain; Vercel issues SSL automatically.

The `prisma migrate deploy` step is critical — runs production migrations on every deploy. Never use `prisma db push` in production.

---

## Railway Postgres setup

1. `railway.app/new` → Provision PostgreSQL 16.
2. Copy the **public connection string** (TCP) for migrations from local CI.
3. Copy the **internal/pooled connection string** for `DATABASE_URL` in Vercel — lower latency, no PgBouncer hop on cold starts.
4. Run initial migration locally **once** against production:
   ```bash
   DATABASE_URL="<railway public url>" npx prisma migrate deploy
   ```
5. Seed the OWNER user (rotate the password!):
   ```bash
   SEED_OWNER_PASSWORD="<strong-secret>" \
   DATABASE_URL="<railway public url>" \
     npx tsx prisma/seed.ts
   ```
   *(seed.ts currently uses `ikon2026` hardcoded — update before running in prod, see F-04 in `07-security-audit.md`)*

---

## CI/CD via GitHub Actions

`.github/workflows/ci.yml` (suggested — not yet committed):

```yaml
name: CI
on:
  pull_request:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16-alpine
        env:
          POSTGRES_USER: arir_user
          POSTGRES_PASSWORD: arir_pass
          POSTGRES_DB: ikon_db_test
        ports: ['5432:5432']
        options: >-
          --health-cmd pg_isready --health-interval 10s --health-timeout 5s --health-retries 5
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: 20, cache: npm, cache-dependency-path: ikon-app/package-lock.json }
      - run: npm ci
        working-directory: ikon-app
      - run: npx prisma generate
        working-directory: ikon-app
        env: { DATABASE_URL: 'postgresql://arir_user:arir_pass@localhost:5432/ikon_db_test' }
      - run: npm run type-check
        working-directory: ikon-app
      - run: npm test
        working-directory: ikon-app
        env: { DATABASE_URL: 'postgresql://arir_user:arir_pass@localhost:5432/ikon_db_test' }
      - run: npm run build
        working-directory: ikon-app
        env: { DATABASE_URL: 'postgresql://arir_user:arir_pass@localhost:5432/ikon_db_test', AUTH_SECRET: 'ci-secret' }
```

Vercel auto-deploys on `main` push once GitHub is linked.

---

## Smoke test post-deploy

After first deploy, verify:

1. **HTTP** `GET https://yourdomain.com/login` → 200 (renders form)
2. **HTTP** `GET https://yourdomain.com/dashboard` → 302 → `/login` (middleware works)
3. Login with seeded OWNER credentials → lands on `/dashboard` with real data
4. Issue a test challan → click PDF link → PDF renders (Puppeteer warm-start may take 3–5s the first time)
5. Open `/reports` → 6-month bars + LC maturity list populate

If PDF fails with Chromium errors: Vercel's Node runtime ships Chromium dependencies but may need `@sparticuz/chromium` swap. Document this only if it happens — current `puppeteer` package bundles Chromium for development and should work on Vercel Node functions.

---

## Rollback

Vercel keeps every deployment. To roll back: **Project → Deployments → "Promote to Production"** on the previous green build. No DB rollback unless a migration changed schema — Prisma migrations are forward-only. For destructive migrations, take a Railway snapshot first.
