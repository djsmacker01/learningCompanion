# Deploying Learning Companion on Vercel (Nurudeen’s walkthrough)

This is the path I use when I want the app **live on the internet** without running my own server. Vercel gives you HTTPS, a URL like `https://something.vercel.app`, and deploys every time you push to GitHub if you wire that up.

Fair warning: this app is **Flask + Supabase**. Vercel runs it as **one serverless Python function**, so cold starts can feel a bit slow the first time someone hits the site. That’s normal on the free tier.

---

## Before you start

1. Code is on **GitHub** (Vercel imports from there).
2. **Supabase** project exists and you’ve run the SQL in `supabase/migrations/` (especially `users`, `topics`, etc.).
3. You have a **long random `SECRET_KEY`** ready (same idea as production anywhere — not your password, not a word from the dictionary).

---

## Step 1 — Push your repo

Make sure `main` (or whatever branch you deploy) has the latest code, including `api/index.py`, `vercel.json`, and `requirements.txt`.

---

## Step 2 — Create the Vercel project

1. Go to [vercel.com](https://vercel.com) and sign in (GitHub login is easiest).
2. **Add New… → Project**.
3. **Import** your `learningCompanion` repository.
4. Vercel will try to auto-detect settings. You want:
   - **Root directory:** leave default (repo root) unless you moved the app.
   - **Framework Preset:** can stay “Other” or whatever it picks; the important bit is the **Python** build pointing at `api/index.py` (already set in `vercel.json`).

If the dashboard offers an **Install Command**, it should match the repo:

```bash
pip install -r requirements.txt
```

(`vercel.json` already sets this — if the UI duplicates it, that’s fine.)

5. Click **Deploy** the first time *knowing* it might fail until env vars exist — that’s OK; we add those next.

---

## Step 3 — Environment variables (do not skip)

In the Vercel project: **Settings → Environment Variables**. Add these for **Production** (and Preview too if you want previews to work the same):

| Name | What to put |
|------|----------------|
| `FLASK_ENV` | `production` |
| `SECRET_KEY` | Long random string (required — the app refuses production without it) |
| `SUPABASE_URL` | From Supabase → Project Settings → API → Project URL |
| `SUPABASE_KEY` | **Service role** `secret` key (same one you use locally for server-side inserts — **never** the anon key for this app) |
| `OPENAI_API_KEY` | Optional — only if you want AI features in production |

Save, then **Redeploy** (Deployments → … on latest → Redeploy, or push an empty commit).

---

## Step 4 — After it’s green

1. Open `https://YOUR-PROJECT.vercel.app`.
2. Try **register → login → create a topic** (same smoke path as `manual_testing.md`).
3. If something breaks, open **Deployments → that deployment → Logs** and read the stack trace — almost always missing env var or Supabase RLS/key issue.

---

## Static files / CSS

Vercel’s Flask doc prefers static assets under **`public/`** for CDN. This project still serves CSS/JS through Flask’s `app/static` inside the function bundle, which usually works. If styles **don’t load** on Vercel only, check the function logs and then consider mirroring assets into `public/` per [Vercel’s Flask static guidance](https://vercel.com/docs/frameworks/backend/flask).

---

## Deploy from your machine (CLI)

If you like the terminal:

```bash
npm i -g vercel
cd /path/to/learningCompanion
vercel login
vercel link
vercel --prod
```

Set the same env vars in the dashboard once; CLI picks them up on deploy.

---

## Troubleshooting (the hits)

- **`SECRET_KEY` must be set…`** — you didn’t add `SECRET_KEY` in Vercel or spelled it wrong.
- **Supabase / auth errors** — wrong URL, wrong key type (use **service role** for this codebase), or migrations not applied.
- **`Client.__init__() got an unexpected keyword argument 'proxy'`** — old `pip` stack; use the repo’s `requirements.txt` (Supabase + httpx versions are pinned to play nice together) and redeploy.
- **504 / timeout** — heavy route; `vercel.json` sets `maxDuration` to 60s for `api/index.py`. You can raise it on paid plans if needed.

---

That’s the whole ritual. Once it’s up, paste the live URL into your report and run through **`manual_testing.md`** again on production so your evidence matches what the markers can click.

— Nurudeen
