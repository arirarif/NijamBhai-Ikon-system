# Tech Stack — Next Phase Build

## Recommended Stack

| Layer | Technology |
|---|---|
| Frontend | Next.js (React) |
| Backend / API | FastAPI (Python) |
| Database | PostgreSQL |
| Auth | Clerk or NextAuth.js |
| File Storage (PDFs, docs) | Cloudflare R2 or AWS S3 |
| Frontend Hosting | Vercel |
| Backend + DB Hosting | Railway or Render |

---

## Why These Choices

- **Next.js** — current HTML mockups port directly into components. SSR, fast, great ecosystem.
- **FastAPI** — fast to build business logic, great for reports and data processing. Python is readable long-term.
- **PostgreSQL** — relational data is the right fit. Orders → companies → LCs → payments, all linked. Not a NoSQL job.
- **Clerk / NextAuth** — handles login, sessions, multi-role (owner / staff / viewer). Never roll your own auth.
- **Cloudflare R2** — cheap object storage for PI PDFs, LC documents, delivery challans.
- **Railway** — affordable, simple deploys, handles Node/Python + Postgres together.

---

## Security Checklist (OWASP-aligned)

| Risk | Solution |
|---|---|
| SQL Injection | Use ORM (Prisma or SQLAlchemy) — never raw queries |
| Auth bypass | JWT with short expiry + refresh tokens |
| Role abuse | Server-side role checks on every route, not just UI |
| Data leaks | HTTPS enforced, env vars for all secrets, never hardcoded |
| CSRF | SameSite cookies + CSRF tokens on all forms |
| XSS | React escapes by default; sanitize any rich-text inputs |

---

## Build Phases

```
Phase 1 (done)    → HTML prototypes — mockups/v2/
Phase 2           → Next.js frontend, same UI converted to React components
Phase 3           → FastAPI backend + PostgreSQL, wire up forms with real data
Phase 4           → Auth + roles, PDF generation for PI / Challan
Phase 5           → Deploy on Railway + Vercel, go live with real data
```

---

## Key Libraries to Use

```
Frontend          next, react, tailwindcss (or keep custom CSS)
Backend           fastapi, sqlalchemy, alembic (migrations), pydantic
Database          postgresql + prisma (if full-stack JS) or psycopg2
Auth              clerk (easiest) or next-auth
PDF              weasyprint (Python) or react-pdf
Validation        zod (frontend) + pydantic (backend)
```
