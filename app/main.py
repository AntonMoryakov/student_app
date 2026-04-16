from pathlib import Path

from fastapi import Depends, FastAPI, Form, HTTPException, Request, status
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app import models
from app.crud import (
    create_student,
    delete_student,
    get_all_students,
    get_student_by_id,
    update_student,
)
from app.database import Base, engine, get_db

app = FastAPI(
    title="Student Management App",
    description="CRUD-приложение для учета студентов",
    version="1.0.0",
)

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")


@app.on_event("startup")
def on_startup() -> None:
    Base.metadata.create_all(bind=engine)


@app.get("/health", response_class=JSONResponse)
def healthcheck() -> dict:
    return {"status": "ok"}


@app.get("/", response_class=HTMLResponse)
def index(request: Request, db: Session = Depends(get_db)) -> HTMLResponse:
    students = get_all_students(db)
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "students": students,
        },
    )


@app.get("/students/create", response_class=HTMLResponse)
def create_student_page(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        "create.html",
        {
            "request": request,
            "error": None,
            "form_data": {
                "name": "",
                "age": "",
                "group_name": "",
                "gender": "",
            },
        },
    )


@app.post("/students/create", response_class=HTMLResponse)
def create_student_action(
    request: Request,
    name: str = Form(...),
    age: int = Form(...),
    group_name: str = Form(...),
    gender: str = Form(...),
    db: Session = Depends(get_db),
):
    name = name.strip()
    group_name = group_name.strip()
    gender = gender.strip()

    form_data = {
        "name": name,
        "age": age,
        "group_name": group_name,
        "gender": gender,
    }

    if not name:
        return templates.TemplateResponse(
            "create.html",
            {
                "request": request,
                "error": "Имя не может быть пустым.",
                "form_data": form_data,
            },
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    if age < 14 or age > 120:
        return templates.TemplateResponse(
            "create.html",
            {
                "request": request,
                "error": "Возраст должен быть в диапазоне от 14 до 120.",
                "form_data": form_data,
            },
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    if not group_name:
        return templates.TemplateResponse(
            "create.html",
            {
                "request": request,
                "error": "Поле группы не может быть пустым.",
                "form_data": form_data,
            },
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    if gender not in {"М", "Ж"}:
        return templates.TemplateResponse(
            "create.html",
            {
                "request": request,
                "error": "Пол должен быть 'М' или 'Ж'.",
                "form_data": form_data,
            },
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    create_student(
        db=db,
        name=name,
        age=age,
        group_name=group_name,
        gender=gender,
    )

    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)


@app.get("/students/edit/{student_id}", response_class=HTMLResponse)
def edit_student_page(
    student_id: int,
    request: Request,
    db: Session = Depends(get_db),
) -> HTMLResponse:
    student = get_student_by_id(db, student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Студент не найден")

    return templates.TemplateResponse(
        "edit.html",
        {
            "request": request,
            "student": student,
            "error": None,
        },
    )


@app.post("/students/edit/{student_id}", response_class=HTMLResponse)
def edit_student_action(
    student_id: int,
    request: Request,
    name: str = Form(...),
    age: int = Form(...),
    group_name: str = Form(...),
    gender: str = Form(...),
    db: Session = Depends(get_db),
):
    student = get_student_by_id(db, student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Студент не найден")

    name = name.strip()
    group_name = group_name.strip()
    gender = gender.strip()

    if not name:
        student.name = name
        student.age = age
        student.group_name = group_name
        student.gender = gender
        return templates.TemplateResponse(
            "edit.html",
            {
                "request": request,
                "student": student,
                "error": "Имя не может быть пустым.",
            },
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    if age < 14 or age > 120:
        student.name = name
        student.age = age
        student.group_name = group_name
        student.gender = gender
        return templates.TemplateResponse(
            "edit.html",
            {
                "request": request,
                "student": student,
                "error": "Возраст должен быть в диапазоне от 14 до 120.",
            },
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    if not group_name:
        student.name = name
        student.age = age
        student.group_name = group_name
        student.gender = gender
        return templates.TemplateResponse(
            "edit.html",
            {
                "request": request,
                "student": student,
                "error": "Поле группы не может быть пустым.",
            },
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    if gender not in {"М", "Ж"}:
        student.name = name
        student.age = age
        student.group_name = group_name
        student.gender = gender
        return templates.TemplateResponse(
            "edit.html",
            {
                "request": request,
                "student": student,
                "error": "Пол должен быть 'М' или 'Ж'.",
            },
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    update_student(
        db=db,
        student_id=student_id,
        name=name,
        age=age,
        group_name=group_name,
        gender=gender,
    )

    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)


@app.post("/students/delete/{student_id}")
def delete_student_action(
    student_id: int,
    db: Session = Depends(get_db),
):
    student = get_student_by_id(db, student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Студент не найден")

    delete_student(db, student_id)
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)