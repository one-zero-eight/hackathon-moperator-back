from src.modules.users.router import router as router_users
from src.modules.auth.router import router as router_auth
from src.modules.tasks.router import router as router_tasks
from src.modules.machines.router import router as router_machines
from src.modules.agregates.router import router as router_agregates

routers = [router_users, router_auth, router_tasks, router_machines, router_agregates]

__all__ = ["routers"]
