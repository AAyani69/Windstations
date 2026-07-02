
from jinja2 import Environment, FileSystemLoader
from euskalmet import get_wind_table

data = get_wind_table("C019", n=20)

env = Environment(loader=FileSystemLoader("templates"))
template = env.get_template("index.html")

html = template.render(data=data)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("index.html generado correctamente")
