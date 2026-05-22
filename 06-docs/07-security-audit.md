# Security Audit — IKON

**Audit date:** 2026-05-22
**Scope:** `ikon-app/` (Next.js 15 + Prisma + NextAuth v5)
**Checklist:** OWASP-aligned per `06-docs/03-tech-stack.md`

---

## Summary

| Risk | Status | Notes |
|---|---|---|
| A01 Broken Access Control | ✅ Mitigated | Every API route uses `requireSession`/`requireRole`. Middleware redirects unauth to `/login`. |
| A02 Cryptographic Failures | ✅ OK | Passwords hashed with bcrypt(cost=12). NextAuth JWT signed with `AUTH_SECRET`. HTTPS enforced by Vercel in prod. |
| A03 Injection | ✅ OK | Prisma ORM only — no raw SQL. Zod validates all request bodies. |
| A04 Insecure Design | ✅ OK | Stage transitions guarded by `NEXT_STAGES` allow-list; mutations are transactional. |
| A05 Security Misconfiguration | ⚠ Action required | Production env vars need rotation; CSP not yet set. |
| A06 Vulnerable Components | ⚠ Action required | `npm audit` reports 5 moderate severity (run before deploy). |
| A07 Authentication Failures | ⚠ **Gap** | **No rate limit on `/login`** — see Findings. |
| A08 Data Integrity | ✅ OK | Server-side validation on every mutation. Foreign keys + uniqueness enforced at DB level. |
| A09 Logging & Monitoring | ⚠ Gap | No audit log of mutations or failed logins. |
| A10 SSRF | ✅ OK | No outbound URL fetches based on user input. |

---

## Detailed findings

### F-01 — No login rate limiting *(Medium → High in production)*

**Where:** `lib/auth.ts` Credentials provider `authorize()`.
**Impact:** Unlimited password attempts per email. Brute-force feasible on weak passwords.
**Fix options:**
1. **In-memory token bucket** (simplest, works for single-instance): map email→attempt count, reset every 5 min, lockout after 5 failures.
2. **Database-backed** (durable, scales): new `LoginAttempt` table; query last N minutes per email/IP.
3. **Upstash Redis or Vercel KV** (recommended for production): distributed counter, ~1ms latency.

Recommend option 3 once deployed. For now, ship option 1 as a baseline.

### F-02 — Audit log missing *(Low)*

**Where:** No table tracking who did what mutation when.
**Impact:** Cannot answer "who approved the sample on 2026-04-15?" or trace insider data tampering.
**Note:** `TimelineEntry` covers *what* happened per order but does not record the acting user.
**Fix:** Add `userId String?` to `TimelineEntry` and populate from `session.user.id`. Cheap, high value.

### F-03 — `npm audit` advisories *(Medium)*

Pre-deploy: run `npm audit` and fix moderate+ findings. Some are transitive deps of `puppeteer`/`@auth/core` that may need `npm audit fix --force`. Verify build still passes after.

### F-04 — Hardcoded seed password in seed.ts *(Low)*

`prisma/seed.ts` uses `ikon2026` as the OWNER password.
**Fix before prod:** Force password rotation on first login OR seed with a value from `process.env.SEED_OWNER_PASSWORD`.

### F-05 — PDF endpoints open to any session *(Low)*

`/api/challans/[id]/pdf` and `/api/pis/[id]/pdf` use `requireSession` (any role). For finer control, consider `requireRole(['OWNER','MANAGER'])` so STAFF/VIEWER can't download financial PDFs unless explicitly granted.

### F-06 — CSP / security headers not set *(Low)*

**Fix:** Add `next.config.ts` `headers()` block with Content-Security-Policy, X-Frame-Options, Referrer-Policy. Vercel can also enforce these globally.

---

## Verified-clean items

- All API mutations require role; reads require session.
- Middleware redirects every protected route to `/login` when unauthenticated.
- Cross-company merchandiser linkage prevented in `POST /api/orders` (rejects mismatched companyId).
- Stage transitions enforce `NEXT_STAGES` allow-list — can't jump straight to MATURED.
- PI finalize-lock prevents silent edits after issuance.
- LC + Challan + PI numbers auto-generated server-side (no client-supplied IDs).
- All currency math uses Prisma `Decimal(12,2)`, never `number`.
- React escapes user content in JSX; PDF templates use explicit `esc()` helper.
- Session cookies: HttpOnly, SameSite=Lax (NextAuth defaults), Secure in prod over HTTPS.

---

## Pre-deploy checklist

- [ ] `AUTH_SECRET` regenerated and stored in Vercel env (not committed)
- [ ] `DATABASE_URL` points to Railway managed Postgres
- [ ] OWNER password changed from `ikon2026`
- [ ] `npm audit` clean (or known-acceptable)
- [ ] F-01 rate limiting addressed (at minimum in-memory)
- [ ] F-02 audit log: add `userId` to `TimelineEntry`
- [ ] HTTPS enforced (Vercel default)
- [ ] CORS not opened (Next default same-origin OK)
- [ ] `prisma migrate deploy` step in CI before app start
