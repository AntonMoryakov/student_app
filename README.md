# Student App

Лабораторный проект по ОНИТ на тему учета студентов.

## Описание

Приложение реализует CRUD-операции для работы со студентами через ORM.

Поля студента:
- имя
- возраст
- группа
- пол

Используемый стек:
- FastAPI
- SQLAlchemy ORM
- PostgreSQL
- Jinja2
- Docker
- Docker Compose
- Pytest

---

## Структура проекта

```text
student_app/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   ├── config.py
│   ├── templates/
│   │   ├── index.html
│   │   ├── create.html
│   │   └── edit.html
│   └── static/
│       └── style.css
├── tests/
│   ├── __init__.py
│   └── test_app.py
├── docker/
│   └── entrypoint.sh
├── node_app/
│   ├── app.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── templates/
│       └── index.html
├── nginx/
│   └── nginx.conf
├── .env
├── .gitignore
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md