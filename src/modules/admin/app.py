__all__ = ["init_app"]

from typing import Optional, Union, Sequence

from fastapi import FastAPI
from sqladmin import Admin

# noinspection PyProtectedMember
from sqladmin._types import ENGINE_TYPE
from sqladmin.authentication import AuthenticationBackend
from sqlalchemy import Engine
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker
from sqlalchemy.orm import sessionmaker
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.routing import Mount, Route
from starlette.staticfiles import StaticFiles

from src.modules.admin.auth import authentication_backend
from src.modules.admin.views import models


class CustomAdmin(Admin):
    def __init__(
        self,
        app: Starlette,
        engine: Optional[ENGINE_TYPE] = None,
        session_maker: Optional[Union[sessionmaker, "async_sessionmaker"]] = None,
        base_url: str = "/admin",
        title: str = "Admin",
        logo_url: Optional[str] = None,
        middlewares: Optional[Sequence[Middleware]] = None,
        debug: bool = False,
        templates_dir: str = "templates",
        authentication_backend: Optional[AuthenticationBackend] = None,
    ) -> None:
        """
        Args:
            app: Starlette or FastAPI application.
            engine: SQLAlchemy engine instance.
            session_maker: SQLAlchemy sessionmaker instance.
            base_url: Base URL for Admin interface.
            title: Admin title.
            logo_url: URL of logo to be displayed instead of title.
        """

        super(Admin, self).__init__(
            app=app,
            engine=engine,
            session_maker=session_maker,
            base_url=base_url,
            title=title,
            logo_url=logo_url,
            templates_dir=templates_dir,
            middlewares=middlewares,
            authentication_backend=authentication_backend,
        )

        statics = StaticFiles(directory="src/modules/admin/statics", packages=["sqladmin"])

        # def http_exception(request: Request, exc: Exception) -> Response:
        #     assert isinstance(exc, HTTPException)
        #     context = {
        #         "status_code": exc.status_code,
        #         "message": exc.detail,
        #     }
        #     return self.templates.TemplateResponse(
        #         request, "error.html", context, status_code=exc.status_code
        #     )

        routes = [
            Mount("/statics", app=statics, name="statics"),
            Route("/", endpoint=self.index, name="index"),
            Route("/{identity}/list", endpoint=self.list, name="list"),
            Route("/{identity}/details/{pk:path}", endpoint=self.details, name="details"),
            Route(
                "/{identity}/delete",
                endpoint=self.delete,
                name="delete",
                methods=["DELETE"],
            ),
            Route(
                "/{identity}/create",
                endpoint=self.create,
                name="create",
                methods=["GET", "POST"],
            ),
            Route(
                "/{identity}/edit/{pk:path}",
                endpoint=self.edit,
                name="edit",
                methods=["GET", "POST"],
            ),
            Route("/{identity}/export/{export_type}", endpoint=self.export, name="export"),
            Route("/{identity}/ajax/lookup", endpoint=self.ajax_lookup, name="ajax_lookup"),
            Route("/login", endpoint=self.login, name="login", methods=["GET", "POST"]),
            Route("/logout", endpoint=self.logout, name="logout", methods=["GET"]),
        ]

        self.admin.router.routes = routes
        # self.admin.exception_handlers = {HTTPException: http_exception}
        self.admin.debug = debug
        self.app.mount(base_url, app=self.admin, name="admin")


def init_app(app: FastAPI, engine: Engine | AsyncEngine):
    admin = CustomAdmin(
        app,
        engine,
        authentication_backend=authentication_backend,
        templates_dir="src/modules/admin/templates",
    )

    for model in models:
        admin.add_view(model)
