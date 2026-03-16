# -*- coding: utf-8 -*-

from flask import Flask, render_template, request
import json
import os

app = Flask(__name__)


# Load cities from JSON
def load_cities():
    try:
        with open('cities.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {}


# Home page
@app.route('/')
def index():

    cities_data = load_cities()

    city_list = []

    # Flatten state -> city structure
    for state in cities_data:
        for city in cities_data[state]:
            city_list.append(city)

    city_list.sort()

    return render_template("index.html", cities=city_list)


# Form submit → Payment page
@app.route('/calculate', methods=['POST'])
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


# Results page (temporary demo values)
@app.route('/results')
def results():

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


# Ping route for cron-job
@app.route('/ping')
def ping():
    return "alive"


# Start server
if __name__ == "__main__":

    port = int(os.environ.get("PORT", 10000))

    app.run(
        host="0.0.0.0",
        port=port
    )
