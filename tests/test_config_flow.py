"""Test KAT Bulgaria setup process."""

from unittest.mock import AsyncMock, patch

from kat_bulgaria.errors import KatError, KatErrorSubtype, KatErrorType
import pytest

from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResultType

from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.kat_bulgaria import const as kat_constants
from custom_components.kat_bulgaria.config_flow import (
    STEP_ID_BUSINESS,
    STEP_ID_INDIVIDUAL,
    STEP_ID_USER,
)

from . import (
    BULSTAT_VALID,
    CAR_PLATE_INVALID,
    CAR_PLATE_VALID,
    EGN_VALID,
    MOCK_DATA_BUSINESS,
    MOCK_DATA_BUSINESS_FULL,
    MOCK_DATA_INDIVIDUAL,
    MOCK_DATA_INDIVIDUAL_FULL,
    MOCK_DATA_INDIVIDUAL_CAR_PLATE,
    MOCK_DATA_INDIVIDUAL_CAR_PLATE_FULL,
    MOCK_ENTRY_TITLE,
    PATCH_VALIDATE_CREDS_BUSINESS,
    PATCH_VALIDATE_CREDS_INDIVIDUAL,
)


@pytest.mark.asyncio
async def test_flow_init_individual(hass: HomeAssistant) -> None:
    """Test config flow."""

    config_flow_user = await hass.config_entries.flow.async_init(
        kat_constants.DOMAIN, context={"source": STEP_ID_USER}
    )
    assert config_flow_user["type"] is FlowResultType.MENU
    assert config_flow_user["step_id"] == STEP_ID_USER

    config_flow_individual = await hass.config_entries.flow.async_configure(
        config_flow_user["flow_id"], user_input={
            "next_step_id": STEP_ID_INDIVIDUAL
        }
    )
    await hass.async_block_till_done()

    assert config_flow_individual["type"] is FlowResultType.FORM
    assert config_flow_individual["step_id"] == STEP_ID_INDIVIDUAL


@pytest.mark.asyncio
async def test_flow_init_business(hass: HomeAssistant) -> None:
    """Test config flow."""

    config_flow_user = await hass.config_entries.flow.async_init(
        kat_constants.DOMAIN, context={"source": STEP_ID_USER}
    )
    assert config_flow_user["type"] is FlowResultType.MENU
    assert config_flow_user["step_id"] == STEP_ID_USER

    config_flow_business = await hass.config_entries.flow.async_configure(
        config_flow_user["flow_id"], user_input={
            "next_step_id": STEP_ID_BUSINESS
        }
    )
    await hass.async_block_till_done()

    assert config_flow_business["type"] is FlowResultType.FORM
    assert config_flow_business["step_id"] == STEP_ID_BUSINESS


@pytest.mark.asyncio
@patch(PATCH_VALIDATE_CREDS_INDIVIDUAL, AsyncMock(return_value=[]))
async def test_flow_individual(hass: HomeAssistant) -> None:
    """Test config flow."""

    config_flow_individual = await hass.config_entries.flow.async_init(
        kat_constants.DOMAIN, context={"source": STEP_ID_INDIVIDUAL}
    )

    config_result = await hass.config_entries.flow.async_configure(
        config_flow_individual["flow_id"],
        user_input=MOCK_DATA_INDIVIDUAL,
    )
    await hass.async_block_till_done()

    assert config_result["type"] is FlowResultType.CREATE_ENTRY
    assert config_result["title"] == MOCK_ENTRY_TITLE
    assert config_result["data"] == MOCK_DATA_INDIVIDUAL_FULL
    assert config_result["context"]["unique_id"] == EGN_VALID


