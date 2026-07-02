import requests
from datetime import date
from colors import wind_color, stronger_color

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

    print(url)

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        r = requests.get(url, headers=headers, timeout=30)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"Error descargando {url}")
        print(repr(e))
        return None




  


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

