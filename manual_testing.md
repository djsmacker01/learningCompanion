# Manual testing — my checklist (Nurudeen)

I use this when **`pytest`** isn’t enough — e.g. coursework wants “manual” evidence, or I need to prove the live site matches my laptop.

I tick boxes on **localhost** first, then again on whatever **production URL** I’ve got after deploy. Same list both times so I’m not fooling myself.

---

## Before I even start clicking

- [ ] I copied **`.env.example`** → **`.env`** and filled it in (nothing secret goes to GitHub).
- [ ] I ran the SQL in **`supabase/migrations/`** on my Supabase project so I’m not testing against an empty shell.
- [ ] On the host (Railway / Render / whatever), **`FLASK_ENV=production`** and a real **`SECRET_KEY`** are set *before* I call it “done”.

---

## Does the app actually do CRUD?

- [ ] I registered, landed somewhere sensible (usually dashboard-ish).
- [ ] I logged out and back in — sessions didn’t feel broken.
- [ ] **Topics:** new topic → open it → edit title/description → delete/soft-delete if that’s how I built it → list looks right.
- [ ] **Sessions:** log or start one → edit → complete/delete if the UI offers it → history matches what I expect.
- [ ] **Quizzes** (if I turned them on): I can at least take or create one and the results page doesn’t explode.
- [ ] Flash messages after forms: I actually *read* them — success feels success-y, errors don’t look like silence.

---

## Navigation (the “no 404 embarrassment” pass)

- [ ] I clicked **everything** in the navbar, including dropdowns. No mystery 404s.
- [ ] Footer + legal pages (privacy, terms, etc.) — they load.
- [ ] “Back” / cancel on forms sends me where I’d expect, not into the void.

---

## Responsive enough that I’d use it on my phone

- [ ] Narrow browser (~390px): I can still use menus and forms without rage-quitting.
- [ ] Tablet-ish width: nothing looks like it gave up halfway.

---

## Accessibility — I’m not an auditor, but I do a honest pass

- [ ] Tab through a form: focus order isn’t random; I can reach buttons without a mouse.
- [ ] Quick peek at landmarks (`nav`, `main`) on at least one page — screen reader users deserve that structure.

---

## Production vs dev (the bit I skip when I’m tired — so I wrote it down)

- [ ] I repeated the same smoke tests on the **live link** as on localhost.
- [ ] Production doesn’t dump Python tracebacks to strangers (**DEBUG** off).
- [ ] I didn’t leave half-dead commented routes or “TODO: real URL” junk where a marker might look.

---

When I hand this in, I jot **date**, **browser**, and **local vs production** on a cover sheet or in my report so it’s obvious I didn’t only test on my machine.

— Nurudeen
