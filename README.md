# 📧 Gmail Cleaner

A clean, transparent, and rule-based Gmail inbox cleaner built with **Python (Django)**.

**Gmail Cleaner** helps you preview, organize, and clean your inbox using clear filter rules — without giving up control or privacy.

> ⚠️ This project is currently in **active development (MVP stage)**.

---

## ✨ Features (Planned & In Progress)

- 🔐 Secure **Google OAuth 2.0** authentication (no passwords stored)
- 👀 **Preview before action** — see what will be cleaned first
- 🧠 Rule-based email filtering (sender, subject, age, labels)
- 🏷️ Archive, label, or delete emails safely
- 🌐 Simple, aesthetic web UI
- 🆓 Free to use (within Google API limits)

---

## 🧱 Tech Stack

### Backend
- Python 3
- Django
- PostgreSQL (hosted on Neon)

### Frontend
- Django Templates
- Tailwind CSS (via CDN)

### Integrations
- Gmail API (Google OAuth 2.0)

---

## 🗂️ Project Structure

gmail-cleaner/
│
├── backend/
│ ├── config/ # Django project settings
│ ├── web/ # Main app (views, templates)
│ └── manage.py
│
├── .env
├── README.md
└── .gitignore


---

## 🚀 Getting Started (Local Development)

### 1️⃣ Prerequisites
- Python 3.10+
- Git
- A free **Neon PostgreSQL** database
- Google Cloud project (for Gmail API — later step)

---

### 2️⃣ Clone the repository
```bash
git clone https://github.com/<your-username>/gmail-cleaner.git
cd gmail-cleaner
3️⃣ Create and activate a virtual environment
python -m venv .venv
# Windows
.venv\Scripts\activate
4️⃣ Install dependencies
pip install -r requirements.txt
5️⃣ Environment variables
Create a .env file in the project root:

DATABASE_URL=postgresql://user:password@host/dbname?sslmode=require
DJANGO_SECRET_KEY=your-secret-key
DJANGO_DEBUG=1
⚠️ Never commit .env files. Use .env.example as a reference.

6️⃣ Run database migrations
cd backend
python manage.py migrate
7️⃣ Start the development server
python manage.py runserver
Open in browser:
👉 http://127.0.0.1:8000/

🔐 Security & Privacy
Gmail Cleaner never stores Gmail passwords

Access is granted only via Google OAuth

Only the minimum required Gmail scopes are used

Email content is not logged or persisted

Users stay in full control of all actions

🛣️ Roadmap
 Django scaffold + remote PostgreSQL

 Google OAuth login

 Gmail read-only preview

 Rule engine (DB-backed)

 Apply actions (archive / label / delete)

 Public deployment (MVP)

 OAuth verification (if going fully public)

