"""Custom Eeero Integration"""
import logging

DOMAIN = "my_heero"

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass, config):
  _LOGGER.info("Setting up My Heero integration...")
  return True