@pytest.mark.asyncio
@patch(PATCH_VALIDATE_CREDS_INDIVIDUAL, AsyncMock(return_value=[]))
async def test_flow_individual_car_plate(hass: HomeAssistant) -> None:
    """Test config flow."""

    config_flow_individual = await hass.config_entries.flow.async_init(
        kat_constants.DOMAIN, context={"source": STEP_ID_INDIVIDUAL}
    )

    config_result = await hass.config_entries.flow.async_configure(
        config_flow_individual["flow_id"],
        user_input=MOCK_DATA_INDIVIDUAL_CAR_PLATE,
    )
    await hass.async_block_till_done()

    assert config_result["type"] is FlowResultType.CREATE_ENTRY
    assert config_result["title"] == MOCK_ENTRY_TITLE
    assert config_result["data"] == MOCK_DATA_INDIVIDUAL_CAR_PLATE_FULL
    assert config_result["context"]["unique_id"] == CAR_PLATE_VALID


@pytest.mark.asyncio
@patch(PATCH_VALIDATE_CREDS_BUSINESS, AsyncMock(return_value=[]))
async def test_flow_business(hass: HomeAssistant) -> None:
    """Test config flow."""

    config_flow_individual = await hass.config_entries.flow.async_init(
        kat_constants.DOMAIN, context={"source": STEP_ID_BUSINESS}
    )

    config_result = await hass.config_entries.flow.async_configure(
        config_flow_individual["flow_id"],
        user_input=MOCK_DATA_BUSINESS,
    )
    await hass.async_block_till_done()

    assert config_result["type"] is FlowResultType.CREATE_ENTRY
    assert config_result["title"] == MOCK_ENTRY_TITLE
    assert config_result["data"] == MOCK_DATA_BUSINESS_FULL
    assert config_result["context"]["unique_id"] == BULSTAT_VALID


@pytest.mark.asyncio
@patch(
    PATCH_VALIDATE_CREDS_INDIVIDUAL,
    AsyncMock(
        side_effect=KatError(
            KatErrorType.VALIDATION_ERROR,
            KatErrorSubtype.VALIDATION_EGN_INVALID,
            "error text",
        )
    ),
)
async def test_flow_error_egn_invalid_individual(hass: HomeAssistant) -> None:
    """Test config flow."""

    config_flow_individual = await hass.config_entries.flow.async_init(
        kat_constants.DOMAIN,
        context={"source": STEP_ID_INDIVIDUAL},
    )

    config_result = await hass.config_entries.flow.async_configure(
        config_flow_individual["flow_id"],
        user_input=MOCK_DATA_INDIVIDUAL,
    )
    await hass.async_block_till_done()

    assert config_result["type"] is FlowResultType.FORM
    assert config_result["errors"] == {"base": "invalid_config"}


@pytest.mark.asyncio
@patch(
    PATCH_VALIDATE_CREDS_BUSINESS,
    AsyncMock(
        side_effect=KatError(
            KatErrorType.VALIDATION_ERROR,
            KatErrorSubtype.VALIDATION_EGN_INVALID,
            "error text",
        )
    ),
)
async def test_flow_error_egn_invalid_business(hass: HomeAssistant) -> None:
    """Test config flow."""

    config_flow_individual = await hass.config_entries.flow.async_init(
        kat_constants.DOMAIN,
        context={"source": STEP_ID_BUSINESS},
    )

    config_result = await hass.config_entries.flow.async_configure(
        config_flow_individual["flow_id"],
        user_input=MOCK_DATA_BUSINESS,
    )
    await hass.async_block_till_done()

    assert config_result["type"] is FlowResultType.FORM
    assert config_result["errors"] == {"base": "invalid_config"}


