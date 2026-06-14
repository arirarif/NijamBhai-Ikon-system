# Operations & Maintenance Guide (run it for 10 years, no full-time developer)

**Audience:** the owner / 1–2 staff who run IKON day to day — **not** a programmer.
**Goal:** the system keeps working, your data is always safe, and you know exactly
what to do when something looks wrong.

You do **not** need to babysit this. It mostly runs itself. This guide is the
"in case of fire" manual. Read it once, then keep it handy.

---

## 1. The 30-second mental model

- The **website** (what you click) runs on **Vercel**. It auto-updates and needs no care.
- Your **data** (orders, companies, cash book…) lives in one **Postgres database** on **Railway**.
- **Your data is the only thing that's irreplaceable.** The code can always be
  rebuilt; the data cannot. That's why backups below matter most.

---

## 2. Backups — your safety net (mostly automatic)

You have **three independent copies** of your data ("multiple versions"), so a
failure of any one place never loses your data:

| # | Copy | Who makes it | How long kept | Effort |
|---|---|---|---|---|
| 1 | **Railway automatic backups** | Railway (managed) | per Railway plan | none — turn on once |
| 2 | **Nightly GitHub backup** | GitHub Action `Daily DB Backup` | 90 days | none — set one secret once |
| 3 | **Monthly archive you keep forever** | you (5 min/month) | forever | tiny |

### One-time setup (do this right after deploy)

1. **Railway backups** — Railway dashboard → your Postgres → **Backups** → enable
   automatic daily backups. Done.
2. **Nightly GitHub backup** — in GitHub: repo → **Settings → Secrets and variables
   → Actions → New repository secret**:
   - Name: `DATABASE_URL`
   - Value: the **public** Railway connection string.
   That's it. Every night at **11:30 PM (Dhaka time)** GitHub makes a fresh backup
   automatically. (File: `.github/workflows/backup.yml`.)

### Monthly habit (5 minutes, keeps a forever-copy)

Once a month, keep one backup permanently somewhere you control:
1. GitHub → **Actions** tab → **Daily DB Backup** → open the latest run →
   **Artifacts** → download the `ikon-backup-…dump` file.
2. Save it to **Google Drive / Dropbox / an external drive** in a folder like
   `IKON-Backups/2026/`. Keep at least the last 12 monthly files.

> Want this monthly copy to also be automatic into your own cloud? Ask the
> developer to enable the "OPTIONAL off-platform copy" block already prepared in
> `.github/workflows/backup.yml`.

### Make a backup right now, on demand

Before any risky change you can trigger one yourself: GitHub → **Actions** →
**Daily DB Backup** → **Run workflow**. (Or, with tools installed:
`DATABASE_URL="…" ./ikon-app/scripts/backup.sh`.)

---

## 3. Restoring (getting your data back)

If data is lost or corrupted, you restore from any backup file above.

**Easiest:** send the latest `.dump` file to your developer and say "please
restore this." It takes them a few minutes.

**If doing it yourself** (advanced), from the `ikon-app` folder:
```bash
DATABASE_URL="postgresql://…TARGET…" ./scripts/restore.sh path/to/ikon-backup-XXXX.dump
```
⚠ Always restore into a **fresh/empty** database first to check it looks right,
**before** pointing it at the live one. The script asks you to type `yes` to confirm.

> **Twice a year, do a restore drill:** restore the newest backup into a throwaay
> database and log in to confirm it works. A backup you've never tested is not a
> backup you can trust. Put it in the calendar (1 Jan, 1 Jul).

---

## 4. Is it healthy? (free monitoring)

The app has a health page: **`https://your-domain/api/health`**
- Healthy → `{"status":"ok","db":"up"}`
- Problem → `{"status":"error","db":"down"}` (and an error code)

**Set up free alerts (10 minutes, once):** create a free account at
**UptimeRobot.com** (or Better Uptime) → add a monitor for that `/api/health`
URL, checked every 5 minutes → enter your email/phone. If the site or database
ever goes down, **you get an email/SMS within minutes** instead of finding out
from a frustrated user.

---

## 5. What to do when something looks wrong

| Symptom | First thing to try |
|---|---|
| Site won't load at all | Check UptimeRobot / open `/api/health`. If `db:down`, see "DB issues". If whole site is down, check the Vercel dashboard → Deployments. |
| Login loops / "can't sign in" | Confirm `AUTH_URL` in Vercel matches your real domain exactly (no trailing slash) and `AUTH_TRUST_HOST=true`. |
| A PDF won't generate | Retry once (first one is slow). If it keeps failing, tell the developer — it's a server setting, not your data. |
| Got locked out after wrong passwords | The 5-attempts safety lock clears itself after **5 minutes**. Just wait and try again. |
| A page shows wrong/old numbers | Refresh. Data is live; there's no stale cache to clear. |
| **DB issues / data looks wrong** | **Do not panic and do not delete anything.** Take a manual backup (Section 2), then call the developer. Your nightly backups have you covered. |
| Accidentally archived a company/order | Use the **"Show archived"** toggle to restore it — archiving is reversible, nothing is truly deleted. |

**Golden rule:** if in doubt, **make a backup first** (Section 2), then change things.

---

## 6. Updates & long-term upkeep (light touch)

This stack was chosen to age well — it needs little. Realistic cadence:

- **Every push to `main` auto-deploys** to Vercel. If a deploy ever goes bad,
  Vercel → Deployments → pick the last good one → **Promote to Production** (instant rollback).
- **Monthly:** GitHub's Dependabot opens at most a few grouped "update" pull
  requests (`.github/dependabot.yml`). You can ignore these safely for a while;
  have the developer review/merge them a few times a year. **Security** alerts
  from GitHub should be handled sooner.
- **Yearly checklist (≈30 min with developer):**
  - [ ] Do a restore drill (Section 3).
  - [ ] Confirm the nightly backup ran (Actions tab shows green every day).
  - [ ] Renew the domain name (if you bought one) — don't let it lapse.
  - [ ] Apply the year's dependency/security updates and redeploy.
  - [ ] Confirm Vercel + Railway billing cards are valid (a failed payment can
        pause the service).

---

## 7. The "keys" — keep these safe (a password manager is ideal)

Losing these doesn't lose your data, but you'll need them to operate:

- Logins: **GitHub**, **Vercel**, **Railway** (+ domain registrar if any).
- The production **`AUTH_SECRET`** and **`DATABASE_URL`** (stored in Vercel env;
  also keep a copy in your password manager).
- The OWNER app login (`/login`).

Store them in **one place** (e.g. Bitwarden/1Password) that a trusted second
person can also reach, so the system isn't locked to a single individual.

---

## 8. Costs to keep it alive (≈ $20–30/month)

| Service | Typical | Note |
|---|---|---|
| Vercel | $0 (Hobby) → $20/mo Pro | Pro recommended for a real business |
| Railway Postgres | ~$5–15/mo | includes managed backups |
| Domain | ~$10–15/year | optional |
| UptimeRobot / GitHub / backups | $0 | free tiers are enough |

A lapsed payment is the most common "it stopped working" cause — keep cards current.

---

## 9. One-page emergency card

1. **Something's wrong?** Don't delete anything.
2. **Make a backup now:** GitHub → Actions → Daily DB Backup → Run workflow.
3. **Check health:** open `/api/health`.
4. **Site bad after a change?** Vercel → Deployments → Promote last good one.
5. **Still stuck?** Call the developer with: what you saw, the time, and the
   latest backup file. Your data is safe in three places.
