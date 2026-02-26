"""Base class for KAТ Bulgaria entities."""

from kat_bulgaria.data_models import PersonalIdentificationType

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, PersonType
from .coordinator import KatBulgariaUpdateCoordinator


class KatBulgariaEntity(CoordinatorEntity[KatBulgariaUpdateCoordinator]):
    """Defines a base AirGradient entity."""

    _attr_has_entity_name = True

    def __init__(self, coordinator: KatBulgariaUpdateCoordinator) -> None:
        """Initialize airgradient entity."""

        super().__init__(coordinator)

        unique_id = coordinator.client.person_egn

        if (
            coordinator.client.person_type == PersonType.INDIVIDUAL
            and coordinator.client.person_identifier_type
            == PersonalIdentificationType.CAR_PLATE_NUM
        ):
            unique_id = coordinator.client.person_identifier

        if (
            coordinator.client.person_type == PersonType.BUSINESS
            and coordinator.client.bulstat
        ):
            unique_id = coordinator.client.bulstat

        self._attr_unique_id: str = unique_id
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, unique_id)},
            manufacturer="KAT Bulgaria",
            serial_number=unique_id,
        )
