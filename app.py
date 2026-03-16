# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect
import json
import os

app = Flask(__name__)

def load_cities():
    try:
        with open('cities.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        # Emergency backup to keep the menu active
        return ["విజయవాడ", "హైదరాబాద్", "గుంటూరు", "విశాఖపట్నం", "తిరుపతి"]

@app.route('/')
def index():
    cities_list = load_cities()
    return render_template('index.html', cities=cities_list)

@app.route('/calculate', methods=['POST'])
def calculate():
    # Insert your real Razorpay link below
    return redirect("https://rzp.io/l/your_actual_link")

@app.route('/results')
def results():
    return "మీ జాతక ఫలితాలు లోడ్ అవుతున్నాయి..."

if __name__ == "__main__":
    # This solves the Port Scan Timeout error
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
    
