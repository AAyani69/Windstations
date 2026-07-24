from colors import wind_color, stronger_color
from datetime import date

import time
import requests
import urllib.request

# -------------------------
# descarga JSON
# -------------------------

def prueba(url):

    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0"
        }
    )

    with urllib.request.urlopen(req, timeout=120) as f:
        print(f.status)
        print(f.read(200))

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
        "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36",

        "Accept":
            "application/json,text/plain,*/*",

        "Accept-Language":
            "es-ES,es;q=0.9,en;q=0.8",

        "Accept-Encoding":
            "gzip, deflate, br",

        "Connection":
            "keep-alive",

        "Referer":
            "https://www.euskalmet.euskadi.eus/"
    }

    session = requests.Session()
    session.headers.update(headers)

    for intento in range(3):

        try:
            
        prueba(url)
        
        r = session.get(
            url,
            stream=True,
            timeout=(30, 120),
            allow_redirects=True
        )

        print("Status:", r.status_code)
        print("Headers recibidos")

        print(r.headers)

        texto = r.text[:200]

        print(texto)

        return r.json()
        
        except Exception as e:

            print(f"Intento {intento+1}/3 fallido")
            print(repr(e))

            time.sleep(5)

    print(f"Error descargando {url}")

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
    temperature = dict(get_last_n(data, "temperature", n))
    result = []

    for hour in speed.keys():

        sp = speed.get(hour)
        gs = gust.get(hour)
        dr = direction.get(hour)
        tm = temperature.get(hour)

        speed_val = ms_to_kmh(sp) if sp is not None else 0
        gust_val = ms_to_kmh(gs) if gs is not None else 0

        speed_color = wind_color(speed_val)
        gust_color = wind_color(gust_val)
        temp_color = wind_color(gust_val)
        
        dir_color = stronger_color(speed_color, gust_color)

        result.append({
            "time": hour,
            "speed": speed_val,
            "gust": gust_val,
            "direction": round(dr) if dr is not None else 0,
            "temperature": round(tm) if tm is not None else 0,
            "speed_color": speed_color,
            "gust_color": gust_color,
            "dir_color": dir_color,
            "temp_color": temp_color
        })

    return result


# -------------------------
# test
# -------------------------
if __name__ == "__main__":

    from pprint import pprint

    pprint(get_wind_table("C042"))

