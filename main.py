from flask import Flask, render_template
from euskalmet import get_wind_table

app = Flask(__name__)

@app.route("/")
def home():

    data = get_wind_table("C019", n=20)

    return render_template("index.html", data=data)

if __name__ == "__main__":
    app.run(debug=True)
