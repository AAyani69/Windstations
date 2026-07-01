from datetime import date
import requests


# -------------------------
# descarga JSON
# -------------------------
def get_station_data(code):

    today = date.today()

    url = (
        f"https://www.euskalmet.euskadi.eus/vamet/stations/readings/"
        f"{code}/"
        f"{today.year}/"
        f"{today.month:02d}/"
        f"{today.day:02d}/"
        f"webmet00-readingsData.json"
    )

    r = requests.get(url)
    r.raise_for_status()

    return r.json()


# -------------------------
# serie temporal
# -------------------------
def get_series(json_data, variable_name):

    for item in json_data.values():
        if item.get("name") == variable_name:
            values = next(iter(item["data"].values()))
            return sorted(values.items())

    return []


# -------------------------
# últimos N valores
# -------------------------
def get_last_n(json_data, variable_name, n=20):
    series = get_series(json_data, variable_name)
    return series[-n:]


# -------------------------
# conversión
# -------------------------
def ms_to_kmh(ms):
    return ms * 3.6


# -------------------------
# colores
# -------------------------
def wind_color(speed):

    if speed < 20:
        return "green"
    elif speed < 30:
        return "yellow"
    elif speed < 40:
        return "orange"
    elif speed < 50:
        return "red"
    else:
        return "darkred"


COLOR_RANK = {
    "green": 1,
    "yellow": 2,
    "orange": 3,
    "red": 4,
    "darkred": 5
}


def stronger_color(c1, c2):
    return c1 if COLOR_RANK[c1] >= COLOR_RANK[c2] else c2


# -------------------------
# tabla viento
# -------------------------
def get_wind_table(code, n=20):

    data = get_station_data(code)

    speed = dict(get_last_n(data, "mean_speed", n))
    gust = dict(get_last_n(data, "max_speed", n))
    direction = dict(get_last_n(data, "mean_direction", n))

    result = []

    for hour in speed.keys():

        sp = speed.get(hour)
        gs = gust.get(hour)
        dr = direction.get(hour)

        speed_val = ms_to_kmh(sp) if sp else None
        gust_val = ms_to_kmh(gs) if gs else None

        speed_color = wind_color(speed_val)
        gust_color = wind_color(gust_val)

        dir_color = stronger_color(speed_color, gust_color)

        result.append({
            "time": hour,
            "speed": speed_val,
            "gust": gust_val,
            "direction": round(dr) if dr else None,
            "speed_color": speed_color,
            "gust_color": gust_color,
            "dir_color": dir_color
        })

    return result


# -------------------------
# test
# -------------------------
if __name__ == "__main__":

    from pprint import pprint

    pprint(get_wind_table("C042"))

