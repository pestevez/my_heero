"""Platform for sensor integration."""
import eero
import logging

from .const import (
  CONF_NETWORK_ID,
  DOMAIN,
  MANUFACTURER,
)

from homeassistant.components.binary_sensor import (
  BinarySensorEntity,
  DEVICE_CLASS_CONNECTIVITY,
)

FIELD_SERIAL = "serial"
FIELD_STATUS = "status"
FIELD_URL = "url"

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, config_entry, async_add_devices):
  """Add sensors for passed config_entry in HA."""
  _eero = hass.data[DOMAIN][config_entry.entry_id]
  network_id = config_entry.data[CONF_NETWORK_ID]

  eero_infos = _eero.eeros(network_id)

  new_devices = []
  for eero_info in eero_infos:
    new_devices.append(EeroConnectivityBinarySensor(_eero, eero_info))

  # If we have any new devices, add them
  if new_devices:
    async_add_devices(new_devices)

class EeroConnectivityBinarySensor(BinarySensorEntity):
  """Representation of a Sensor."""

  device_class = DEVICE_CLASS_CONNECTIVITY

  def __init__(self, _eero, eero_info):
    """Initialize the sensor."""
    self._eero_info = eero_info
    self._status = eero_info[FIELD_STATUS]
    self._eero_id = _eero.id_from_url(eero_info[FIELD_URL])

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
    return self._status == "green"

  # This property is important to let HA know if this entity is online or not.
  # If an entity is offline (return False), the UI will refelect this.
  @property
  def available(self):
    return self._eero_info is not None

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

  #def update(self):
    # Load state
