
from jinja2 import Environment, FileSystemLoader

from stations import STATIONS

import euskalmet
import windguru


all_stations = []

for station in STATIONS:

    print(f"Procesando {station.name}")

    try:

        if station.source == "E":

            data = euskalmet.get_wind_table(
                station.code,
                20
            )

        elif station.source == "W":

            data = windguru.get_wind_table(
                station.code,
                20
            )

        else:

            continue

        all_stations.append({

            "name": station.name,
            "code": station.code,
            "source": station.source,
            "data": data

        })

    except Exception as e:

        print(f"Error en {station.name}: {e}")


env = Environment(
    loader=FileSystemLoader("templates")
)

template = env.get_template("index.html")

html = template.render(
    stations=all_stations
)

with open(
    "index.html",
    "w",
    encoding="utf-8"
) as f:

    f.write(html)

print("index.html generado correctamente")