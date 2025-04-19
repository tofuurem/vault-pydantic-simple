from typing import Self

from hvac.api.secrets_engines.kv_v2 import DEFAULT_MOUNT_POINT
from pydantic import Field, model_validator, ValidationError

from pydantic_settings import BaseSettings


class VaultAccess(BaseSettings):
    address: str = Field(alias="VAULT_ADDRESS")
    token: str | None = Field(alias="VAULT_TOKEN", default=None)
    username: str | None = Field(alias="VAULT_USERNAME", default=None)
    password: str | None = Field(alias="VAULT_PASSWORD", default=None)
    app_name: str = Field(alias="VAULT_APP_NAME")
    mount_point: str = Field(alias="VAULT_MOUNT_POINT", default=DEFAULT_MOUNT_POINT)

    @model_validator(mode="after")
    def validate_creds(self) -> Self:
        if self.token is None and (self.username is None or self.password is None):
            raise ValidationError(
                "Must be some fields for auth token or username + password"
            )
        return self
