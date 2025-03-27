from typing import Type

from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
    PydanticBaseSettingsSource,
)

from vlt.json_source import PydanticJSONSource
from vlt.vault_source import PydanticVaultSource


class VaultJsonConfig(BaseSettings):
    model_config = SettingsConfigDict(populate_by_name=True)

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (
            env_settings,
            PydanticVaultSource(settings_cls),
            PydanticJSONSource(settings_cls),
            init_settings,
            dotenv_settings,
            file_secret_settings,
        )


__all__ = ["VaultJsonConfig"]
