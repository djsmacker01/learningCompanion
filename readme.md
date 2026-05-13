# Learning Companion

 I built **Learning Companion** because I got tired of studying feeling scattered: notes everywhere, no honest picture of what I’d actually done that week, and “progress” tools that felt like homework for my homework.

So this is a Flask app where you can **organise topics**, **log study sessions**, poke at **GCSE-focused bits** (subjects, past papers, scheduling — the stuff that mattered to me), plus **quizzes** and **reminders**. If you hook up an OpenAI key, there’s an **AI tutor** layer too. I’m not pretending it solves life — it’s just a calmer place to put your learning and see it add up.

---

## Why I made it

I wanted one place where I could **create, read, update, and delete** real records (topics, sessions, etc.) without losing the plot. The database side lives on **Supabase** (Postgres), and the UI is plain HTML templates with Bootstrap and my own CSS — nothing fancy, but it had to work on a phone as well as a laptop.

If you’re marking this for uni: the “value” bit is simple — **less friction between “I should study” and “I actually logged what I did.”**

---

## What you need on your machine

- **Python 3.11+** — I run tests on 3.11 in CI; 3.12 has been fine for me locally.
- A **Supabase** project (free tier is enough to start).
- **Optional:** an **OpenAI** API key if you want the AI features to do more than politely fail.

---

## How I run it locally

```bash
python -m venv venv
source venv/bin/activate          # Windows Git Bash: source venv/Scripts/activate
pip install -r requirements.txt
cp .env.example .env
```

Then I open `.env` and fill in the blanks. For local dev I still set a **`SECRET_KEY`** — I just use a long random string I make up; it doesn’t need to be pretty, it just can’t be empty if you flip to production mode later.

The database schema is in **`supabase/migrations/`**. I run those scripts in the Supabase SQL editor when I spin up a fresh project (honestly, that’s the least glamorous part — copy, paste, run, swear once if I typo a semicolon).

```bash
python run.py
```

Then I hit **`http://127.0.0.1:5000`** in the browser. If the app complains about env vars, it’s almost always me forgetting to save `.env` or putting the wrong key name.

---

## Tests (what I actually run)

I use **pytest** because I like seeing green in the terminal:

```bash
pytest -q
```

For assignments that want “manual testing” evidence, I wrote **`manual_testing.md`** for myself — it’s literally a checklist: click the nav, try CRUD, resize the window, do the same on the live site after deploy. I tick boxes like a normal person so I don’t forget anything obvious.

---

## Deploying (I’m not married to one host)

I’ve got notes in two places because different weeks meant different platforms:

- **`deployment_guide.md`** — Railway, Render, Heroku-style flow, DigitalOcean — the “pick your fighter” doc.
- **`deployment.md`** — when I was chasing **Vercel** specifically.

Whatever you use: set **`FLASK_ENV=production`**, generate a proper **`SECRET_KEY`** in the host’s dashboard (not in Git), and paste **Supabase** URL + key there too. My **`.gitignore`** already ignores `.env` — please don’t commit secrets; I’ve made that mistake in my head enough times without doing it for real.

After it’s live, I open the public URL and run through **`manual_testing.md`** again. The deployed app should feel like the one on my laptop — if it doesn’t, I go read the logs instead of assuming magic.

---

## Env vars I keep straight

| Variable | In my own words |
|----------|------------------|
| `FLASK_ENV` | **`development`** on my laptop; **`production`** when it’s on the internet |
| `SECRET_KEY` | Flask uses this for sessions — **non-negotiable in production** |
| `SUPABASE_URL` | Where my Supabase project lives |
| `SUPABASE_KEY` | The key the app uses to talk to the DB — treat it like a password |
| `OPENAI_API_KEY` | Optional — without it, some AI bits just won’t fire |

If you’re stuck on `SECRET_KEY`, I literally open a password generator or bash out random characters until my fingers hurt. Then I paste it **once** into Railway/Render/Vercel and never put it in the repo.

---

## Where stuff lives in the repo

- **`app/`** — routes, templates, static files (the actual app)
- **`supabase/migrations/`** — tables, relationships, the boring important stuff
- **`tests/`** — what `pytest` runs
- **`deployment_guide.md`** / **`deployment.md`** — me explaining deployment to future-me

---

## Git

I try to write commit messages I’d understand three weeks later — *“Fix session history when topic is shared”* beats *“fix”*. Future Nurudeen says thanks.

---

That’s the honest version. If something in here doesn’t match what you see on your machine, it’s probably me assuming your Supabase project is already migrated — ping me or your tutor and we’ll untangle it.

— Nurudeen
