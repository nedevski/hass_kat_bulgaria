"""Coordinator."""

import pytest

from homeassistant.config_entries import ConfigEntryState
from homeassistant.core import HomeAssistant

from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.kat_bulgaria.const import COORD_DATA_KEY

from . import (
    BULSTAT_VALID,
    EGN_VALID,
    GOV_ID_VALID,
    LICENSE_VALID,
    PersonalIdentificationType,
    PersonType,
)


@pytest.mark.asyncio
async def test_coordinator_setup_ok_individual(
    hass: HomeAssistant,
    config_entry_v2_individual: MockConfigEntry,
    mock_get_obligations_ok_nodata,
) -> None:
    """Test that the coordinator can update."""
    assert config_entry_v2_individual.state == ConfigEntryState.NOT_LOADED
    config_entry_v2_individual.add_to_hass(hass)

    result = await hass.config_entries.async_setup(config_entry_v2_individual.entry_id)
    await hass.async_block_till_done()

    assert result is True
    assert config_entry_v2_individual.state == ConfigEntryState.LOADED

    coordinator = config_entry_v2_individual.runtime_data
    assert coordinator
    assert coordinator.client.person_type == PersonType.INDIVIDUAL
    assert coordinator.client.person_egn == EGN_VALID
    assert coordinator.client.person_identifier == LICENSE_VALID
    assert (
        coordinator.client.person_identifier_type == PersonalIdentificationType.DRIVING_LICENSE
    )
    assert coordinator.client.bulstat is None

    assert coordinator.client.get_obligations.call_count == 1
    assert coordinator.data == {COORD_DATA_KEY: []}


@pytest.mark.asyncio
async def test_coordinator_setup_ok_business(
    hass: HomeAssistant,
    config_entry_v2_business: MockConfigEntry,
    mock_get_obligations_ok_nodata,
) -> None:
    """Test that the coordinator can update."""
    assert config_entry_v2_business.state == ConfigEntryState.NOT_LOADED
    config_entry_v2_business.add_to_hass(hass)

    result = await hass.config_entries.async_setup(config_entry_v2_business.entry_id)
    await hass.async_block_till_done()

    assert result is True
    assert config_entry_v2_business.state == ConfigEntryState.LOADED

    coordinator = config_entry_v2_business.runtime_data
    assert coordinator
    assert coordinator.client.person_type == PersonType.BUSINESS
    assert coordinator.client.person_egn == EGN_VALID
    assert coordinator.client.person_identifier == GOV_ID_VALID
    assert coordinator.client.bulstat == BULSTAT_VALID

    assert coordinator.client.get_obligations.call_count == 1
    assert coordinator.data == {COORD_DATA_KEY: []}


@pytest.mark.asyncio
async def test_coordinator_setup_id_document_invalid_individual(
    hass: HomeAssistant,
    config_entry_v2_individual: MockConfigEntry,
    mock_get_obligations_err_driving_license_invalid,
) -> None:
    """Test that the coordinator can update."""
    assert config_entry_v2_individual.state == ConfigEntryState.NOT_LOADED
    config_entry_v2_individual.add_to_hass(hass)

    result = await hass.config_entries.async_setup(config_entry_v2_individual.entry_id)
    await hass.async_block_till_done()

    assert result is False
    assert config_entry_v2_individual.state == ConfigEntryState.SETUP_RETRY


@pytest.mark.asyncio
async def test_coordinator_setup_id_document_invalid_business(
    hass: HomeAssistant,
    config_entry_v2_business: MockConfigEntry,
    mock_get_obligations_err_gov_id_number_invalid,
) -> None:
    """Test that the coordinator can update."""
    assert config_entry_v2_business.state == ConfigEntryState.NOT_LOADED
    config_entry_v2_business.add_to_hass(hass)

    result = await hass.config_entries.async_setup(config_entry_v2_business.entry_id)
    await hass.async_block_till_done()

    assert result is False
    assert config_entry_v2_business.state == ConfigEntryState.SETUP_RETRY


@pytest.mark.asyncio
async def test_coordinator_setup_bulstat_invalid_business(
    hass: HomeAssistant,
    config_entry_v2_business: MockConfigEntry,
    mock_get_obligations_err_bulstat_invalid,
) -> None:
    """Test that the coordinator can update."""
    assert config_entry_v2_business.state == ConfigEntryState.NOT_LOADED
    config_entry_v2_business.add_to_hass(hass)

    result = await hass.config_entries.async_setup(config_entry_v2_business.entry_id)
    await hass.async_block_till_done()

    assert result is False
    assert config_entry_v2_business.state == ConfigEntryState.SETUP_RETRY


