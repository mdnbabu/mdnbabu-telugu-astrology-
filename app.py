# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect
import json
import os

app = Flask(__name__)

# Load your cities.json from the repository root
def load_cities():
    try:
        with open('cities.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"City Load Error: {e}")
        return ["విజయవాడ", "హైదరాబాద్", "గుంటూరు"]

CITIES_LIST = load_cities()

@app.route('/')
def index():
    return render_template('index.html', cities=CITIES_LIST)

@app.route('/calculate', methods=['POST'])
def calculate():
    # Capture inputs safely
    name = request.form.get('name')
    # REVENUE: Replace the link below with your specific Razorpay Payment Link
    return redirect("https://rzp.io/l/your_actual_link_here")

@app.route('/results')
def results():
    # Landing page after successful ₹11 payment
    data = {
        "nakshatra": "లెక్కించబడుతోంది...",
        "rasi": "రాశి వివరాలు",
        "pada": "1",
        "lagna": "లగ్నం",
        "shani_status": "శని ప్రభావం వివరాలు ఇక్కడ కనిపిస్తాయి."
    }
    return render_template('result.html', **data)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
    
