from datetime import datetime, timedelta
import requests

from colors import wind_color, stronger_color


# ---------------------------------
# URL Windguru
# ---------------------------------

def windguru_url(id_station, hours_back=48, avg_minutes=8):

    to_time = datetime.utcnow()
    from_time = to_time - timedelta(hours=hours_back)

    return (
        "https://www.windguru.cz/int/iapi.php"
        f"?q=station_data"
        f"&id_station={id_station}"
        f"&from={from_time.strftime('%Y-%m-%dT%H:%M:%S')}.000Z"
        f"&to={to_time.strftime('%Y-%m-%dT%H:%M:%S')}.000Z"
        f"&avg_minutes={avg_minutes}"
        f"&graph_info=1"
    )


# ---------------------------------
# Descarga JSON
# ---------------------------------

def get_station_data(code):

    url = windguru_url(code)

    headers = {
        "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 Chrome/120 Safari/537.36",

        "Accept":
            "application/json,text/plain,*/*",

        "Referer":
            "https://www.windguru.cz",

        "Origin":
            "https://www.windguru.cz"
    }

    r = requests.get(
        url,
        headers=headers,
        timeout=30
    )

    r.raise_for_status()

    return r.json()


# ---------------------------------
# Tabla compatible con Euskalmet
# ---------------------------------

def get_wind_table(code, n=20):

    data = get_station_data(code)

    times = data["datetime"][-n:]
    avg = data["wind_avg"][-n:]
    gust = data["wind_max"][-n:]
    direction = data["wind_direction"][-n:]
    temperature = data["temperature"][-n:]

    result = []

    for t, sp, gs, dr, tm in zip(
        times,
        avg,
        gust,
        direction,
        temperature
    ):

        sp = round(sp * 1.854, 1)
        gs = round(gs * 1.854, 1)
        
        hour = t[11:16]

        speed_color = wind_color(sp)
        gust_color = wind_color(gs)

        dir_color = stronger_color(
            speed_color,
            gust_color)
        
        temp_color = wind_color(tm)

        result.append({

            "time": hour,

            "speed": sp,

            "gust": gs,

            "direction": round(dr) if dr else None,
            
            "temperature": round(tm) if tm else None,

            "speed_color": speed_color,

            "gust_color": gust_color,

            "dir_color": dir_color,
            
            "temp_color": temp_color
        })

    return result
