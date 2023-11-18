__all__ = ["models"]

from sqladmin import ModelView

from src.storages.sqlalchemy.models import User, Task, Machine, Agregate


class UserView(ModelView, model=User):
    form_excluded_columns = ["password_hash", "email_flows"]
    column_details_exclude_list = ["password_hash", "email_flows"]
    column_exclude_list = ["password_hash", "email_flows"]

    icon = "fa-solid fa-user"


class TaskView(ModelView, model=Task):
    icon = "fa-solid fa-user"

    form_excluded_columns = ["comments", "status_history", "created_at", "updated_at"]
    column_list = ["id", "title", "asignee", "description", "status", "priority", "location", "starting", "deadline"]


class MachineView(ModelView, model=Machine):
    icon = "fa-solid fa-building-wheat"

    form_excluded_columns = ["suitable_tasks", "current_task", "suitable_agregates"]
    column_list = ["id", "name", "type", "description", "status", "current_location"]


class AgregateView(ModelView, model=Agregate):
    icon = "fa-solid fa-list-check"

    form_excluded_columns = ["suitable_tasks", "current_task", "suitable_machines"]
    column_list = ["id", "name", "type", "description", "status", "current_location"]


models = [UserView, TaskView, MachineView, AgregateView]
