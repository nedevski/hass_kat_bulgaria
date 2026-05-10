"""Test migrating from v1 to v2."""

import pytest

from homeassistant.config_entries import ConfigEntryState
from homeassistant.core import HomeAssistant

from pytest_homeassistant_custom_component.common import MockConfigEntry

from . import (
    EGN_VALID,
    MOCK_DATA_INDIVIDUAL_FULL,
)


@pytest.mark.asyncio
async def test_init_migration_from_v1(
    hass: HomeAssistant,
    config_entry_v1: MockConfigEntry,
    mock_get_obligations_ok_nodata
) -> None:
    """Test migration from v1 to v2."""

    config_entry_v1.add_to_hass(hass)

    await hass.config_entries.async_setup(config_entry_v1.entry_id)
    await hass.async_block_till_done()

    assert len(hass.config_entries.flow.async_progress()) == 0
    assert config_entry_v1.state is ConfigEntryState.LOADED
    assert config_entry_v1.version == 2
    assert config_entry_v1.unique_id == EGN_VALID
    assert config_entry_v1.data == MOCK_DATA_INDIVIDUAL_FULL


@pytest.mark.asyncio
async def test_init_migration_from_v2(
    hass: HomeAssistant,
    config_entry_v2_individual: MockConfigEntry,
    mock_get_obligations_ok_nodata
) -> None:
    """Test migration from v1 to v2."""

    config_entry_v2_individual.add_to_hass(hass)

    await hass.config_entries.async_setup(config_entry_v2_individual.entry_id)
    await hass.async_block_till_done()

    assert len(hass.config_entries.flow.async_progress()) == 0
    assert config_entry_v2_individual.state is ConfigEntryState.LOADED
    assert config_entry_v2_individual.version == 2
    assert config_entry_v2_individual.unique_id == EGN_VALID
    assert config_entry_v2_individual.data == MOCK_DATA_INDIVIDUAL_FULL
