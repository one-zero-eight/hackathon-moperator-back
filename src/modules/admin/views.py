__all__ = ["models"]

import datetime

from sqladmin import ModelView
from sqlalchemy.orm import InstrumentedAttribute
from starlette.requests import Request

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


class UserView(ModelView, model=User):
    form_excluded_columns = ["email_flows"]
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
    ]

    column_list = ["id", "title", "asignee", "description", "status", "priority", "location", "starting", "deadline", "attachments"]
    column_details_exclude_list = [
        "current_machine_id",
        "current_agregate_id",
        "id",
        "comments",
        "type_id",
        "asignee_id",
        "created_at",
        "updated_at",
    ]


class TaskTypeView(ModelView, model=TaskType):
    icon = "fa-solid fa-font"

    column_list = ["id", "title", "description"]


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
    column_list = ["id", "name", "type", "status", "current_location", "tasks", "attachments"]


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

    column_list = ["id", "name", "type", "status", "current_location", "tasks"]


models = [UserView, TaskView, MachineView, AgregateView, TaskTypeView]
