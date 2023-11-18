__all__ = ["models"]

from sqladmin import ModelView

from src.storages.sqlalchemy.models import User, Task, Machine, Agregate
from src.storages.sqlalchemy.models.tasks import TaskType


class UserView(ModelView, model=User):
    form_excluded_columns = ["password_hash", "email_flows"]
    column_details_exclude_list = ["password_hash", "email_flows"]
    column_exclude_list = ["password_hash", "email_flows"]

    icon = "fa-solid fa-user"


class TaskView(ModelView, model=Task):
    icon = "fa-solid fa-circle-exclamation"

    form_columns = [
        "title",
        "type",
        "asignee",
        "status",
        "priority",
        "location",
        "starting",
        "deadline",
        # "work_volume",
        # "payment_coefficient",
        # "fuel_consumption",
        # "agregate_depth",
        # "agregate_working_speed",
        # "agregate_solvent_consumption",
        "current_machine",
        "current_agregate",
    ]
    column_list = ["id", "title", "asignee", "description", "status", "priority", "location", "starting", "deadline"]


class TaskTypeView(ModelView, model=TaskType):
    icon = "fa-solid fa-font"


class MachineView(ModelView, model=Machine):
    icon = "fa-solid fa-building-wheat"

    form_columns = [
        "name",
        "type",
        "description",
        "status",
        "current_location",
        "suitable_task_types",
        "suitable_agregates",
    ]
    column_list = ["id", "name", "type", "description", "status", "current_location"]


class AgregateView(ModelView, model=Agregate):
    icon = "fa-solid fa-list-check"

    form_columns = [
        "name",
        "type",
        "description",
        "status",
        "current_location",
        "suitable_task_types",
        "suitable_machines",
    ]

    column_list = ["id", "name", "type", "status", "current_location"]


models = [UserView, TaskView, MachineView, AgregateView, TaskTypeView]
