import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    def __init__(self) -> None:
        self.db_host = os.getenv("DB_HOST", "localhost")
        self.db_port = os.getenv("DB_PORT", "5432")
        self.db_name = os.getenv("DB_NAME", "students_db")
        self.db_user = os.getenv("DB_USER", "student_user")
        self.db_password = os.getenv("DB_PASSWORD", "student_pass")


settings = Settings()