# Deploy Runbook — Step by Step

**Goal:** ship `ikon-app/` to production on Vercel + Railway.
**Audience:** the person clicking the buttons (you).
**Prereqs:** GitHub account, Vercel account, Railway account, domain (optional).

Each step is one human action. Follow in order.

---

## Phase 1 — Push code to GitHub

### 1.1 Create the GitHub repo

Open https://github.com/new

- Repo name: `ikon-app` (or your choice)
- Visibility: **Private** (recommended — this is your business)
- Do NOT initialize with README/gitignore/license (we already have them)
- Click **Create repository**

GitHub shows you setup commands. Use the "**…push an existing repository**" section.

### 1.2 Push from your machine

```bash
cd C:\Users\arira\Desktop\NijamVhai\ikon-app

# Replace with the URL GitHub showed you
git remote add origin https://github.com/<you>/ikon-app.git
git branch -M main
git push -u origin main
```

> Note: this repo's default branch is `master`. `-M main` renames it to `main` which is Vercel/Railway-standard.

### 1.3 (Optional) Push the parent project repo too

Strategy docs + decisions + mockups live in the parent repo. Useful to keep with the code:

```bash
cd C:\Users\arira\Desktop\NijamVhai

# Create a separate repo on GitHub (e.g. nijamvhai-strategy)
git remote add origin https://github.com/<you>/nijamvhai-strategy.git
git push -u origin main
```

---

## Phase 2 — Provision Postgres on Railway

### 2.1 Sign in

Open https://railway.app/new → log in with GitHub.

### 2.2 Create the database

- Click **Provision PostgreSQL**
- Railway spins up a managed Postgres 16 instance — takes ~30s
- Open the **PostgreSQL** card

### 2.3 Get the connection strings

In the **Variables** tab:

| Copy this | Use it for |
|---|---|
| `DATABASE_URL` (the **public** one with the hostname like `monorail.proxy.rlwy.net`) | Local one-time migration |
| `DATABASE_PUBLIC_URL` or the private internal URL | Vercel `DATABASE_URL` |

Save both — you'll paste them in Phase 4.

### 2.4 Run migrations against production

From your local machine, **once**:

```bash
cd C:\Users\arira\Desktop\NijamVhai\ikon-app

# Paste the PUBLIC Railway URL here
$env:DATABASE_URL = "postgresql://postgres:xxxx@monorail.proxy.rlwy.net:12345/railway"
npx prisma migrate deploy
```

This applies every migration in `prisma/migrations/` to your production DB. **Forward-only** — you cannot undo. Take a Railway backup first if you're nervous (Railway → Settings → Backups).

### 2.5 Seed the OWNER user with a STRONG password

```bash
# Still inside ikon-app/
$env:DATABASE_URL = "postgresql://postgres:xxxx@monorail.proxy.rlwy.net:12345/railway"
$env:SEED_OWNER_EMAIL = "you@yourdomain.com"
$env:SEED_OWNER_NAME = "Your Full Name"
$env:SEED_OWNER_PASSWORD = "<a strong password — 16+ chars, mixed>"
$env:NODE_ENV = "production"

npx tsx prisma/seed.ts
```

> The seed script throws if `NODE_ENV=production` and `SEED_OWNER_PASSWORD` is missing (F-04 safeguard).

You can skip seeding the 4 demo companies / 25 demo orders by editing `prisma/seed.ts` first if you want a clean prod DB. Otherwise the demo data lands too.

---

## Phase 3 — Generate AUTH_SECRET

This signs NextAuth session JWTs. **Never reuse the dev one.** Generate fresh:

```bash
# Windows PowerShell
node -e "console.log(require('crypto').randomBytes(32).toString('base64'))"
```

One example output (DO NOT use this exact value — generate your own):
```
Q9KltltkV1cy+vzJJla2RJ1J5xZH5rpxjTBG80w2v0Y=
```

Save it — you'll paste it in Phase 4.

---

## Phase 4 — Deploy to Vercel

### 4.1 Import the project

Open https://vercel.com/new → log in with GitHub.

- Find your `ikon-app` repo → **Import**
- Framework Preset: **Next.js** (auto-detected)
- Root Directory: leave blank if the repo *is* ikon-app, or set to `ikon-app/` if you pushed the parent
- Build Command: **override** with `prisma migrate deploy && next build`
- Install Command: default (`npm install`)
- Output Directory: default

### 4.2 Add environment variables

