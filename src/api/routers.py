from src.modules.users.router import router as router_users
from src.modules.auth.router import router as router_auth
from src.modules.tasks.router import router as router_tasks

routers = [router_users, router_auth, router_tasks]

__all__ = ["routers"]
