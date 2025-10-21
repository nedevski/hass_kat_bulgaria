"""The KAT Bulgaria integration."""

from __future__ import annotations

import logging

from kat_bulgaria.data_models import PersonalIdentificationType

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .const import (
    CONF_DOCUMENT_NUMBER,
    CONF_DOCUMENT_TYPE,
    CONF_DRIVING_LICENSE,
    CONF_PERSON_EGN,
    CONF_PERSON_NAME,
    CONF_PERSON_TYPE,
    PersonType,
)
from .coordinator import KatBulgariaConfigEntry, KatBulgariaUpdateCoordinator

PLATFORMS: list[Platform] = [
    Platform.BINARY_SENSOR,
    Platform.SENSOR,
]

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: KatBulgariaConfigEntry) -> bool:
    """Set up KAT Bulgaria from a config entry."""

    coordinator = KatBulgariaUpdateCoordinator(hass, entry)
    await coordinator.async_config_entry_first_refresh()

    entry.runtime_data = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(
    hass: HomeAssistant, entry: KatBulgariaConfigEntry
) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)


async def async_migrate_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Migrate old entries."""

    _LOGGER.debug(
        "Migrating configuration from version %s.%s",
        config_entry.version,
        config_entry.minor_version,
    )

    if config_entry.version > 1:
        # This means the user has downgraded from a future version
        return False

    if config_entry.version == 1:
        old_data = {**config_entry.data}

        new_data = {}
        new_data[CONF_PERSON_TYPE] = PersonType.INDIVIDUAL
        new_data[CONF_PERSON_NAME] = old_data[CONF_PERSON_NAME]
        new_data[CONF_PERSON_EGN] = old_data[CONF_PERSON_EGN]
        new_data[CONF_DOCUMENT_NUMBER] = old_data[CONF_DRIVING_LICENSE]
        new_data[CONF_DOCUMENT_TYPE] = PersonalIdentificationType.DRIVING_LICENSE

        hass.config_entries.async_update_entry(
            config_entry, unique_id=config_entry.unique_id, data=new_data, version=2
        )

    _LOGGER.debug(
        "Migration to configuration version %s.%s successful",
        config_entry.version,
        config_entry.minor_version,
    )

    return True
