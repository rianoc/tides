# Tides

## Install and config

Dependencies needed:

```bash
pip install bs4 pandas
```

I am using the hass.io VM image and also needed
```bash
apk add  build-base gcc
```

```
cd /share
git clone https://github.com/rianoc/tides.git
cd tides
cp config.py.example config.py
```

Edit `config.py` to replace `URL` which you can find on [tidetimes.org.uk](https://www.tidetimes.org.uk)
You can also change `LOCATION` and not use `/share` as I have.


