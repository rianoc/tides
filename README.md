# Tides

## Install and config

Dependencies needed:

```bash
pip install bs4
```

```bash
cd /share
git clone https://github.com/rianoc/tides.git
cd tides
cp config.py.example config.py
```

Edit `config.py` to replace `URL` which you can find on [tidetimes.org.uk](https://www.tidetimes.org.uk)
You can also change `LOCATION` and not use `/share` as I have.

```bash
crontab -e
```

```bash
0 6 * * * /usr/bin/python3 /share/tides/getTides.py
```

Add sensors to `configuration.yaml`

```yaml
sensor 9:
  platform: command_line
  name: High Tide 1 Time
  command: "/usr/bin/python3 /share/tides/tides.py | grep 'H1T' | sed 's/^.*,//'"
  
sensor 10:
  platform: command_line
  name: High Tide 1 Height
  command: "/usr/bin/python3 /share/tides/tides.py | grep 'H1H' | sed 's/^.*,//'"
  unit_of_measurement: "m"

sensor 11:
  platform: command_line
  name: Low Tide 1 Time
  command: "/usr/bin/python3 /share/tides/tides.py | grep 'L1T' | sed 's/^.*,//'"

sensor 12:
  platform: command_line
  name: Low Tide 1 Height
  command: "/usr/bin/python3 /share/tides/tides.py | grep 'L1H' | sed 's/^.*,//'"
  unit_of_measurement: "m"
  
sensor 13:
  platform: command_line
  name: High Tide 2 Time
  command: "/usr/bin/python3 /share/tides/tides.py | grep 'H2T' | sed 's/^.*,//'"
  
sensor 14:
  platform: command_line
  name: High Tide 2 Height
  command: "/usr/bin/python3 /share/tides/tides.py | grep 'H2H' | sed 's/^.*,//'"
  unit_of_measurement: "m"

sensor 15:
  platform: command_line
  name: Low Tide 2 Time
  command: "/usr/bin/python3 /share/tides/tides.py | grep 'L2T' | sed 's/^.*,//'"

sensor 16:
  platform: command_line
  name: Low Tide 2 Height
  command: "/usr/bin/python3 /share/tides/tides.py | grep 'L2H' | sed 's/^.*,//'"
  unit_of_measurement: "m"
```

To customise icons I also added:

```yaml
homeassistant:
  customize: !include customize.yaml
```

Then in `customize.yaml`:

```yaml
sensor.high_tide_1_height:
  icon: mdi:elevation-rise
sensor.high_tide_1_time:
  icon: mdi:flag-variant
sensor.low_tide_1_height:
  icon: mdi:elevation-decline
sensor.low_tide_1_time:
  icon: mdi:flag-outline
sensor.high_tide_2_height:
  icon: mdi:elevation-rise
sensor.high_tide_2_time:
  icon: mdi:flag-variant
sensor.low_tide_2_height:
  icon: mdi:elevation-decline
sensor.low_tide_2_time:
  icon: mdi:flag-outline
```
