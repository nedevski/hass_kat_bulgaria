"""Tests for the KatClient aiohttp integration."""

import aiohttp
import socket
from unittest.mock import AsyncMock, Mock, patch

import pytest

from custom_components.kat_bulgaria.const import PersonType
from custom_components.kat_bulgaria.kat_client import KatClient


@pytest.mark.asyncio
async def test_get_obligations_uses_injected_aiohttp_session(hass) -> None:
    """Assert KatClient forwards a provided aiohttp session to the API."""
    fake_session = Mock(spec=aiohttp.ClientSession)

    client = KatClient(
        hass,
        PersonType.INDIVIDUAL,
        "1234567890",
        "A1234567",
        "driving_license",
        None,
        aiohttp_session=fake_session,
    )

    async_mock = AsyncMock(return_value=[])
    with patch.object(client.api, "get_obligations_individual", new=async_mock):
        await client.get_obligations()

    async_mock.assert_awaited_once_with(
        "1234567890",
        "driving_license",
        "A1234567",
        fake_session,
    )


@pytest.mark.asyncio
async def test_get_obligations_uses_home_assistant_session(hass) -> None:
    """Assert KatClient obtains the session from Home Assistant pipeline."""
    fake_session = Mock(spec=aiohttp.ClientSession)

    with patch(
        "custom_components.kat_bulgaria.kat_client.async_get_clientsession",
        return_value=fake_session,
    ) as get_clientsession:
        async_mock = AsyncMock(return_value=[])
        with patch(
            "custom_components.kat_bulgaria.kat_client.KatApiClient.get_obligations_individual",
            new=async_mock,
        ):
            client = KatClient(
                hass,
                PersonType.INDIVIDUAL,
                "1234567890",
                "A1234567",
                "driving_license",
                None,
            )
            await client.get_obligations()

    get_clientsession.assert_called_once_with(hass, family=socket.AF_INET)
    async_mock.assert_awaited_once_with(
        "1234567890",
        "driving_license",
        "A1234567",
        fake_session,
    )
