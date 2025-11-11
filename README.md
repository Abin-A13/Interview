# Task Queue & Notification API

## Requirements
- Python 3.10+
- Redis
- (optional) Postgres / Docker

## Install
pip install -r requirements.txt
cp .env.example .env  
python manage.py migrate
python manage.py createsuperuser

Run Redis locally (or via Docker):
docker run -p 6379:6379 -d redis:7

Start Django dev server:
python manage.py runserver

Start Celery worker:
celery -A taskqueue_project worker --loglevel=info

Start Celery beat (optional):
celery -A taskqueue_project beat --loglevel=info

## Sample API flows

1. Register:
POST /api/register/
{ "username": "alice", "email": "...", "password": "..." }

2. Login:
POST /api/login/
{ "username": "alice", "password": "..." } -> returns access token

3. Create task:
POST /api/tasks/
Header: Authorization: Bearer <token>
{ "title": "Process files" }

4. Get task:
GET /api/tasks/<id>/

5. Delete:
DELETE /api/tasks/<id>/