@pytest.mark.asyncio
async def test_coordinator_setup_usernotfoundonline_individual(
    hass: HomeAssistant,
    config_entry_v2_individual: MockConfigEntry,
    mock_get_obligations_err_usernotfound,
) -> None:
    """Test that the coordinator can update."""
    assert config_entry_v2_individual.state == ConfigEntryState.NOT_LOADED
    config_entry_v2_individual.add_to_hass(hass)

    result = await hass.config_entries.async_setup(config_entry_v2_individual.entry_id)
    await hass.async_block_till_done()

    assert result is False
    assert config_entry_v2_individual.state == ConfigEntryState.SETUP_RETRY


@pytest.mark.asyncio
async def test_coordinator_setup_usernotfoundonline_business(
    hass: HomeAssistant,
    config_entry_v2_business: MockConfigEntry,
    mock_get_obligations_err_usernotfound,
) -> None:
    """Test that the coordinator can update."""
    assert config_entry_v2_business.state == ConfigEntryState.NOT_LOADED
    config_entry_v2_business.add_to_hass(hass)

    result = await hass.config_entries.async_setup(config_entry_v2_business.entry_id)
    await hass.async_block_till_done()

    assert result is False
    assert config_entry_v2_business.state == ConfigEntryState.SETUP_RETRY


@pytest.mark.asyncio
async def test_coordinator_setup_api_timeout_individual(
    hass: HomeAssistant,
    config_entry_v2_individual: MockConfigEntry,
    mock_get_obligations_err_api_timeout,
) -> None:
    """Test that the coordinator can update."""
    assert config_entry_v2_individual.state == ConfigEntryState.NOT_LOADED
    config_entry_v2_individual.add_to_hass(hass)

    result = await hass.config_entries.async_setup(config_entry_v2_individual.entry_id)
    await hass.async_block_till_done()

    assert result is False
    assert config_entry_v2_individual.state == ConfigEntryState.SETUP_RETRY


@pytest.mark.asyncio
async def test_coordinator_setup_api_timeout_business(
    hass: HomeAssistant,
    config_entry_v2_business: MockConfigEntry,
    mock_get_obligations_err_api_timeout,
) -> None:
    """Test that the coordinator can update."""
    assert config_entry_v2_business.state == ConfigEntryState.NOT_LOADED
    config_entry_v2_business.add_to_hass(hass)

    result = await hass.config_entries.async_setup(config_entry_v2_business.entry_id)
    await hass.async_block_till_done()

    assert result is False
    assert config_entry_v2_business.state == ConfigEntryState.SETUP_RETRY


@pytest.mark.asyncio
async def test_coordinator_setup_api_toomanyrequests_individual(
    hass: HomeAssistant,
    config_entry_v2_individual: MockConfigEntry,
    mock_get_obligations_err_api_toomanyrequests,
) -> None:
    """Test that the coordinator can update."""
    assert config_entry_v2_individual.state == ConfigEntryState.NOT_LOADED
    config_entry_v2_individual.add_to_hass(hass)

    result = await hass.config_entries.async_setup(config_entry_v2_individual.entry_id)
    await hass.async_block_till_done()

    assert result is False
    assert config_entry_v2_individual.state == ConfigEntryState.SETUP_RETRY


@pytest.mark.asyncio
async def test_coordinator_setup_api_toomanyrequests_business(
    hass: HomeAssistant,
    config_entry_v2_business: MockConfigEntry,
    mock_get_obligations_err_api_toomanyrequests,
) -> None:
    """Test that the coordinator can update."""
    assert config_entry_v2_business.state == ConfigEntryState.NOT_LOADED
    config_entry_v2_business.add_to_hass(hass)

    result = await hass.config_entries.async_setup(config_entry_v2_business.entry_id)
    await hass.async_block_till_done()

    assert result is False
    assert config_entry_v2_business.state == ConfigEntryState.SETUP_RETRY


