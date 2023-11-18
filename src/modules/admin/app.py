__all__ = ["init_app"]

from sqladmin import Admin
from fastapi import FastAPI
from sqlalchemy import Engine
from sqlalchemy.ext.asyncio import AsyncEngine

from src.modules.admin.views import models
from src.modules.admin.auth import authentication_backend


def init_app(app: FastAPI, engine: Engine | AsyncEngine):
    admin = Admin(app, engine, authentication_backend=authentication_backend)

    for model in models:
        admin.add_view(model)
