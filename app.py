# -*- coding: utf-8 -*-
from flask import Flask, render_template, request
import json
import os

app = Flask(__name__)


def load_cities():
    try:
        with open("cities.json", "r", encoding="utf-8") as f:
            data = json.load(f)

        cities = []

        # Extract cities from states
        for state in data:
            for city in data[state]:
                cities.append(city)

        return cities

    except Exception as e:
        # Backup list if JSON fails
        return ["విజయవాడ", "హైదరాబాద్", "గుంటూరు", "విశాఖపట్నం", "తిరుపతి"]


@app.route("/")
def index():
    cities_list = load_cities()
    return render_template("index.html", cities=cities_list)


@app.route("/calculate", methods=["POST"])
def calculate():

    name = request.form.get("name")
    dob = request.form.get("dob")
    tob = request.form.get("tob")
    city = request.form.get("city")

    return render_template(
        "payment.html",
        name=name,
        dob=dob,
        tob=tob,
        city=city
    )


@app.route("/results")
def results():

    # Temporary test data
    nakshatra = "అశ్విని"
    pada = "1"
    rasi = "మేషం"
    lagna = "వృషభం"
    shani_status = "శని ప్రభావం లేదు"

    return render_template(
        "results.html",
        nakshatra=nakshatra,
        pada=pada,
        rasi=rasi,
        lagna=lagna,
        shani_status=shani_status
    )


@app.route("/ping")
def ping():
    return "alive"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