@pytest.mark.asyncio
@patch(
    PATCH_VALIDATE_CREDS_INDIVIDUAL,
    AsyncMock(
        side_effect=KatError(
            KatErrorType.VALIDATION_ERROR,
            KatErrorSubtype.VALIDATION_USER_NOT_FOUND_ONLINE,
            "error text",
        )
    ),
)
async def test_flow_error_notfoundonline_individual(hass: HomeAssistant) -> None:
    """Test config flow."""

    config_flow_individual = await hass.config_entries.flow.async_init(
        kat_constants.DOMAIN,
        context={"source": STEP_ID_INDIVIDUAL},
    )

    config_result = await hass.config_entries.flow.async_configure(
        config_flow_individual["flow_id"],
        user_input=MOCK_DATA_INDIVIDUAL,
    )
    await hass.async_block_till_done()

    assert config_result["type"] is FlowResultType.FORM
    assert config_result["errors"] == {"base": "invalid_config"}


@pytest.mark.asyncio
@patch(
    PATCH_VALIDATE_CREDS_BUSINESS,
    AsyncMock(
        side_effect=KatError(
            KatErrorType.VALIDATION_ERROR,
            KatErrorSubtype.VALIDATION_USER_NOT_FOUND_ONLINE,
            "error text",
        )
    ),
)
async def test_flow_error_notfoundonline_business(hass: HomeAssistant) -> None:
    """Test config flow."""

    config_flow_individual = await hass.config_entries.flow.async_init(
        kat_constants.DOMAIN,
        context={"source": STEP_ID_BUSINESS},
    )

    config_result = await hass.config_entries.flow.async_configure(
        config_flow_individual["flow_id"],
        user_input=MOCK_DATA_BUSINESS,
    )
    await hass.async_block_till_done()

    assert config_result["type"] is FlowResultType.FORM
    assert config_result["errors"] == {"base": "invalid_config"}


@pytest.mark.asyncio
@patch(
    PATCH_VALIDATE_CREDS_INDIVIDUAL,
    AsyncMock(
        side_effect=KatError(
            KatErrorType.VALIDATION_ERROR,
            KatErrorSubtype.VALIDATION_DRIVING_LICENSE_INVALID,
            "error text",
        )
    ),
)
async def test_flow_error_invalid_document_individual(hass: HomeAssistant) -> None:
    """Test config flow."""

    config_flow_individual = await hass.config_entries.flow.async_init(
        kat_constants.DOMAIN,
        context={"source": STEP_ID_INDIVIDUAL},
    )

    config_result = await hass.config_entries.flow.async_configure(
        config_flow_individual["flow_id"],
        user_input=MOCK_DATA_INDIVIDUAL,
    )
    await hass.async_block_till_done()

    assert config_result["type"] is FlowResultType.FORM
    assert config_result["errors"] == {"base": "invalid_config"}


@pytest.mark.asyncio
@patch(
    PATCH_VALIDATE_CREDS_INDIVIDUAL,
    AsyncMock(
        side_effect=KatError(
            KatErrorType.VALIDATION_ERROR,
            KatErrorSubtype.VALIDATION_CAR_PLATE_NUMBER_INVALID,
            "error text",
        )
    ),
)
async def test_flow_error_invalid_car_plate_number_individual(hass: HomeAssistant) -> None:
    """Test config flow."""

    config_flow_individual = await hass.config_entries.flow.async_init(
        kat_constants.DOMAIN,
        context={"source": STEP_ID_INDIVIDUAL},
    )

    config_result = await hass.config_entries.flow.async_configure(
        config_flow_individual["flow_id"],
        user_input={
            **MOCK_DATA_INDIVIDUAL_CAR_PLATE,
            kat_constants.CONF_DOCUMENT_NUMBER: CAR_PLATE_INVALID,
        },
    )
    await hass.async_block_till_done()

    assert config_result["type"] is FlowResultType.FORM
    assert config_result["errors"] == {
        "base": "invalid_config_car_plate_number"}


