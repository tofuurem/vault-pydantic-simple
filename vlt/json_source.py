import json
import os
from pathlib import Path
from typing import Any

from loguru import logger
from pydantic_settings import PydanticBaseSettingsSource, BaseSettings

from pydantic.fields import FieldInfo

from vlt.constants import PYDANTIC_JSON_PATH


class PydanticJSONSource(PydanticBaseSettingsSource):
    def __init__(self, settings_cls: type[BaseSettings]) -> None:
        super().__init__(settings_cls)
        self._result_config = {}

    def get_field_value(
        self, field: FieldInfo, field_name: str
    ) -> tuple[Any, str, bool]:
        return self._result_config[field_name]

    def _get_secret_from_vault(self) -> None:
        path_env = os.getenv(PYDANTIC_JSON_PATH, default=None)
        with Path(path_env or os.path.dirname(__file__), "config.json").open("r") as f:
            self._result_config = json.load(f)

    def __call__(self) -> dict[str, Any]:
        try:
            self._get_secret_from_vault()
        except Exception as ex:
            logger.warning(f"Load config without config.json - {ex}")
        return self._result_config
