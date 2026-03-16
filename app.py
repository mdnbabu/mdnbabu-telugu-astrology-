# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect
import json
import os

app = Flask(__name__)

# This backup list ensures the menu is ALWAYS active for your users
BACKUP_CITIES = ["Vijayawada", "Hyderabad", "Guntur", "Visakhapatnam", "Tirupati", "Nellore", "Kurnool", "Kakinada", "Rajahmundry"]

@app.route('/')
def index():
    # Attempt to load the full JSON, otherwise use the backup
    try:
        with open('cities.json', 'r', encoding='utf-8') as f:
            cities = json.load(f)
    except:
        cities = BACKUP_CITIES
    
    return render_template('index.html', cities=cities)

@app.route('/calculate', methods=['POST'])
def calculate():
    # Final Revenue Bridge: Put your Razorpay link here
    return redirect("https://rzp.io/l/your_actual_link")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    
