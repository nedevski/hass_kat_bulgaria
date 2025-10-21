"""DateUpdateCoordinator for Kat Bulgaria integration."""

import logging
from typing import Any

from kat_bulgaria.errors import KatError, KatErrorType

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import (
    CONF_BULSTAT,
    CONF_DOCUMENT_NUMBER,
    CONF_DOCUMENT_TYPE,
    CONF_PERSON_EGN,
    CONF_PERSON_NAME,
    CONF_PERSON_TYPE,
    COORD_DATA_KEY,
    DEFAULT_POLL_INTERVAL,
    DOMAIN,
    PersonType,
)
from .kat_client import KatClient

type KatBulgariaConfigEntry = ConfigEntry[KatBulgariaUpdateCoordinator]

_LOGGER = logging.getLogger(__name__)


class KatBulgariaUpdateCoordinator(DataUpdateCoordinator):
    """My custom coordinator."""

    config_entry: KatBulgariaConfigEntry
    client: KatClient

    def __init__(
        self,
        hass: HomeAssistant,
        config_entry: KatBulgariaConfigEntry,
    ) -> None:
        """Initialize coordinator."""

        person_type: str = config_entry.data[CONF_PERSON_TYPE]
        person_name: str = config_entry.data[CONF_PERSON_NAME]
        person_egn: str = config_entry.data[CONF_PERSON_EGN]
        document_number: str = config_entry.data[CONF_DOCUMENT_NUMBER]

        super().__init__(
            hass,
            logger=_LOGGER,
            config_entry=config_entry,
            name=f"KAT - {person_name}",
            update_interval=DEFAULT_POLL_INTERVAL,
        )

        assert self.config_entry.unique_id
        self.serial_number = self.config_entry.unique_id
        if person_type == PersonType.INDIVIDUAL:
            document_type: str = config_entry.data[CONF_DOCUMENT_TYPE]
            self.client = KatClient(
                hass, person_type, person_egn, document_number, document_type, None
            )
        elif person_type == PersonType.BUSINESS:
            bulstat: str = config_entry.data[CONF_BULSTAT]
            self.client = KatClient(
                hass, person_type, person_egn, document_number, None, bulstat
            )
        else:
            raise ValueError(f"Invalid person type: {person_type}")

    async def _async_update_data(self) -> dict[str, Any]:
        try:
            obligations = await self.client.get_obligations()

        except KatError as error:
            if error.error_type == KatErrorType.VALIDATION_ERROR:
                _LOGGER.warning(
                    "Invalid KAT API credentials, unable to update: %s",
                    error.error_type,
                )
                raise UpdateFailed(
                    translation_domain=DOMAIN,
                    translation_key="invalid_config",
                ) from error

            _LOGGER.warning(
                "KAT API down, unable to update: %s", error.error_type)
            raise UpdateFailed(
                translation_domain=DOMAIN,
                translation_key="update_error",
                translation_placeholders={"error": str(error)},
            ) from error

        return {COORD_DATA_KEY: obligations}
