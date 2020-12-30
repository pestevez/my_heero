"""Custom Eeero Integration"""
import logging

from .const import (
  DOMAIN,
)

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass, config):
  return True
