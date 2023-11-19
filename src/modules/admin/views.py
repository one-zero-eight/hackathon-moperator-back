__all__ = ["models"]

import datetime

from passlib.context import CryptContext
from sqladmin import ModelView, action
from sqlalchemy.orm import InstrumentedAttribute, make_transient
from starlette.requests import Request
from starlette.responses import RedirectResponse

from src.api.dependencies import Dependencies
from src.modules.users.schemas import Notification
from src.storages.sqlalchemy.models import User, Task, Machine, Agregate
from src.storages.sqlalchemy.models.tasks import TaskType


class CustomTaskModelView(ModelView):
    export_columns: list[str | InstrumentedAttribute] = None

    def get_export_columns(self) -> list[str]:
        """Get list of properties to export."""

        return self._build_column_list(
            include=self.export_columns,
            defaults=self._list_prop_names,
        )

    async def on_model_change(self, data: dict, model: Task, is_created: bool, request: Request) -> None:
        """Called when creating or updating a model."""

        new_status = data.get("status")

        if new_status is None or new_status == "draft":
            return

        if model.status == new_status:
            return

        if model.asignee_id is None:
            return

        user_repository = Dependencies.get_user_repository()
        user_repository.add_notification(
            int(model.asignee_id),
            Notification(
                title="Задание изменило статус!",
                description=f"'{model.title}' теперь имеет статус '{new_status}'\n"
                f"Время: {datetime.datetime.now().strftime('%d.%m.%Y %H:%M')}",
                created_at=datetime.datetime.now(),
            ),
        )


class CustomUserModelView(ModelView):
    async def on_model_change(self, data: dict, model: User, is_created: bool, request: Request) -> None:
        # get password from form
        password = data.get("password_hash")

        if password is None:
            return

            # hash password
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        hashed_password = pwd_context.hash(password)

        data["password_hash"] = hashed_password


class UserView(CustomUserModelView, model=User):
    form_columns = [
        "email",
        "password_hash",
        "first_name",
        "last_name",
        "middle_name",
        "role",
        "rfid_id",
        "photo",
    ]
    form_args = {"password_hash": {"label": "Пароль"}}

    column_details_exclude_list = ["password_hash", "email_flows"]
    column_exclude_list = ["password_hash", "email_flows"]

    icon = "fa-solid fa-user"


class TaskView(CustomTaskModelView, model=Task):
    icon = "fa-solid fa-circle-exclamation"

    export_columns = [
        "id",
        "title",
        "type",
        "asignee",
        "status",
        "priority",
        "location",
        "starting",
        "deadline",
        "description",
        "current_machine",
        "current_agregate",
    ]

    form_columns = [
        "title",
        "type",
        "asignee",
        "status",
        "priority",
        "location",
        "starting",
        "deadline",
        "description",
        # "work_volume",
        # "payment_coefficient",
        # "fuel_consumption",
        # "agregate_depth",
        # "agregate_working_speed",
        # "agregate_solvent_consumption",
        "current_machine",
        "current_agregate",
        "attachments",
    ]

    column_list = [
        "id",
        "title",
        "description",
        "type",
        "asignee",
        "status",
        "priority",
        "location",
        "starting",
        "deadline",
        "attachments",
    ]

    column_details_exclude_list = []

    @action(
        name="Copy",
        label="Copy",
        add_in_detail=True,
        add_in_list=True,
    )
    async def copy_task(self, request: Request):
        pks = request.query_params.get("pks", "").split(",")
        if pks:
            for pk in pks:
                model: Task = await self.get_object_for_edit(pk)
                # create new
                make_transient(model)
                model.id = None
                model.title = f"Копия {model.title}"
                model.status = "draft"
                # process attachments

                # save
                await self.on_model_change({}, model, True, request)

                async with self.session_maker() as session:
                    session.add(model)
                    await session.commit()

        referer = request.headers.get("Referer")

        if referer:
            return RedirectResponse(referer)
        else:
            return RedirectResponse(request.url_for("admin:list", identity=self.identity))


class TaskTypeView(ModelView, model=TaskType):
    icon = "fa-solid fa-font"

    column_list = ["id", "title", "description", "tasks", "suitable_machines", "suitable_agregates"]


class MachineView(ModelView, model=Machine):
    icon = "fa-solid fa-building-wheat"

    list_template = "custom_list.html"

    form_columns = [
        "name",
        "type",
        "description",
        "status",
        "current_location",
        "suitable_task_types",
        "suitable_agregates",
        "attachments",
    ]
    # !!! Description should be 3rd
    column_list = ["id", "name", "description", "type", "status", "current_location", "tasks", "attachments"]


class AgregateView(ModelView, model=Agregate):
    icon = "fa-solid fa-list-check"

    list_template = "custom_list.html"

    form_columns = [
        "name",
        "type",
        "description",
        "status",
        "current_location",
        "suitable_task_types",
        "suitable_machines",
    ]

    # !!! Description should be 3rd
    column_list = ["id", "name", "description", "type", "status", "current_location", "tasks"]


models = [UserView, TaskView, MachineView, AgregateView, TaskTypeView]
