# justbartek.ca

My little place on the internet

## Setup

```sh
./bootstrap.sh            # creates .venv (Python 3.13) and installs requirements
source .venv/bin/activate
```

## Running

```sh
python site.py            # dev server on http://localhost:4000
python site.py build      # static build into build/
```

The bike parking map loads `static/hfxbikeparking.geojson` and
`static/counter_channels.geojson`. These aren't committed; CI copies them in from
[bartek/hfxbikeparking](https://github.com/bartek/hfxbikeparking) at build time.
Copy them in yourself to see data locally.
