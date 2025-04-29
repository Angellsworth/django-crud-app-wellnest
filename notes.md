PROJECT ROOT/
├── manage.py
├── Pipfile
├── Pipfile.lock
├── README.md
├── wellnest_project/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── main_app/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations/
│   │   └── __init__.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py             
│   ├── forms.py            
│   ├── static/              
│   │   ├── css/
│   │   ├── js/
│   │   └── images/
│   └── templates/           
│       ├── base.html
│       ├── home.html
│       ├── dashboard.html
│       ├── reflections/
│       └── habits/ROJECT ROOT/
├── manage.py
├── requirements.txt
├── wellnest_project/
│   ├── settings.py
│   ├── urls.py
│   └── ...
├── main_app/
│   ├── static/
│   │   ├── css/
│   │   ├── js/
│   │   └── images/
│   ├── templates/
│   │   ├── base.html
│   │   ├── home.html
│   │   ├── dashboard.html
│   │   ├── reflections/
│   │   └── habits/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── forms.py
└── README.md

Models:
- User (full Django auth, full CRUD: sign up, view profile, edit profile, delete account)
- Reflection (CRUD, linked to user)
- Habit (CRUD, linked to user)
- Mood (CRUD, linked to user)

Dashboard:
- Reflection journal entries
- Habit tracking
- Mood check-ins
- Profile overview

All data tied to authenticated user.