# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect
import swisseph as swe
import datetime
import os
import pytz

app = Flask(__name__)

# తెలుగు డేటా (Telugu Data)
NAKSHATRAS = ["అశ్విని", "భరణి", "కృత్తిక", "రోహిణి", "మృగశిర", "ఆరుద్ర", "పునర్వసు", "పుష్యమి", "ఆశ్లేష", "మఖ", "పుబ్బ", "ఉత్తర", "హస్త", "చిత్త", "స్వాతి", "విశాఖ", "అనూరాధ", "జ్యేష్ట", "మూల", "పూర్వాషాఢ", "ఉత్తరాషాఢ", "శ్రవణం", "ధనిష్ట", "శతభిషం", "పూర్వాభాద్ర", "ఉత్తరాభాద్ర", "రేవతి"]
RASIS = ["మేషం", "వృషభం", "మిధునం", "కర్కాటకం", "సింహం", "కన్య", "తుల", "వృశ్చికం", "ధనుస్సు", "మకరం", "కుంభం", "మీనం"]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    # User inputs
    name = request.form.get('name')
    dob = request.form.get('dob')
    tob = request.form.get('tob')
    city = request.form.get('city')
    
    # Step 1: Redirect to Payment (Bridge Page)
    # After real payment is integrated, this will point to your Razorpay link
    return render_template('pay.html')

@app.route('/results')
def results():
    # This is the "Success" page after ₹11 payment
    # Sample data for verification
    data = {
        "nakshatra": "లెక్కించబడుతోంది...",
        "rasi": "రాశి వివరాలు",
        "pada": "1",
        "lagna": "లగ్నం",
        "shani_status": "ప్రస్తుతం శని కుంభ రాశిలో సంచరిస్తున్నారు. మీకు అనుకూల సమయం."
    }
    return render_template('result.html', **data)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
    
