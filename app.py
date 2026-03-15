# -*- coding: utf-8 -*-
from flask import Flask, render_template, request
import swisseph as swe
import datetime
import os

app = Flask(__name__)

# టెలుగు జ్యోతిష్య వివరాలు (Telugu Astrology Data)
NAKSHATRAS = [
    "అశ్విని", "భరణి", "కృత్తిక", "రోహిణి", "మృగశిర", "ఆరుద్ర", "పునర్వసు", "పుష్యమి", "ఆశ్లేష",
    "మఖ", "పుబ్బ", "ఉత్తర", "హస్త", "చిత్త", "స్వాతి", "విశాఖ", "అనూరాధ", "జ్యేష్ట",
    "మూల", "పూర్వాషాఢ", "ఉత్తరాషాఢ", "శ్రవణం", "ధనిష్ట", "శతభిషం", "పూర్వాభాద్ర", "ఉత్తరాభాద్ర", "రేవతి"
]

RASIS = [
    "మేషం", "వృషభం", "మిధునం", "కర్కాటకం", "సింహం", "కన్య", 
    "తుల", "వృశ్చికం", "ధనుస్సు", "మకరం", "కుంభం", "మీనం"
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    # ఇక్కడ మీ లెక్కల లాజిక్ ఉంటుంది (Your calculation logic goes here)
    # Testing with sample Telugu output
    results = {
        "nakshatra": "నక్షత్రం వివరాలు లోడ్ అవుతున్నాయి...",
        "rasi": "రాశి వివరాలు",
        "pada": "1",
        "lagna": "లగ్నం",
        "shani_status": "శని ప్రభావం వివరాలు ఇక్కడ కనిపిస్తాయి"
    }
    return render_template('result.html', **results)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
  
