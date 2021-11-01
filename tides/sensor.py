"""Support for the tide times RSS feeds"""
from datetime import timedelta
from datetime import datetime
import logging
import time

import requests
from bs4 import BeautifulSoup
import voluptuous as vol

from homeassistant.components.sensor import PLATFORM_SCHEMA, SensorEntity
from homeassistant.const import (
    ATTR_ATTRIBUTION,
)
import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)

ATTRIBUTION = "Data provided by tide times"

DEFAULT_NAME = "Tides"

SCAN_INTERVAL = timedelta(seconds=3600)

#PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
#    {
#        vol.Required(CONF_LOCATION): cv.string,
#        vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
#    }
#)


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the Tides sensor."""
#   name = config.get(CONF_NAME)
    name = "Tides"
#   loc = config.get(CONF_LOCATION)
    loc = 'dublin-bar-tide-times'

    tides = TidesSensor(name, loc)
    tides.update()
    add_entities([tides])


class TidesSensor(SensorEntity):
    """Representation of a Tides sensor."""

    def __init__(self, name, loc):
        """Initialize the sensor."""
        self._name = name
        self._loc = loc
        self.data = None

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def extra_state_attributes(self):
        """Return the state attributes of this device."""
        attr = {ATTR_ATTRIBUTION: ATTRIBUTION}

        if "High Tide"== self.data[0][0]:
            attr["high_tide_time"] = self.data[0][1]
            attr["high_tide_height"] = self.data[0][2]
            attr["low_tide_time"] = self.data[1][1]
            attr["low_tide_height"] = self.data[1][2]
            attr["high_tide_2_time"] = self.data[2][1]
            attr["high_tide_2_height"] = self.data[2][2]
            if 4 == len(self.data):
                attr["low_tide_2_time"] = self.data[3][1]
                attr["low_tide_2_height"] = self.data[3][2]
            else:
                attr["low_tide_2_time"] = ""
                attr["low_tide_2_height"] = ""
        elif "Low Tide"== self.data[0][0]:
            attr["low_tide_time"] = self.data[0][1]
            attr["low_tide_height"] = self.data[0][2]
            attr["high_tide_time"] = self.data[1][1]
            attr["high_tide_height"] = self.data[1][2]
            attr["low_tide_2_time"] = self.data[2][1]
            attr["low_tide_2_height"] = self.data[2][2]
            if 4 == len(self.data):
                attr["high_tide_2_time"] = self.data[3][1]
                attr["high_tide_2_height"] = self.data[3][2]
            else:
                attr["high_tide_2_time"] = ""
                attr["high_tide_2_height"] = ""
        return attr

    @property
    def native_value(self):
        """Return the state of the device."""
        times=[datetime.strptime(x[1],'%H:%M').time()for x in self.data]
        now=datetime.now().time()
        nextTide=-1
        for k, t in enumerate(times):
            if t > now:
                nextTide= k
                break
        if nextTide==-1:
            return None
        return self.data[nextTide][0] + " at " + self.data[nextTide][1] + " (" + self.data[nextTide][2] +"m)"

    def update(self):
        """Get the latest data from Tides API."""
        start = int(time.time())
        resource = "https://www.tidetimes.org.uk/" + self._loc + ".rss"

        try:
            self.data = requests.get(resource, timeout=10).text
            self.data = BeautifulSoup(self.data, 'html.parser')
            description = (self.data.findAll("description"))[1].getText()
            tides = BeautifulSoup(description, 'html.parser')
            tides = (str(tides).split('<br/>'))[2:-1]
            output_rows = []
            for table_row in tides:
                s = table_row.split(' - ')
                s1 = s[1].split(' (')
                output_rows.append([s1[0],s[0],s1[1][:-2]])
            self.data = output_rows
            _LOGGER.debug("Tides recovered: %s", len(self.data))
            _LOGGER.debug("Tide data queried with start time set to: %s", start)
        except ValueError as err:
            _LOGGER.error("Error retrieving data from Tides: %s", err.args)
            self.data = None
