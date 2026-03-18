# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, session
import json
import os
import math
import razorpay

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "vedic-telugu-2026")

# ── Razorpay client – created INSIDE route, NOT at startup ───────────────────
# This prevents app crash if keys are missing at startup
def get_razorpay_client():
    key_id     = os.environ.get("RAZORPAY_KEY_ID", "")
    key_secret = os.environ.get("RAZORPAY_KEY_SECRET", "")
    return razorpay.Client(auth=(key_id, key_secret))

# ── Load cities from nested JSON ─────────────────────────────────────────────
def load_cities():
    try:
        with open('cities.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        flat = []
        for state, cities in data.items():
            for city_name, info in cities.items():
                flat.append({
                    "name":  city_name,
                    "state": state,
                    "lat":   info["lat"],
                    "lon":   info["lon"]
                })
        return flat
    except Exception as e:
        print(f"cities.json error: {e}")
        return [
            {"name": "విజయవాడ",  "state": "ఆంధ్రప్రదేశ్", "lat": 16.5062, "lon": 80.6480},
            {"name": "హైదరాబాద్", "state": "తెలంగాణ",      "lat": 17.3850, "lon": 78.4867},
        ]

CITIES = load_cities()

# ── Haversine distance ────────────────────────────────────────────────────────
def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat/2)**2 +
         math.cos(math.radians(lat1)) *
         math.cos(math.radians(lat2)) *
         math.sin(dlon/2)**2)
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

# ── Keep Render awake ─────────────────────────────────────────────────────────
@app.route('/ping')
def ping():
    return "pong", 200

# ── City search API ───────────────────────────────────────────────────────────
@app.route('/api/cities')
def api_cities():
    query = request.args.get('q', '').strip()
    lat   = request.args.get('lat', type=float)
    lon   = request.args.get('lon', type=float)

    if lat is not None and lon is not None:
        scored = sorted(
            [{**c, "distance_km": round(haversine(lat, lon, c["lat"], c["lon"]), 1)}
             for c in CITIES],
            key=lambda x: x["distance_km"]
        )
        return json.dumps(scored[:10], ensure_ascii=False), 200, {'Content-Type': 'application/json'}

    if query:
        results = [c for c in CITIES if query in c["name"]]
        return json.dumps(results[:15], ensure_ascii=False), 200, {'Content-Type': 'application/json'}

    return json.dumps(CITIES[:20], ensure_ascii=False), 200, {'Content-Type': 'application/json'}

# ── Home page ─────────────────────────────────────────────────────────────────
@app.route('/')
def index():
    return render_template("index.html")

# ── Form → Razorpay order → Payment page ─────────────────────────────────────
@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        session['name'] = request.form.get("name", "")
        session['dob']  = request.form.get("dob", "")
        session['tob']  = request.form.get("tob", "")
        session['city'] = request.form.get("city_name", "")
        session['lat']  = request.form.get("city_lat", "")
        session['lon']  = request.form.get("city_lon", "")

        # ✅ TEST: ₹1 = 100 paise
        # For live: change 100 → 1100 (₹11)
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

    # TODO: Replace stubs with real Swiss Ephemeris calculations
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
    
