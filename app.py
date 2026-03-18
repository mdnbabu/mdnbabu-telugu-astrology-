# -*- coding: utf-8 -*-

import os
import json
import math
import razorpay
import swisseph as swe
import pytz

from datetime import datetime
from flask import Flask, render_template, request, session

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "vedic-telugu-2026")

# Swiss Ephemeris setup
swe.set_sid_mode(swe.SIDM_LAHIRI)
swe.set_ephe_path(" ")

# ── Razorpay – created inside route, NOT at startup ──────────────────────────
def get_razorpay_client():
    key_id     = os.environ.get("RAZORPAY_KEY_ID", "")
    key_secret = os.environ.get("RAZORPAY_KEY_SECRET", "")
    return razorpay.Client(auth=(key_id, key_secret))

# ── Data ──────────────────────────────────────────────────────────────────────
nakshatras = [
    "అశ్విని","భరణి","కృత్తిక","రోహిణి","మృగశిర","ఆర్ద్ర",
    "పునర్వసు","పుష్యమి","ఆశ్లేష","మఘ","పూర్వఫల్గుణి",
    "ఉత్తరఫల్గుణి","హస్త","చిత్త","స్వాతి","విశాఖ",
    "అనూరాధ","జ్యేష్ఠ","మూల","పూర్వాషాఢ","ఉత్తరాషాఢ",
    "శ్రవణం","ధనిష్ఠ","శతభిషం","పూర్వాభాద్ర",
    "ఉత్తరాభాద్ర","రేవతి"
]

rasi_list = [
    "మేషం","వృషభం","మిథునం","కర్కాటకం","సింహం","కన్య",
    "తుల","వృశ్చికం","ధనుస్సు","మకరం","కుంభం","మీనం"
]

dasha_sequence = [
    "కేతు","శుక్రుడు","సూర్యుడు","చంద్రుడు","కుజుడు",
    "రాహువు","గురువు","శని","బుధుడు"
]

dasha_years = {
    "కేతు":7,"శుక్రుడు":20,"సూర్యుడు":6,"చంద్రుడు":10,"కుజుడు":7,
    "రాహువు":18,"గురువు":16,"శని":19,"బుధుడు":17
}

# ── Load cities ───────────────────────────────────────────────────────────────
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
        print(f"cities.json error: {e}")
        return ["విజయవాడ","హైదరాబాద్","గుంటూరు","విశాఖపట్నం","తిరుపతి"]

def get_city_coords(city_name):
    try:
        with open('cities.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        for state, cities in data.items():
            for cname, info in cities.items():
                if cname == city_name or info.get("roman","").lower() == city_name.lower():
                    return info["lat"], info["lon"]
    except:
        pass
    return 17.3850, 78.4867  # Default Hyderabad

# ── Keep Render awake ─────────────────────────────────────────────────────────
@app.route('/ping')
def ping():
    return "pong", 200

# ── Home page ─────────────────────────────────────────────────────────────────
@app.route('/')
def index():
    cities = load_cities()
    return render_template("index.html", cities=cities)

# ── Form → Payment ────────────────────────────────────────────────────────────
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

# ── Results – real Swiss Ephemeris calculations ───────────────────────────────
@app.route('/results', methods=['GET', 'POST'])
def results():
    try:
        payment_id = (request.form.get("razorpay_payment_id") or
                      request.args.get("razorpay_payment_id"))

        if not payment_id:
            return "<h3>చెల్లింపు అవసరం</h3><a href='/'>తిరిగి వెళ్ళు</a>", 403

        name = session.get('name', '')
        dob  = session.get('dob', '')
        tob  = session.get('tob', '')
        city = session.get('city', '')

        # Parse date and time
        year, month, day = map(int, dob.split("-"))
        hour, minute     = map(int, tob.split(":"))

        # Get coordinates
        lat, lon = get_city_coords(city)

        # Convert to UTC
        dt       = datetime(year, month, day, hour, minute)
        tz       = pytz.timezone("Asia/Kolkata")
        dt_local = tz.localize(dt)
        dt_utc   = dt_local.astimezone(pytz.utc)

        # Julian day
        jd = swe.julday(
            dt_utc.year, dt_utc.month, dt_utc.day,
            dt_utc.hour + dt_utc.minute / 60.0
        )

        # Moon and Saturn positions
        moon   = swe.calc_ut(jd, swe.MOON,   swe.FLG_SWIEPH | swe.FLG_SIDEREAL)[0][0] % 360
        saturn = swe.calc_ut(jd, swe.SATURN, swe.FLG_SWIEPH | swe.FLG_SIDEREAL)[0][0] % 360

        # Nakshatra, Pada, Rasi
        nak_span        = 360 / 27
        nak_index       = int(moon / nak_span)
        degrees_into_nak = moon % nak_span
        pada            = int(degrees_into_nak / (nak_span / 4)) + 1
        rasi_index      = int(moon / 30)

        # Lagna
        houses = swe.houses_ex(jd, lat, lon, b'P', swe.FLG_SWIEPH | swe.FLG_SIDEREAL)
        asc    = houses[0][0] % 360
        lagna  = rasi_list[int(asc / 30)]

        # Shani Dosha
        moon_sign_num   = int(moon / 30) + 1
        saturn_sign_num = int(saturn / 30) + 1
        house_from_moon = (saturn_sign_num - moon_sign_num) % 12 + 1

        shani_status = "శని గోచర దోషం లేదు"
        if house_from_moon == 8:
            shani_status = "అష్టమ శని (చంద్రుని నుండి 8వ స్థానంలో శని)"
        elif house_from_moon == 4:
            shani_status = "కంటక శని (చంద్రుని నుండి 4వ స్థానంలో శని)"
        elif house_from_moon == 1:
            shani_status = "జన్మ శని (చంద్ర రాశిలో శని)"
        elif house_from_moon == 12:
            shani_status = "సాడేసాటి - దశ 1 (చంద్రుని నుండి 12వ స్థానం)"
        elif house_from_moon == 2:
            shani_status = "సాడేసాటి - దశ 3 (చంద్రుని నుండి 2వ స్థానం)"

        # Dasha calculation
        birth_md_index = nak_index % 9
        birth_md       = dasha_sequence[birth_md_index]
        balance_years  = (1 - (degrees_into_nak / nak_span)) * dasha_years[birth_md]
        age_years      = (datetime.now() - dt).days / 365.25

        if age_years < balance_years:
            running_md = birth_md
        else:
            temp = age_years - balance_years
            idx  = (birth_md_index + 1) % 9
            while temp >= dasha_years[dasha_sequence[idx]]:
                temp -= dasha_years[dasha_sequence[idx]]
                idx   = (idx + 1) % 9
            running_md = dasha_sequence[idx]

        return render_template(
            "results.html",
            name=name,
            dob=dob,
            tob=tob,
            city=city,
            nakshatra=nakshatras[nak_index],
            pada=pada,
            rasi=rasi_list[rasi_index],
            lagna=lagna,
            birth_md=birth_md,
            running_md=running_md,
            shani_status=shani_status
        )

    except Exception as e:
        print(f"Result error: {e}")
        return f"<h3>లోపం జరిగింది: {str(e)}</h3><a href='/'>తిరిగి వెళ్ళు</a>", 500

# ── Start ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
            
