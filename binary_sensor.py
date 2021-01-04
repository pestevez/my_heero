"""Platform for sensor integration."""
import eero
import logging

from .const import (
  CONF_NETWORK_ID,
  DATA_COORDINATOR_KEY,
  DOMAIN,
  MANUFACTURER,
)

from homeassistant.components.binary_sensor import (
  BinarySensorEntity,
  DEVICE_CLASS_CONNECTIVITY,
)
from homeassistant.helpers.update_coordinator import CoordinatorEntity

FIELD_SERIAL = "serial"
FIELD_STATUS = "status"
FIELD_URL = "url"

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, config_entry, async_add_devices):
  """Add a binary sensor for each passed config_entry in HA."""
  coordinator = hass.data[DOMAIN][DATA_COORDINATOR_KEY]

  eero_infos = coordinator.data.items()

  new_devices = []
  for eero_info in eero_infos:
    new_devices.append(EeroConnectivityBinarySensor(eero_info, coordinator))

  # If we have any new devices, add them
  if new_devices:
    async_add_devices(new_devices)

class EeroConnectivityBinarySensor(CoordinatorEntity, BinarySensorEntity):
  """Representation of a Sensor."""

  device_class = DEVICE_CLASS_CONNECTIVITY

  def __init__(self, eero_info, coordinator):
    """Initialize the sensor."""
    super().__init__(coordinator)
    self._eero_info = eero_info
    self._eero_id = eero.id_from_url(eero_info[FIELD_URL])

  # Supports connecting the entity with the correct device
  @property
  def device_info(self):
    return {
      "identifiers": {(DOMAIN, self._eero_info[FIELD_SERIAL])},
      "name": self._eero_info["location"] + " " + MANUFACTURER,
      "manufacturer": MANUFACTURER,
      "sw_version": self._eero_info["os"],
      "model": self._eero_info["model_number"],
    }

  @property
  def is_on(self):
    return self._eero_info[FIELD_STATUS] == "green"

  # This property is important to let HA know if this entity is online or not.
  # If an entity is offline (return False), the UI will refelect this.
  @property
  def available(self):
    return self.coordinator.last_update_success and self._eero_info["heartbeat_ok"]

  @property
  def unique_id(self):
    """Return Unique ID string."""
    return f'{MANUFACTURER}_{self._eero_id}_connectivity'

  # This is the name for this *entity*, the "name" attribute from "device_info"
  # is used as the device name for device screens in the UI. This name is used on
  # entity screens, and used to build the Entity ID that's used is automations etc.
  @property
  def name(self):
    """Return the name of the entity."""
    return self._eero_info["location"] + f' {MANUFACTURER} Connectivity'
