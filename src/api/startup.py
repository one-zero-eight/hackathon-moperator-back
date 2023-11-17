from src.config import settings


async def setup_repositories():
    from src.modules.users.repository import UserRepository
    from src.modules.smtp.repository import SMTPRepository
    from src.storages.sqlalchemy import SQLAlchemyStorage
    from src.api.dependencies import Dependencies

    # ------------------- Repositories Dependencies -------------------
    storage = SQLAlchemyStorage.from_url(settings.DB_URL.get_secret_value())
    user_repository = UserRepository(storage)

    Dependencies.set_storage(storage)
    Dependencies.set_user_repository(user_repository)

    if settings.SMTP_ENABLED:
        smtp_repository = SMTPRepository()
        Dependencies.set_smtp_repository(smtp_repository)

    # await storage.create_all()
