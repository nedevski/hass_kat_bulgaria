"""Config flow for KAT Bulgaria integration."""

from __future__ import annotations

import logging
from typing import Any

from kat_bulgaria.data_models import PersonalIdentificationType
from kat_bulgaria.errors import KatError, KatErrorSubtype, KatErrorType
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.config_entries import ConfigEntry, ConfigFlow, ConfigFlowResult
from homeassistant.helpers.selector import SelectSelector, SelectSelectorConfig

from .const import (
    CONF_BULSTAT,
    CONF_DOCUMENT_NUMBER,
    CONF_DOCUMENT_TYPE,
    CONF_PERSON_EGN,
    CONF_PERSON_NAME,
    CONF_PERSON_TYPE,
    DOMAIN,
    PersonType,
)
from .kat_client import KatClient

_LOGGER = logging.getLogger(__name__)

SCHEMA_INDIVIDUAL = vol.Schema(
    {
        vol.Required(CONF_PERSON_NAME): str,
        vol.Required(CONF_PERSON_EGN): str,
        vol.Required(
            CONF_DOCUMENT_TYPE, default=PersonalIdentificationType.NATIONAL_ID
        ): SelectSelector(
            SelectSelectorConfig(
                options=[
                    PersonalIdentificationType.NATIONAL_ID,
                    PersonalIdentificationType.DRIVING_LICENSE,
                    PersonalIdentificationType.CAR_PLATE_NUM,
                ],
                translation_key=CONF_DOCUMENT_TYPE,
            )
        ),
        vol.Required(CONF_DOCUMENT_NUMBER): str,
    }
)

SCHEMA_BUSINESS = vol.Schema(
    {
        vol.Required(CONF_PERSON_NAME): str,
        vol.Required(CONF_PERSON_EGN): str,
        vol.Required(CONF_DOCUMENT_NUMBER): str,
        vol.Required(CONF_BULSTAT): str,
    }
)

STEP_ID_USER = config_entries.SOURCE_USER
STEP_ID_INDIVIDUAL = PersonType.INDIVIDUAL
STEP_ID_BUSINESS = PersonType.BUSINESS
STEP_ID_RECONFIGURE = config_entries.SOURCE_RECONFIGURE


