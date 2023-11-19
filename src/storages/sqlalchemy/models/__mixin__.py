__all__ = ["IdMixin", "NoneImageType", "NoneFileType"]

from sqlalchemy.orm import Mapped, mapped_column
import os
from typing import Any, Optional

from PIL import Image
from fastapi_storages import StorageImage, StorageFile
from fastapi_storages.integrations.sqlalchemy import ImageType, FileType
from sqlalchemy import Dialect


class NoneImageType(ImageType):
    def process_result_value(self, value: Any, dialect: Dialect) -> Optional[StorageImage]:
        if value is None:
            return value

        image_path = self.storage.get_path(value)
        # if image does not exist
        if not os.path.exists(image_path):
            return None

        image = Image.open(self.storage.get_path(value))
        return StorageImage(name=value, storage=self.storage, height=image.height, width=image.width)

    def process_bind_param(self, value: Any, dialect: Dialect) -> Optional[str]:
        if isinstance(value, StorageFile):
            return value.name
        return super().process_bind_param(value, dialect)


class NoneFileType(FileType):
    def process_result_value(self, value: Any, dialect: Dialect) -> Optional[StorageFile]:
        if value is None:
            return value

        # check if file exists
        file_path = self.storage.get_path(value)
        if not os.path.exists(file_path):
            return None

        return StorageFile(name=value, storage=self.storage)

    def process_bind_param(self, value: Any, dialect: Dialect) -> Optional[str]:
        if isinstance(value, StorageFile):
            return value.name
        return super().process_bind_param(value, dialect)


class IdMixin:
    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
