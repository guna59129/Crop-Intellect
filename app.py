from flask import Flask, render_template, request, jsonify
import joblib
import numpy as np
import os
import sqlite3
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__, template_folder='templates', static_folder='static')
model = joblib.load(r"C:\Users\guna5\OneDrive\Desktop\CROP INTELLECT(Project)\crop_recommendation_model.pkl")

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS contactdetails (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fullname TEXT NOT NULL,
            emailid TEXT NOT NULL,
            phonenumber TEXT NOT NULL,
            message TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def form():
    return render_template('home.html')

@app.route('/contactus')    
def contact_us():
    return render_template('contactus.html')

@app.route('/aboutus')
def about_us():
    return render_template('aboutus.html')

@app.route('/explorenow', methods=['GET', 'POST'])
def explore_now():
    if request.method == 'POST':
        nitrogen = float(request.form['nitrogen'])
        phosphorus = float(request.form['phosphorus'])
        potassium = float(request.form['potassium'])
        temperature = float(request.form['temperature'])
        humidity = float(request.form['humidity'])
        soil_ph = float(request.form['soil_pH'])
        rainfall = float(request.form['rainfall'])
        prediction = model.predict(np.array([[nitrogen, phosphorus, potassium, temperature, humidity, soil_ph, rainfall]]))[0]
        return jsonify({'prediction': prediction})
    else:
        return render_template('explorenow.html', prediction=None)

@app.route('/pp')
def privacy_policy():
    return render_template('pp.html')

@app.route('/tac')
def terms_and_conditions():
    return render_template('tac.html')

@app.route('/output')
def output():
    return render_template('output.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        fullname = request.form['fullname']
        emailid = request.form['emailid']
        phonenumber = request.form['phonenumber']
        message = request.form['message']
        conn = get_db_connection()
        conn.execute(
            'INSERT INTO contactdetails (fullname, emailid, phonenumber, message) VALUES (?, ?, ?, ?)',
            (fullname, emailid, phonenumber, message)
        )
        conn.commit()
        conn.close()
        return render_template('contactus.html')

@app.route('/home')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)
