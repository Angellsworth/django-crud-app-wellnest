# 🌿 WellNest

*Your gentle space to begin again — as many times as you need.*

---

## About WellNest

**WellNest** is a personal wellness journal to help you reconnect with yourself — one habit, one mood, one reflection at a time.

It’s a quiet place to track what matters most: how you’re feeling, what you’re building, and who you’re becoming.

---

## Built With

- Django (Python)
- PostgreSQL
- JavaScript
- Django Templates, HTML, CSS
- Deployed on Heroku

---

## Features

- Secure user authentication
- Daily habit tracking (Create, Read, Update, Delete)
- Mood check-ins with emotional tracking
- Journal-style reflections
- Simple, forest-inspired design

---

## Getting Started

### Prerequisites

- Python 3.11  
- PostgreSQL  
- Git  

### Installation

```bash
git clone https://github.com/your-username/wellnest.git
cd wellnest

python3 -m venv env
source env/bin/activate

pip install -r requirements.txt

# Set up your .env file

python3 manage.py migrate
python3 manage.py runserver