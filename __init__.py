"""Custom Eeero Integration"""
import logging

from .const import (
  DOMAIN,
)

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass, config):
  hass.data.setdefault(DOMAIN, {})
  return True

#async def async_setup_entry(hass, self):