@pytest.mark.asyncio
@patch(
    PATCH_VALIDATE_CREDS_BUSINESS,
    AsyncMock(
        side_effect=KatError(
            KatErrorType.VALIDATION_ERROR,
            KatErrorSubtype.VALIDATION_GOV_ID_NUMBER_INVALID,
            "error text",
        )
    ),
)
async def test_flow_error_invalid_document_business(hass: HomeAssistant) -> None:
    """Test config flow."""

    config_flow_individual = await hass.config_entries.flow.async_init(
        kat_constants.DOMAIN,
        context={"source": STEP_ID_BUSINESS},
    )

    config_result = await hass.config_entries.flow.async_configure(
        config_flow_individual["flow_id"],
        user_input=MOCK_DATA_BUSINESS,
    )
    await hass.async_block_till_done()

    assert config_result["type"] is FlowResultType.FORM
    assert config_result["errors"] == {"base": "invalid_config"}


@pytest.mark.asyncio
@patch(
    PATCH_VALIDATE_CREDS_INDIVIDUAL,
    AsyncMock(
        side_effect=KatError(
            KatErrorType.API_ERROR, KatErrorSubtype.API_TIMEOUT, "error text"
        )
    ),
)
async def test_flow_error_api_timeout_individual(hass: HomeAssistant) -> None:
    """Test config flow."""

    config_flow_individual = await hass.config_entries.flow.async_init(
        kat_constants.DOMAIN,
        context={"source": STEP_ID_INDIVIDUAL},
    )

    config_result = await hass.config_entries.flow.async_configure(
        config_flow_individual["flow_id"],
        user_input=MOCK_DATA_INDIVIDUAL,
    )
    await hass.async_block_till_done()

    assert config_result["type"] is FlowResultType.FORM
    assert config_result["errors"] == {"base": "cannot_connect"}


@pytest.mark.asyncio
@patch(
    PATCH_VALIDATE_CREDS_BUSINESS,
    AsyncMock(
        side_effect=KatError(
            KatErrorType.API_ERROR, KatErrorSubtype.API_TIMEOUT, "error text"
        )
    ),
)
async def test_flow_error_api_timeout_business(hass: HomeAssistant) -> None:
    """Test config flow."""

    config_flow_individual = await hass.config_entries.flow.async_init(
        kat_constants.DOMAIN,
        context={"source": STEP_ID_BUSINESS},
    )

    config_result = await hass.config_entries.flow.async_configure(
        config_flow_individual["flow_id"],
        user_input=MOCK_DATA_BUSINESS,
    )
    await hass.async_block_till_done()

    assert config_result["type"] is FlowResultType.FORM
    assert config_result["errors"] == {"base": "cannot_connect"}


@pytest.mark.asyncio
@patch(
    PATCH_VALIDATE_CREDS_INDIVIDUAL,
    AsyncMock(
        side_effect=KatError(
            KatErrorType.API_ERROR, KatErrorSubtype.API_ERROR_READING_DATA, "error text"
        )
    ),
)
async def test_flow_error_api_error_reading_data_individual(
    hass: HomeAssistant,
) -> None:
    """Test config flow."""

    config_flow_individual = await hass.config_entries.flow.async_init(
        kat_constants.DOMAIN,
        context={"source": STEP_ID_INDIVIDUAL},
    )

    config_result = await hass.config_entries.flow.async_configure(
        config_flow_individual["flow_id"],
        user_input=MOCK_DATA_INDIVIDUAL,
    )
    await hass.async_block_till_done()

    assert config_result["type"] is FlowResultType.FORM
    assert config_result["errors"] == {"base": "cannot_connect"}


@pytest.mark.asyncio
@patch(
    PATCH_VALIDATE_CREDS_BUSINESS,
    AsyncMock(
        side_effect=KatError(
            KatErrorType.API_ERROR, KatErrorSubtype.API_ERROR_READING_DATA, "error text"
        )
    ),
)
async def test_flow_error_api_error_reading_data_business(hass: HomeAssistant) -> None:
    """Test config flow."""

    config_flow_individual = await hass.config_entries.flow.async_init(
        kat_constants.DOMAIN,
        context={"source": STEP_ID_BUSINESS},
    )

    config_result = await hass.config_entries.flow.async_configure(
        config_flow_individual["flow_id"],
        user_input=MOCK_DATA_BUSINESS,
    )
    await hass.async_block_till_done()

    assert config_result["type"] is FlowResultType.FORM
    assert config_result["errors"] == {"base": "cannot_connect"}


