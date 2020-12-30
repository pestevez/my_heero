from homeassistant import config_entries

import eero
import logging
import voluptuous as vol

from .const import (
  CONF_NETWORK_ID,
  CONF_USER_TOKEN,
  DOMAIN,
)

from .cookie import (
  CookieStore,
)

_LOGGER = logging.getLogger(__name__)

class MyHeeroConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
  """My Heero config flow."""

  VERSION = 1

  def __init__(self):
    """Initialize the config flow."""
    self.eero = None

  async def async_step_user(self, info):
    if info is not None:
      #  TODO: Validate  user input
      user_token = info[CONF_USER_TOKEN]

      # Get user input value to populate cookie
      cookie = CookieStore(user_token)
      # Get Eero client using cookie
      self.eero = eero.Eero(cookie)
      account = self.eero.account()

      # TODO: Validate fields

      # Use the email address as the title of the configuration
      title = account["email"]["value"]

      # Get all the networks from the account response
      networks = account["networks"]
      if (networks is not None and networks["count"] > 0):
        # We'll only process the first network
        first_network = networks["data"][0]
        first_network_id = self.eero.id_from_url(first_network["url"])

        return self.async_create_entry(
          # The value that will be showin in the UI
          title=title,
          # The values that we'll store
          data={
            CONF_USER_TOKEN: info[CONF_USER_TOKEN],
            CONF_NETWORK_ID: first_network_id,
          },
        )
      else:
        return self.asyc_abort(reason="No networks found")

    data_schema = {
      vol.Required(CONF_USER_TOKEN): str,
    }

    return self.async_show_form(
      step_id="user", data_schema=vol.Schema(data_schema)
    )
