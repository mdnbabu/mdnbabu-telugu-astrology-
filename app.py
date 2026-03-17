# -*- coding: utf-8 -*-

from flask import Flask, render_template, request
import json
import os
import razorpay

app = Flask(__name__)

# Razorpay setup
RAZORPAY_KEY_ID = os.environ.get("RAZORPAY_KEY_ID")
RAZORPAY_KEY_SECRET = os.environ.get("RAZORPAY_KEY_SECRET")

client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))


# Load cities
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

    for state in cities_data:
        for city in cities_data[state]:
            city_list.append(city)

    city_list.sort()

    return render_template("index.html", cities=city_list)


# Form → Payment
@app.route('/calculate', methods=['POST'])
def calculate():

    name = request.form.get("name")
    dob = request.form.get("dob")
    tob = request.form.get("tob")
    city = request.form.get("city")

    # ✅ ₹1 TEST AMOUNT (100 paise)
    amount = 100

    order = client.order.create({
        "amount": amount,
        "currency": "INR",
        "payment_capture": 1
    })

    return render_template(
        "payment.html",
        name=name,
        dob=dob,
        tob=tob,
        city=city,
        order_id=order["id"],
        key_id=RAZORPAY_KEY_ID,
        amount=amount
    )


# Result page (AFTER PAYMENT)
@app.route('/results', methods=['POST'])
def results():

    # 🔒 Payment verification
    if not request.form.get("razorpay_payment_id"):
        return "Payment required", 403

    # Temporary values (later we connect real logic)
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


# Ping (optional)
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
