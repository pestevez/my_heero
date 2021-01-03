"""Custom Eeero Integration"""
import asyncio
import eero
import logging

from .const import (
  CONF_USER_TOKEN,
  DOMAIN,
)

from .cookie import (
  CookieStore,
)

# List of platforms to support. There should be a matching .py file for each,
# eg <sensor.py>
PLATFORMS = ["binary_sensor"]

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass, config):
  hass.data.setdefault(DOMAIN, {})

  return True

async def async_setup_entry(hass, entry):
  user_token = entry.data[CONF_USER_TOKEN]

  # Get user input value to populate cookie
  cookie = CookieStore(user_token)
  # Get Eero client using cookie
  _eero = eero.Eero(cookie)

  hass.data[DOMAIN][entry.entry_id] = _eero

  # This creates each HA object for each platform your device requires.
  # It's done by calling the `async_setup_entry` function in each platform module.
  for component in PLATFORMS:
    hass.async_create_task(
      hass.config_entries.async_forward_entry_setup(entry, component)
    )

  return True

async def async_unload_entry(hass, entry):
  """Unload a config entry."""
  # This is called when an entry/configured device is to be removed. The class
  # needs to unload itself, and remove callbacks. See the classes for further
  # details
  unload_ok = all(
    await asyncio.gather(
      *[
        hass.config_entries.async_forward_entry_unload(entry, component)
        for component in PLATFORMS
      ]
    )
  )

  if unload_ok:
    hass.data[DOMAIN].pop(entry.entry_id)

  return unload_ok
