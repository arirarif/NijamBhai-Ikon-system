# 08 — Engineering Workflow & Test Strategy

How the ERP expansion is actually built: team roles (even for a tiny team), a
**git-worktree** workflow for developing modules in parallel without stepping on the live
app, the **test strategy** that protects money/stock correctness, the CI quality gates, and
the per-phase **Definition of Done**.

---

## 8.1 Team & roles

The firm is small and the build is likely one developer (the owner-side author) possibly
assisted. Roles are *hats*, not headcount:

| Role | Responsibility |
|---|---|
| **Product owner** (Nezam bhai) | Confirms each module against business reality; signs off mockups; UAT |
| **Lead developer** | Schema design, posting services, code, migrations |
| **Reviewer** (peer or AI-assisted) | Reviews each module PR for correctness & the right-sizing charter |
| **QA / tester** | Runs the per-module test plan + UAT scripts before a module goes live |

Even solo, separating these hats matters: the *reviewer* and *QA* hats are where the
money/stock bugs get caught. Adversarial review (a second perspective, human or AI) on every
finance-touching PR is the single highest-value discipline.

---

## 8.2 Branch & git-worktree workflow

Because each ERP module is a clean folder boundary (§5.1), modules can be built in
**parallel git worktrees** — separate working directories sharing one repository — so an
in-progress module never destabilises `main` or another module.

```
ikon-app/                      # main worktree — always deployable
../ikon-erp-accounting/        # worktree on branch feat/erp-accounting   (E1)
../ikon-erp-inventory/         # worktree on branch feat/erp-inventory    (E2)
../ikon-erp-hr/                # worktree on branch feat/erp-hr           (E4)
```

Conventions:
- One **branch per phase**: `feat/erp-<module>` (e.g. `feat/erp-accounting`).
- One **worktree per active branch** (`git worktree add ../ikon-erp-accounting feat/erp-accounting`) — lets the dev run the live app and a feature build side by side, each with its own dev server/port and, if needed, its own test database.
- **Schema discipline:** because all modules share `prisma/schema.prisma`, merge migrations
  in **dependency order** (E0 → E1 → E2 …). Only one phase edits the schema at a time on
  `main`; parallel worktrees rebase onto the latest schema before their own migration. This
  prevents migration conflicts — the one real hazard of parallel work on a shared schema.
- Small, reviewable PRs; squash-merge to `main`; delete the worktree on merge
  (`git worktree remove`).

> The worktree approach is deliberately matched to this project's modular monolith: it gives
> the isolation benefits people reach to microservices for, at zero infrastructure cost.

---

## 8.3 Test strategy

The existing project already has Vitest (integration) + Playwright (e2e) and a CI pipeline.
The ERP modules extend that with **money/stock correctness as the priority**.

| Test layer | What it covers for ERP modules | Tooling |
|---|---|---|
| **Unit** | Pure calculations: P&L roll-ups, receivable aging, stock on-hand from movements, payroll net = gross − deduction, PO line totals, rounding | Vitest (pure functions in `lib/`) |
| **Integration** (real Postgres) | Posting services in transactions: stock-out posts the right ledger + cost + audit; goods-receipt raises stock + payable; payroll posts salary expense; **cross-module totals reconcile** | Vitest + test DB |
| **E2E** | Owner journeys: record expense → see it in P&L; stock-in → stock-out against order → cost on order; run payroll → slip PDF; log trip → transport expense | Playwright |
| **Migration tests** | `CashEntry → LedgerEntry` migration preserves existing cash totals | Integration, before/after assertions |

**Non-negotiable test rules for finance/stock code:**
1. Every posting service has an integration test asserting **all** of its effects (entity +
   ledger + audit), not just the primary write.
2. Reconciliation tests: derived stock on-hand == sum of movements; ledger P&L == sum of
   categorised entries.
3. Money math is tested for rounding at the boundary (Decimal, `.toFixed(2)` behaviour).

---

## 8.4 CI quality gates

Every PR must pass (extending the existing pipeline):

- `type-check` (tsc, zero errors)
- `lint` (ESLint, `--max-warnings 0`)
- `build` (no live DB needed)
- **`test`** — Vitest suite against a Postgres service (this is being added in the current
  hardening work; the ERP modules depend on it)
- Reviewer approval (the charter check: "is this the simplest thing that works at this
  scale?")

Migrations run as a **release step** (`railway.json` `preDeployCommand`), never on app
start — already configured.

---

## 8.5 Definition of Done (per module)

A module is DONE when **all** hold:

- [ ] Prisma migration written, applied, and reversible; schema conventions (§5.2) followed.
- [ ] API routes Zod-validated at the boundary; correct HTTP status codes.
- [ ] Server-side `requireRole` per the role matrix (§5.5).
- [ ] All cross-effects go through a `lib/posting` service **inside a transaction** and write
      `AuditLog`.
- [ ] UI matches the existing mockup; operable by a non-technical user (P8).
- [ ] Lists are **paginated**.
- [ ] Unit + integration tests for every calculation and posting; reconciliation tests green.
- [ ] CI green; reviewer + product-owner (UAT) sign-off.
- [ ] The §3.4 question the module owns is answerable from the UI.
- [ ] Docs: README/module note updated; any new decision recorded in doc 09.

---

## 8.6 Rollout & data

- **Ship behind the existing nav** — the four modules already have (disabled) nav slots;
  enable each as it reaches DoD.
- **Legacy data import** (open decision D-06): for each module decide *seed vs import* — e.g.
  opening stock balances and the employee list are worth a one-time CSV import; historical
  cash may start fresh from go-live. Keep imports as one-off scripts, not a permanent module.
- **UAT scripts** per module derived from §3.4 questions; the product owner runs them on real
  data before go-live.