Click **Environment Variables** → add these (apply to **Production + Preview + Development**):

| Name | Value |
|---|---|
| `DATABASE_URL` | Railway public/private URL from Phase 2.3 |
| `AUTH_SECRET` | The base64 string from Phase 3 |
| `AUTH_URL` | `https://your-vercel-subdomain.vercel.app` (no trailing slash — update after custom domain) |
| `AUTH_TRUST_HOST` | `true` |

### 4.3 Deploy

Click **Deploy**. First build takes ~3-5 min:

1. `npm install`
2. `prisma migrate deploy` (no-op now — already migrated in Phase 2.4)
3. `prisma generate`
4. `next build`

When green, Vercel shows your URL.

### 4.4 Custom domain (optional)

In Vercel → **Settings → Domains** → add your domain. Update DNS as instructed (ANAME/CNAME). SSL is automatic.

Once the domain works, **update `AUTH_URL`** to your custom domain and **redeploy** (Deployments → ⋯ → Redeploy).

---

## Phase 5 — Post-deploy smoke test

Visit your deployed URL. Verify each:

- [ ] `GET /login` renders the login form
- [ ] `GET /dashboard` (unauthenticated) → redirects to `/login`
- [ ] Login with your seeded OWNER credentials → lands on `/dashboard` with real numbers
- [ ] `/orders` lists orders
- [ ] Open any order detail → 10-stage dots bar visible
- [ ] Try issuing a test challan → PDF downloads (Puppeteer warm-start may take 5-10s first time)
- [ ] `/reports` shows the 6-month chart
- [ ] `/settings` is editable (you should be OWNER)

### If PDF fails

Vercel Node functions ship Chromium dependencies. If you see "Failed to launch the browser process":

1. Check Vercel function logs (Deployments → click the deployment → Functions → `/api/challans/[id]/pdf`)
2. Common fix: swap `puppeteer` for `puppeteer-core` + `@sparticuz/chromium` in `lib/pdf/render.ts`. Tell me and I'll patch it.

### If login redirects in a loop

Verify `AUTH_URL` exactly matches your domain (no trailing slash, correct protocol). Also confirm `AUTH_TRUST_HOST=true`.

---

## Phase 6 — Lock it down

### 6.1 Verify role enforcement

- Create a STAFF user in `/settings` (after wiring user management — that's a follow-up sprint; for now use Prisma Studio)
- Log in as that user → verify `/settings` shows read-only banner
- Verify `DELETE /api/companies/[id]` returns 403 from a STAFF session

### 6.2 Enable Vercel security headers (optional, F-06)

Add to `next.config.ts`:

```ts
async headers() {
  return [{
    source: '/(.*)',
    headers: [
      { key: 'X-Frame-Options', value: 'DENY' },
      { key: 'X-Content-Type-Options', value: 'nosniff' },
      { key: 'Referrer-Policy', value: 'strict-origin-when-cross-origin' },
      { key: 'Permissions-Policy', value: 'camera=(), microphone=(), geolocation=()' },
    ],
  }]
}
```

Redeploy. Verify with `curl -I https://yourdomain.com/`.

### 6.3 Set up auto-deploys

Already enabled by default — every push to `main` redeploys automatically. Optional: branch previews for `develop` (Vercel Settings → Git → Production Branch).

---

## Rollback

Something broken in production?

1. Vercel → **Deployments** → find the last good build → ⋯ → **Promote to Production**
2. Done. No DB rollback unless a migration changed schema — Prisma migrations are forward-only. For destructive migrations: restore Railway from the snapshot you took in Phase 2.4.

---

## Cost expectations (May 2026 pricing)

| Service | Free tier | When you'll outgrow it |
|---|---|---|
| Vercel Hobby | Personal projects, 100 GB bandwidth | When you go commercial — upgrade to Pro ($20/mo) |
| Railway | $5 starter credit/mo, then pay-as-you-go | ~$5-15/mo for a small Postgres instance |
| Domain | n/a | ~$10-15/yr (Namecheap, Porkbun) |

Total monthly when live: **~$20-30/mo** to start. Scales linearly with usage.

---

## What I (Claude) cannot do for you

- Sign in to GitHub / Vercel / Railway with your credentials
- Pay for plans
- Pick a domain name
- Decide what's a "strong" OWNER password
- Run `git push` to a remote that doesn't exist yet

Everything else (code fixes if deploy fails, migrations, fresh seeds, performance tuning) — ask and I'll do it.
