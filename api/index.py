"""
Vercel serverless entry for Learning Companion.

Vercel runs this as a single Python function; it must expose a WSGI `app`
(see https://vercel.com/docs/frameworks/backend/flask).
"""
import os

from dotenv import load_dotenv

load_dotenv()

from app import create_app

# Match config.py keys: only "development" and "production" are valid.
_env = (os.getenv("FLASK_ENV") or "production").strip().lower()
if _env not in ("development", "production"):
    _env = "production"

app = create_app(_env)

if __name__ == "__main__":
    app.run()