@pytest.mark.asyncio
@patch(
    PATCH_VALIDATE_CREDS_INDIVIDUAL,
    AsyncMock(
        side_effect=KatError(
            KatErrorType.API_ERROR, KatErrorSubtype.API_INVALID_SCHEMA, "error text"
        )
    ),
)
async def test_flow_error_api_invalid_schema_individual(
    hass: HomeAssistant,
) -> None:
    """Test config flow."""

    config_flow_individual = await hass.config_entries.flow.async_init(
        kat_constants.DOMAIN,
        context={"source": STEP_ID_INDIVIDUAL},
    )

    config_result = await hass.config_entries.flow.async_configure(
        config_flow_individual["flow_id"],
        user_input=MOCK_DATA_INDIVIDUAL,
    )
    await hass.async_block_till_done()

    assert config_result["type"] is FlowResultType.FORM
    assert config_result["errors"] == {"base": "cannot_connect"}


@pytest.mark.asyncio
@patch(
    PATCH_VALIDATE_CREDS_BUSINESS,
    AsyncMock(
        side_effect=KatError(
            KatErrorType.API_ERROR, KatErrorSubtype.API_INVALID_SCHEMA, "error text"
        )
    ),
)
async def test_flow_error_api_invalid_schema_business(hass: HomeAssistant) -> None:
    """Test config flow."""

    config_flow_individual = await hass.config_entries.flow.async_init(
        kat_constants.DOMAIN,
        context={"source": STEP_ID_BUSINESS},
    )

    config_result = await hass.config_entries.flow.async_configure(
        config_flow_individual["flow_id"],
        user_input=MOCK_DATA_BUSINESS,
    )
    await hass.async_block_till_done()

    assert config_result["type"] is FlowResultType.FORM
    assert config_result["errors"] == {"base": "cannot_connect"}


@pytest.mark.asyncio
@patch(
    PATCH_VALIDATE_CREDS_INDIVIDUAL,
    AsyncMock(
        side_effect=KatError(
            KatErrorType.API_ERROR, KatErrorSubtype.API_TOO_MANY_REQUESTS, "error text"
        )
    ),
)
async def test_flow_error_api_too_many_requests_individual(
    hass: HomeAssistant,
) -> None:
    """Test config flow."""

    config_flow_individual = await hass.config_entries.flow.async_init(
        kat_constants.DOMAIN,
        context={"source": STEP_ID_INDIVIDUAL},
    )

    config_result = await hass.config_entries.flow.async_configure(
        config_flow_individual["flow_id"],
        user_input=MOCK_DATA_INDIVIDUAL,
    )
    await hass.async_block_till_done()

    assert config_result["type"] is FlowResultType.FORM
    assert config_result["errors"] == {"base": "cannot_connect"}


@pytest.mark.asyncio
@patch(
    PATCH_VALIDATE_CREDS_BUSINESS,
    AsyncMock(
        side_effect=KatError(
            KatErrorType.API_ERROR, KatErrorSubtype.API_TOO_MANY_REQUESTS, "error text"
        )
    ),
)
async def test_flow_error_api_too_many_requests_business(hass: HomeAssistant) -> None:
    """Test config flow."""

    config_flow_individual = await hass.config_entries.flow.async_init(
        kat_constants.DOMAIN,
        context={"source": STEP_ID_BUSINESS},
    )

    config_result = await hass.config_entries.flow.async_configure(
        config_flow_individual["flow_id"],
        user_input=MOCK_DATA_BUSINESS,
    )
    await hass.async_block_till_done()

    assert config_result["type"] is FlowResultType.FORM
    assert config_result["errors"] == {"base": "cannot_connect"}


