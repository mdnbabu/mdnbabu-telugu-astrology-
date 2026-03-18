# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, session
import json
import os
import razorpay

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "vedic-telugu-2026")

# ── Razorpay client – created INSIDE route to prevent startup crash ──────────
def get_razorpay_client():
    key_id     = os.environ.get("RAZORPAY_KEY_ID", "")
    key_secret = os.environ.get("RAZORPAY_KEY_SECRET", "")
    return razorpay.Client(auth=(key_id, key_secret))

# ── Load cities – returns flat list of city names ────────────────────────────
def load_cities():
    try:
        with open('cities.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        city_list = []
        for state, cities in data.items():
            for city_name in cities:
                city_list.append(city_name)
        city_list.sort()
        return city_list
    except Exception as e:
        print(f"cities.json error: {e}")
        return ["విజయవాడ", "హైదరాబాద్", "గుంటూరు", "విశాఖపట్నం", "తిరుపతి"]

# ── Keep Render awake ─────────────────────────────────────────────────────────
@app.route('/ping')
def ping():
    return "pong", 200

# ── Home page ─────────────────────────────────────────────────────────────────
@app.route('/')
def index():
    cities = load_cities()
    return render_template("index.html", cities=cities)

# ── Form → Razorpay order → Payment page ─────────────────────────────────────
@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        session['name'] = request.form.get("name", "")
        session['dob']  = request.form.get("dob", "")
        session['tob']  = request.form.get("tob", "")
        session['city'] = request.form.get("city", "")

        # ✅ TEST: ₹1 = 100 paise
        # For live change 100 → 1100 (₹11)
        amount = 100

        client = get_razorpay_client()
        order  = client.order.create({
            "amount":          amount,
            "currency":        "INR",
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
        print(f"Calculate error: {e}")
        return f"<h3>లోపం జరిగింది: {str(e)}</h3><a href='/'>తిరిగి వెళ్ళు</a>", 500

# ── Results – accepts GET and POST ───────────────────────────────────────────
@app.route('/results', methods=['GET', 'POST'])
def results():
    payment_id = (request.form.get("razorpay_payment_id") or
                  request.args.get("razorpay_payment_id"))

    if not payment_id:
        return "<h3>చెల్లింపు అవసరం</h3><a href='/'>తిరిగి వెళ్ళు</a>", 403

    name = session.get('name', '')
    dob  = session.get('dob', '')
    tob  = session.get('tob', '')
    city = session.get('city', '')

    return render_template(
        "results.html",
        name=name,
        dob=dob,
        tob=tob,
        city=city,
        nakshatra="అశ్విని",
        pada="1",
        rasi="మేషం",
        lagna="వృషభం",
        birth_md="శుక్రుడు",
        running_md="సూర్యుడు",
        shani_status="శని ప్రభావం లేదు"
    )

# ── Start ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
    
