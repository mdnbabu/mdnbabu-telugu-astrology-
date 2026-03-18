# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, session
import json
import os
import razorpay

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "vedic-telugu-2026")


# ---------- Razorpay ----------
def get_razorpay_client():
    key_id = os.environ.get("RAZORPAY_KEY_ID", "")
    key_secret = os.environ.get("RAZORPAY_KEY_SECRET", "")
    return razorpay.Client(auth=(key_id, key_secret))


# ---------- Load Cities ----------
def load_cities():
    try:
        with open('cities.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

        city_list = []
        for state, cities in data.items():
            for city_name, city_info in cities.items():
                city_list.append(city_name)
                if "roman" in city_info:
                    city_list.append(city_info["roman"])

        city_list.sort()
        return city_list

    except Exception as e:
        print("Cities load error:", e)
        return ["విజయవాడ", "Vijayawada", "హైదరాబాద్", "Hyderabad"]


# ---------- Ping ----------
@app.route('/ping')
def ping():
    return "ok", 200


# ---------- Home ----------
@app.route('/')
def index():
    cities = load_cities()
    return render_template("index.html", cities=cities)


# ---------- Calculate ----------
@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        session['name'] = request.form.get("name", "")
        session['dob']  = request.form.get("dob", "")
        session['tob']  = request.form.get("tob", "")
        session['city'] = request.form.get("city", "")

        amount = 100  # ₹1 test

        client = get_razorpay_client()

        order = client.order.create({
            "amount": amount,
            "currency": "INR",
            "payment_capture": 1
        })

        return render_template(
            "payment.html",
            name=session['name'],
            dob=session['dob'],
            tob=session['tob'],
            city=session['city'],
            order_id=order["id"],
            key_id=os.environ.get("RAZORPAY_KEY_ID", ""),
            amount=amount
        )

    except Exception as e:
        print("Calculate error:", e)
        return "<h3>లోపం జరిగింది</h3>"


# ---------- Results ----------
@app.route('/results', methods=['POST'])
def results():
    try:
        payment_id = request.form.get("razorpay_payment_id")

        if not payment_id:
            return "<h3>చెల్లింపు కాలేదు</h3>"

        return render_template(
            "results.html",
            name=session.get('name', ''),
            dob=session.get('dob', ''),
            tob=session.get('tob', ''),
            city=session.get('city', ''),
            nakshatra="అశ్విని",
            pada="1",
            rasi="మేషం",
            lagna="వృషభం",
            shani_status="శని ప్రభావం లేదు"
        )

    except Exception as e:
        print("Result error:", e)
        return "<h3>లోపం జరిగింది</h3>"


# ---------- Run ----------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