@pytest.mark.asyncio
async def test_coordinator_setup_api_error_reading_data_individual(
    hass: HomeAssistant,
    config_entry_v2_individual: MockConfigEntry,
    mock_get_obligations_err_api_errorreadingdata,
) -> None:
    """Test that the coordinator can update."""
    assert config_entry_v2_individual.state == ConfigEntryState.NOT_LOADED
    config_entry_v2_individual.add_to_hass(hass)

    result = await hass.config_entries.async_setup(config_entry_v2_individual.entry_id)
    await hass.async_block_till_done()

    assert result is False
    assert config_entry_v2_individual.state == ConfigEntryState.SETUP_RETRY


@pytest.mark.asyncio
async def test_coordinator_setup_api_error_reading_data_business(
    hass: HomeAssistant,
    config_entry_v2_business: MockConfigEntry,
    mock_get_obligations_err_api_errorreadingdata,
) -> None:
    """Test that the coordinator can update."""
    assert config_entry_v2_business.state == ConfigEntryState.NOT_LOADED
    config_entry_v2_business.add_to_hass(hass)

    result = await hass.config_entries.async_setup(config_entry_v2_business.entry_id)
    await hass.async_block_till_done()

    assert result is False
    assert config_entry_v2_business.state == ConfigEntryState.SETUP_RETRY


@pytest.mark.asyncio
async def test_coordinator_setup_api_invalidschema_individual(
    hass: HomeAssistant,
    config_entry_v2_individual: MockConfigEntry,
    mock_get_obligations_err_api_invalidschema,
) -> None:
    """Test that the coordinator can update."""
    assert config_entry_v2_individual.state == ConfigEntryState.NOT_LOADED
    config_entry_v2_individual.add_to_hass(hass)

    result = await hass.config_entries.async_setup(config_entry_v2_individual.entry_id)
    await hass.async_block_till_done()

    assert result is False
    assert config_entry_v2_individual.state == ConfigEntryState.SETUP_RETRY


@pytest.mark.asyncio
async def test_coordinator_setup_api_invalidschema_business(
    hass: HomeAssistant,
    config_entry_v2_business: MockConfigEntry,
    mock_get_obligations_err_api_invalidschema,
) -> None:
    """Test that the coordinator can update."""
    assert config_entry_v2_business.state == ConfigEntryState.NOT_LOADED
    config_entry_v2_business.add_to_hass(hass)

    result = await hass.config_entries.async_setup(config_entry_v2_business.entry_id)
    await hass.async_block_till_done()

    assert result is False
    assert config_entry_v2_business.state == ConfigEntryState.SETUP_RETRY


@pytest.mark.asyncio
async def test_coordinator_setup_api_unknownerror_individual(
    hass: HomeAssistant,
    config_entry_v2_individual: MockConfigEntry,
    mock_get_obligations_err_api_unknown,
) -> None:
    """Test that the coordinator can update."""
    assert config_entry_v2_individual.state == ConfigEntryState.NOT_LOADED
    config_entry_v2_individual.add_to_hass(hass)

    result = await hass.config_entries.async_setup(config_entry_v2_individual.entry_id)
    await hass.async_block_till_done()

    assert result is False
    assert config_entry_v2_individual.state == ConfigEntryState.SETUP_RETRY


@pytest.mark.asyncio
async def test_coordinator_setup_api_unknownerror_business(
    hass: HomeAssistant,
    config_entry_v2_business: MockConfigEntry,
    mock_get_obligations_err_api_unknown,
) -> None:
    """Test that the coordinator can update."""
    assert config_entry_v2_business.state == ConfigEntryState.NOT_LOADED
    config_entry_v2_business.add_to_hass(hass)

    result = await hass.config_entries.async_setup(config_entry_v2_business.entry_id)
    await hass.async_block_till_done()

    assert result is False
    assert config_entry_v2_business.state == ConfigEntryState.SETUP_RETRY


@pytest.mark.asyncio
async def test_coordinator_setup_invalid_person_type(
    hass: HomeAssistant,
    config_entry_v2_invalid_person_type: MockConfigEntry,
    mock_get_obligations_ok_nodata,
) -> None:
    """Test that the coordinator can update."""
    assert config_entry_v2_invalid_person_type.state == ConfigEntryState.NOT_LOADED
    config_entry_v2_invalid_person_type.add_to_hass(hass)

    result = await hass.config_entries.async_setup(config_entry_v2_invalid_person_type.entry_id)
    await hass.async_block_till_done()

    assert result is False
    assert config_entry_v2_invalid_person_type.state == ConfigEntryState.SETUP_ERROR