@pytest.mark.asyncio
@patch(
    PATCH_VALIDATE_CREDS_INDIVIDUAL,
    AsyncMock(
        side_effect=KatError(
            KatErrorType.API_ERROR, KatErrorSubtype.API_UNKNOWN_ERROR, "error text"
        )
    ),
)
async def test_flow_error_api_unknown_error_individual(
    hass: HomeAssistant,
) -> None:
    """Test config flow."""

    config_flow_individual = await hass.config_entries.flow.async_init(
        kat_constants.DOMAIN,
        context={"source": STEP_ID_INDIVIDUAL},
    )

    config_result = await hass.config_entries.flow.async_configure(
        config_flow_individual["flow_id"],
        user_input=MOCK_DATA_INDIVIDUAL,
    )
    await hass.async_block_till_done()

    assert config_result["type"] is FlowResultType.FORM
    assert config_result["errors"] == {"base": "cannot_connect"}


@pytest.mark.asyncio
@patch(
    PATCH_VALIDATE_CREDS_BUSINESS,
    AsyncMock(
        side_effect=KatError(
            KatErrorType.API_ERROR, KatErrorSubtype.API_UNKNOWN_ERROR, "error text"
        )
    ),
)
async def test_flow_error_api_unknown_error_business(hass: HomeAssistant) -> None:
    """Test config flow."""

    config_flow_individual = await hass.config_entries.flow.async_init(
        kat_constants.DOMAIN,
        context={"source": STEP_ID_BUSINESS},
    )

    config_result = await hass.config_entries.flow.async_configure(
        config_flow_individual["flow_id"],
        user_input=MOCK_DATA_BUSINESS,
    )
    await hass.async_block_till_done()

    assert config_result["type"] is FlowResultType.FORM
    assert config_result["errors"] == {"base": "cannot_connect"}


@pytest.mark.asyncio
@patch(PATCH_VALIDATE_CREDS_INDIVIDUAL, AsyncMock(return_value=[]))
async def test_flow_error_already_configured_individual(
    hass: HomeAssistant,
) -> None:
    """Test config flow."""

    entry = MockConfigEntry(
        domain=kat_constants.DOMAIN,
        data=MOCK_DATA_INDIVIDUAL_FULL,
        unique_id=EGN_VALID,
    )
    entry.add_to_hass(hass)

    config_flow_individual = await hass.config_entries.flow.async_init(
        kat_constants.DOMAIN,
        context={"source": STEP_ID_INDIVIDUAL},
    )

    config_result = await hass.config_entries.flow.async_configure(
        config_flow_individual["flow_id"],
        user_input=MOCK_DATA_INDIVIDUAL,
    )
    await hass.async_block_till_done()

    assert config_result["type"] is FlowResultType.ABORT
    assert config_result["reason"] == "already_configured"


@pytest.mark.asyncio
@patch(PATCH_VALIDATE_CREDS_BUSINESS, AsyncMock(return_value=True))
async def test_flow_error_already_configured_business(
    hass: HomeAssistant,
) -> None:
    """Test config flow."""

    entry = MockConfigEntry(
        domain=kat_constants.DOMAIN,
        data=MOCK_DATA_BUSINESS_FULL,
        unique_id=BULSTAT_VALID,
    )
    entry.add_to_hass(hass)

    config_flow_individual = await hass.config_entries.flow.async_init(
        kat_constants.DOMAIN,
        context={"source": STEP_ID_BUSINESS},
    )

    config_result = await hass.config_entries.flow.async_configure(
        config_flow_individual["flow_id"],
        user_input=MOCK_DATA_BUSINESS,
    )
    await hass.async_block_till_done()

    assert config_result["type"] is FlowResultType.ABORT
    assert config_result["reason"] == "already_configured"