class ConfigFlowHandler(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for kat_bulgaria."""

    VERSION = 2

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """User config step to choose if setting up for an individual or a business."""

        return self.async_show_menu(
            step_id="user",
            menu_options=[STEP_ID_INDIVIDUAL, STEP_ID_BUSINESS],
        )

    async def async_step_individual(
        self, user_input: dict[str, Any]
    ) -> ConfigFlowResult:
        """Handle the individual setup step."""

        if user_input is None:
            return self.async_show_form(
                step_id=STEP_ID_INDIVIDUAL, data_schema=SCHEMA_INDIVIDUAL
            )

        # Init user input values & init KatClient
        user_name = user_input[CONF_PERSON_NAME]
        user_egn = user_input[CONF_PERSON_EGN]
        user_identifier_type = user_input[CONF_DOCUMENT_TYPE]
        user_identifier = user_input[CONF_DOCUMENT_NUMBER]

        user_input[CONF_PERSON_TYPE] = PersonType.INDIVIDUAL

        kat_client = KatClient(
            self.hass,
            PersonType.INDIVIDUAL,
            user_egn,
            user_identifier,
            user_identifier_type,
            None,
        )

        errors = await self._validate_user_credentials(kat_client)

        if errors:
            return self.async_show_form(
                step_id=STEP_ID_INDIVIDUAL,
                data_schema=SCHEMA_INDIVIDUAL,
                errors=errors,
            )

        unique_id = user_egn
        if user_identifier_type == PersonalIdentificationType.CAR_PLATE_NUM:
            unique_id = user_identifier

        # If this entity is already configured, abort
        await self.async_set_unique_id(unique_id)
        self._abort_if_unique_id_configured()

        return self.async_create_entry(title=f"KAT - {user_name}", data=user_input)

    async def async_step_business(self, user_input: dict[str, Any]) -> ConfigFlowResult:
        """Handle the business setup step."""

        if user_input is None:
            return self.async_show_form(
                step_id=STEP_ID_BUSINESS, data_schema=SCHEMA_BUSINESS
            )

        # Init user input values & init KatClient
        user_name = user_input[CONF_PERSON_NAME]
        user_egn = user_input[CONF_PERSON_EGN]
        user_gov_id_number = user_input[CONF_DOCUMENT_NUMBER]
        user_bulstat = user_input[CONF_BULSTAT]

        user_input[CONF_PERSON_TYPE] = PersonType.BUSINESS

        kat_client = KatClient(
            self.hass,
            PersonType.BUSINESS,
            user_egn,
            user_gov_id_number,
            None,
            user_bulstat,
        )

        errors = await self._validate_user_credentials(kat_client)

        if errors:
            return self.async_show_form(
                step_id=STEP_ID_BUSINESS, data_schema=SCHEMA_BUSINESS, errors=errors
            )

        # If this person (EGN) is already configured, abort
        await self.async_set_unique_id(user_bulstat)
        self._abort_if_unique_id_configured()

        return self.async_create_entry(title=f"KAT - {user_name}", data=user_input)

    async def async_step_reconfigure(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle a reconfiguration flow initialized by the user."""

        reconfigure_entry = self._get_reconfigure_entry()

        person_type = reconfigure_entry.data[CONF_PERSON_TYPE]

        if person_type == PersonType.INDIVIDUAL:
            return await self._async_step_reconfigure_individual(
                reconfigure_entry, user_input
            )

        if person_type == PersonType.BUSINESS:
            return await self._async_step_reconfigure_business(
                reconfigure_entry, user_input
            )

        return self.async_show_form(
            step_id=STEP_ID_RECONFIGURE,
            data_schema=None,
            errors={"base": "invalid_type"},
        )

    async def _async_step_reconfigure_individual(
        self,
        reconfigure_entry: ConfigEntry[Any],
        user_input: dict[str, Any] | None = None,
    ) -> ConfigFlowResult:
        """Reconfigure the individual step."""

        reconfigure_data_schema = vol.Schema(
            {
                vol.Required(
                    CONF_DOCUMENT_TYPE,
                    default=reconfigure_entry.data.get(
                        CONF_DOCUMENT_TYPE, PersonalIdentificationType.NATIONAL_ID
                    ),
                ): SelectSelector(
                    SelectSelectorConfig(
                        options=[
                            PersonalIdentificationType.NATIONAL_ID,
                            PersonalIdentificationType.DRIVING_LICENSE,
                            PersonalIdentificationType.CAR_PLATE_NUM,
                        ],
                        translation_key=CONF_DOCUMENT_TYPE,
                    )
                ),
                vol.Required(
                    CONF_DOCUMENT_NUMBER,
                    default=reconfigure_entry.data.get(
                        CONF_DOCUMENT_NUMBER, ""),
                ): str,
            }
        )

        if not user_input:
            return self.async_show_form(
                step_id=STEP_ID_RECONFIGURE,
                data_schema=reconfigure_data_schema,
            )

        existing_person_egn = reconfigure_entry.data[CONF_PERSON_EGN]
        new_document_type = user_input[CONF_DOCUMENT_TYPE]
        new_document_number = user_input[CONF_DOCUMENT_NUMBER]

        errors = await self._validate_user_credentials(
            KatClient(
                self.hass,
                PersonType.INDIVIDUAL,
                existing_person_egn,
                new_document_number,
                new_document_type,
                None,
            )
        )

        if errors:
            return self.async_show_form(
                step_id=STEP_ID_RECONFIGURE,
                data_schema=reconfigure_data_schema,
                errors=errors,
            )

        return self.async_update_reload_and_abort(
            reconfigure_entry, data_updates={**user_input}
        )

    async def _async_step_reconfigure_business(
        self,
        reconfigure_entry: ConfigEntry[Any],
        user_input: dict[str, Any] | None = None,
    ) -> ConfigFlowResult:
        """Reconfigure the business step."""

        reconfigure_data_schema = vol.Schema(
            {
                vol.Required(
                    CONF_DOCUMENT_NUMBER,
                    default=reconfigure_entry.data.get(
                        CONF_DOCUMENT_NUMBER, ""),
                ): str,
            }
        )

        if not user_input:
            return self.async_show_form(
                step_id=STEP_ID_RECONFIGURE,
                data_schema=reconfigure_data_schema,
            )

        existing_person_egn = reconfigure_entry.data[CONF_PERSON_EGN]
        existing_bulstat = reconfigure_entry.data[CONF_BULSTAT]

        new_document_number = user_input[CONF_DOCUMENT_NUMBER]

        errors = await self._validate_user_credentials(
            KatClient(
                self.hass,
                PersonType.BUSINESS,
                existing_person_egn,
                new_document_number,
                None,
                existing_bulstat,
            )
        )

        if errors:
            return self.async_show_form(
                step_id=STEP_ID_RECONFIGURE,
                data_schema=reconfigure_data_schema,
                errors=errors,
            )

        return self.async_update_reload_and_abort(
            reconfigure_entry, data_updates={**user_input}
        )

    async def _validate_user_credentials(self, kat_client: KatClient) -> dict[str, str]:
        """Validate user credentials."""

        errors = {}

        # Verify user input
        try:
            await kat_client.validate_credentials()
        except KatError as err:
            if (
                err.error_type == KatErrorType.VALIDATION_ERROR
                and err.error_subtype
                == KatErrorSubtype.VALIDATION_CAR_PLATE_NUMBER_INVALID
            ):
                _LOGGER.warning(
                    "Invalid credentials, unable to setup: %s - %s",
                    err.error_type,
                    err.error_subtype,
                )
                errors["base"] = "invalid_config_car_plate_number"

            elif err.error_type == KatErrorType.VALIDATION_ERROR:
                _LOGGER.warning(
                    "Invalid credentials, unable to setup: %s - %s",
                    err.error_type,
                    err.error_subtype,
                )
                errors["base"] = "invalid_config"

            elif err.error_type == KatErrorType.API_ERROR:
                _LOGGER.warning(
                    "KAT API down, unable to setup: %s - %s",
                    err.error_type,
                    err.error_subtype,
                )
                errors["base"] = "cannot_connect"

        return errors
