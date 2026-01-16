from __future__ import annotations

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback

from .const import DOMAIN


class AutodartsConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(
                title="Autodarts",
                data=user_input,
            )

        schema = vol.Schema(
            {
                vol.Required("host"): str,
                vol.Required("port", default=3180): int,
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
        )

