from sqlalchemy import Column, Integer, String

from app.database import Base


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    age = Column(Integer, nullable=False)
    group_name = Column(String(50), nullable=False)
    gender = Column(String(10), nullable=False)

    def __repr__(self) -> str:
        return (
            f"Student(id={self.id}, name='{self.name}', age={self.age}, "
            f"group_name='{self.group_name}', gender='{self.gender}')"
        )