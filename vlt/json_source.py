import json
import os
from pathlib import Path
from typing import Any

from pydantic_settings import PydanticBaseSettingsSource, BaseSettings
from pydantic import FieldInfo

from vlt.constants import PYDANTIC_JSON_PATH


class PydanticJSONSource(PydanticBaseSettingsSource):

    def __init__(self, settings_cls: type[BaseSettings]) -> None:
        super().__init__(settings_cls)
        self._result_config = {}

    def get_field_value(self, field: FieldInfo, field_name: str) -> tuple[Any, str, bool]:
        return self._result_config[field_name]

    def _get_secret_from_vault(self) -> None:
        path_env = os.getenv(PYDANTIC_JSON_PATH, default=None)
        if path_env is None:
            return
        file = Path(path_env)
        with open(file, 'r') as f:
            self._result_config = json.load(f)

    def __call__(self) -> dict[str, Any]:
        self._get_secret_from_vault()
        return self._result_config
