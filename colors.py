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
