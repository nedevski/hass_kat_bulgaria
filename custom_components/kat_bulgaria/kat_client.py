"""KAT Bulgaria Client Wrapper."""

import socket

import aiohttp
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from kat_bulgaria.data_models import KatObligation
from kat_bulgaria.kat_api_client import KatApiClient

from .const import PersonType


class KatClient:
    """KAT Client Manager."""

    _aiohttp_session: aiohttp.ClientSession | None

    api: KatApiClient
    hass: HomeAssistant

    person_type: str
    person_egn: str
    person_identifier: str
    person_identifier_type: str | None
    bulstat: str | None

    def __init__(
        self,
        hass: HomeAssistant,
        person_type: str,
        egn: str,
        identifier_str: str,
        document_type: str | None,
        bulstat: str | None,
        aiohttp_session: aiohttp.ClientSession | None = None,
    ) -> None:
        """Initialize client."""
        super().__init__()

        self._aiohttp_session = aiohttp_session
        self.hass = hass
        self.api = KatApiClient()

        self.person_type = person_type
        self.person_egn = egn
        self.person_identifier = identifier_str
        self.person_identifier_type = None
        self.bulstat = None

        if self.person_type == PersonType.INDIVIDUAL:
            if document_type is None:
                raise ValueError("Document type is required for individual type")

            self.person_identifier_type = document_type

        if self.person_type == PersonType.BUSINESS:
            if bulstat is None:
                raise ValueError("Bulstat is required for business type")

            self.bulstat = bulstat

    async def _get_aiohttp_session(self) -> aiohttp.ClientSession:
        """Return an aiohttp client session managed by Home Assistant."""

        if self._aiohttp_session is None:
            self._aiohttp_session = async_get_clientsession(
                self.hass,
                family=socket.AF_INET,
            )

        return self._aiohttp_session

    async def validate_credentials(self) -> bool:
        """Validate EGN/License Number."""

        obligations = await self.get_obligations()

        if not obligations:
            return False

        return True

    async def get_obligations(self) -> list[KatObligation]:
        """Get obligations."""

        client = await self._get_aiohttp_session()

        if self.person_type == PersonType.BUSINESS:
            return await self.api.get_obligations_business(
                self.person_egn, self.person_identifier, self.bulstat, client
            )

        return await self.api.get_obligations_individual(
            self.person_egn, self.person_identifier_type, self.person_identifier, client
        )
