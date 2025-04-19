from typing import Any

from loguru import logger
from pydantic.fields import FieldInfo

from pydantic_settings import BaseSettings, PydanticBaseSettingsSource

import hvac

from vlt.config import VaultAccess


def _auth_by_userpass(cfg: VaultAccess) -> hvac.Client:
    if cfg.token:
        client = hvac.Client(url=cfg.address, token=cfg.token)
        if not client.is_authenticated():
            raise ValueError("Can't auth in Vault")
        return client
    else:
        client = hvac.Client(url=cfg.address)
        resp = client.auth.userpass.login(username=cfg.username, password=cfg.password)
        client.token = resp["auth"]["client_token"]
        return client


class PydanticVaultSource(PydanticBaseSettingsSource):
    def __init__(self, settings_cls: type[BaseSettings]) -> None:
        super().__init__(settings_cls)
        self._result_config = {}

    def get_field_value(
        self, field: FieldInfo, field_name: str
    ) -> tuple[Any, str, bool]:
        return self._result_config[field_name]

    def _get_secret_from_vault(self) -> None:
        cfg = VaultAccess()
        client = _auth_by_userpass(cfg)
        secret = client.secrets.kv.v2.read_secret_version(path=cfg.app_name, mount_point=cfg.mount_point)
        self._result_config = secret["data"]["data"]

    def __call__(self) -> dict[str, Any]:
        try:
            self._get_secret_from_vault()
        except Exception as ex:
            logger.error(ex)
        return self._result_config
