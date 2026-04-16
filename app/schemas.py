from pydantic import BaseModel, Field, field_validator


class StudentBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    age: int = Field(..., ge=14, le=120)
    group_name: str = Field(..., min_length=1, max_length=50)
    gender: str = Field(..., min_length=1, max_length=10)

    @field_validator("name", "group_name", "gender")
    @classmethod
    def strip_and_validate_not_empty(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Поле не может быть пустым")
        return value

    @field_validator("gender")
    @classmethod
    def validate_gender(cls, value: str) -> str:
        if value not in {"М", "Ж"}:
            raise ValueError("Пол должен быть 'М' или 'Ж'")
        return value


class StudentCreate(StudentBase):
    pass


class StudentUpdate(StudentBase):
    pass


class StudentRead(StudentBase):
    id: int

    model_config = {"from_attributes": True}