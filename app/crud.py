from sqlalchemy.orm import Session

from app.models import Student


def get_all_students(db: Session):
    return db.query(Student).order_by(Student.id.asc()).all()


def get_student_by_id(db: Session, student_id: int):
    return db.query(Student).filter(Student.id == student_id).first()


def create_student(
    db: Session,
    name: str,
    age: int,
    group_name: str,
    gender: str,
):
    student = Student(
        name=name,
        age=age,
        group_name=group_name,
        gender=gender,
    )
    db.add(student)
    db.commit()
    db.refresh(student)
    return student


def update_student(
    db: Session,
    student_id: int,
    name: str,
    age: int,
    group_name: str,
    gender: str,
):
    student = get_student_by_id(db, student_id)
    if student is None:
        return None

    student.name = name
    student.age = age
    student.group_name = group_name
    student.gender = gender

    db.commit()
    db.refresh(student)
    return student


def delete_student(db: Session, student_id: int):
    student = get_student_by_id(db, student_id)
    if student is None:
        return None

    db.delete(student)
    db.commit()
    return student