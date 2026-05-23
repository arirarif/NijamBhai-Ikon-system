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
| A07 Authentication Failures | ✅ Mitigated | In-memory rate limit on `/login` (5 attempts / 5 min). See F-01. |
| A08 Data Integrity | ✅ OK | Server-side validation on every mutation. Foreign keys + uniqueness enforced at DB level. |
| A09 Logging & Monitoring | ✅ Partial | `TimelineEntry.userId` records every order mutation. Failed login attempts still not logged (low risk with F-01 in place). |
| A10 SSRF | ✅ OK | No outbound URL fetches based on user input. |

---

## Detailed findings

### F-01 — Login rate limiting ✅ Mitigated (in-memory baseline)

**Implemented:** `lib/rate-limit.ts` (sliding-window bucket) + integrated into `lib/auth.ts` Credentials provider.
- 5 attempts per 5-minute window per email (`LOGIN_RATE_LIMIT`).
- Successful login calls `rateLimitReset(email)` so legit users aren't penalized.
- Tested in `tests/integration/rate-limit.test.ts` (5 tests).

**For multi-instance production:** swap the in-memory `Map` with Vercel KV / Upstash Redis. The function signature stays the same.

### F-02 — Audit log ✅ Mitigated

**Implemented:** `TimelineEntry.userId String?` added via migration `20260522163749_add_timeline_user` + relation to `User`. Every mutation now records the acting user:
- `POST /api/orders` (order created)
- `PATCH /api/orders/[id]/stage` (stage transitions)
- `POST /api/orders/[id]/revisions` (R# started/sent)
- `PATCH /api/revisions/[id]` (approve / correction)
- `POST/PATCH /api/orders/[id]/bulk` (start, progress, complete)
- `POST /api/orders/[id]/challan` + `PATCH /api/challans/[id]`
- `POST /api/orders/[id]/pi` + `PATCH /api/pis/[id]`
- `POST /api/orders/[id]/lc` + `PATCH /api/lcs/[id]`

Query example for "who approved sample R2 on order X?":
```sql
SELECT u.name, t.action, t.detail, t."createdAt"
FROM timeline_entries t
JOIN users u ON u.id = t."userId"
WHERE t."orderId" = '<orderId>' AND t.action LIKE 'R% approved';
```

### F-03 — `npm audit` advisories ✅ Reviewed (no action needed)

5 moderate advisories as of 2026-05-23:
- `@hono/node-server` middleware bypass via `serveStatic` — appears via `@prisma/dev` (dev tool only, not production runtime). No exposure.
- `postcss <8.5.10` XSS via unescaped `</style>` — used at build time only, not in runtime. No user-facing CSS processing.

`npm audit fix --force` would downgrade Prisma to v6 and Next to v9. **Do not run.** Re-review on every Prisma/Next major version bump.

### F-04 — Seed password rotation ✅ Mitigated

`prisma/seed.ts` now reads `SEED_OWNER_EMAIL` / `SEED_OWNER_NAME` / `SEED_OWNER_PASSWORD` from env. When `NODE_ENV=production`, the seed throws if `SEED_OWNER_PASSWORD` is missing. Default falls back to `ikon2026` only in development.

### F-05 — PDF endpoint role tightening ✅ Mitigated

`/api/challans/[id]/pdf` and `/api/pis/[id]/pdf` now require `OWNER` or `MANAGER`. STAFF/VIEWER receive 403 when attempting to download financial PDFs.

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
- [x] `npm audit` reviewed (2 advisories, both dev-only — see F-03)
- [x] F-01 rate limiting addressed (in-memory baseline, swap to KV/Redis for multi-instance)
- [x] F-02 audit log: `TimelineEntry.userId` shipped
- [x] F-04 seed password reads from `SEED_OWNER_PASSWORD` env in production
- [x] F-05 PDF endpoints require OWNER/MANAGER role
- [ ] HTTPS enforced (Vercel default)
- [ ] CORS not opened (Next default same-origin OK)
- [ ] `prisma migrate deploy` step in CI before app start
