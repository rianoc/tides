# Tides

Copy the `tides` folder so that it lives at `config/custom_components/tides`

In `configuration.yaml` add:

```yaml
sensor:
  - platform: tides
```

Currently to handle location it is entered on line 38 of `sensor.py`. It must be a valid location taken from the URL on <https://www.tidetimes.org.uk/>.

ToDo:

1. Configure location through `configuration.yaml` or UI
2. Register multiple sensors rather than using attributes
3. Only poll site for data once per day
