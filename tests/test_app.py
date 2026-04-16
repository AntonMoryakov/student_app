from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app

TEST_DATABASE_URL = "sqlite://"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def reset_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_index_page_opens():
    reset_database()

    response = client.get("/")
    assert response.status_code == 200
    assert "Система учета студентов" in response.text


def test_create_student():
    reset_database()

    response = client.post(
        "/students/create",
        data={
            "name": "Иван Петров",
            "age": 19,
            "group_name": "ИДБ-22-05",
            "gender": "М",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert "Иван Петров" in response.text
    assert "ИДБ-22-05" in response.text


def test_edit_student():
    reset_database()

    client.post(
        "/students/create",
        data={
            "name": "Мария Иванова",
            "age": 20,
            "group_name": "ИДБ-22-06",
            "gender": "Ж",
        },
        follow_redirects=True,
    )

    response = client.post(
        "/students/edit/1",
        data={
            "name": "Мария Смирнова",
            "age": 21,
            "group_name": "ИДБ-22-07",
            "gender": "Ж",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert "Мария Смирнова" in response.text
    assert "ИДБ-22-07" in response.text
    assert "21" in response.text


def test_delete_student():
    reset_database()

    client.post(
        "/students/create",
        data={
            "name": "Алексей Сидоров",
            "age": 18,
            "group_name": "ИДБ-22-08",
            "gender": "М",
        },
        follow_redirects=True,
    )

    response = client.post("/students/delete/1", follow_redirects=True)

    assert response.status_code == 200
    assert "Алексей Сидоров" not in response.text