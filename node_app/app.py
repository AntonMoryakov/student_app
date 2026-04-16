import os

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI(
    title="Node Identifier App",
    description="Мини-приложение для идентификации ноды",
    version="1.0.0",
)

templates = Jinja2Templates(directory="templates")


@app.get("/health")
def healthcheck() -> dict:
    return {"status": "ok"}


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    node_name = os.getenv("NODE_NAME", "Нода неизвестна")
    hostname = os.getenv("HOSTNAME", "unknown-host")

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "node_name": node_name,
            "hostname": hostname,
        },
    )