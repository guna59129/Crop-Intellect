from flask import Flask, render_template, request, jsonify
import mysql.connector
import joblib
import numpy as np

app = Flask(__name__, template_folder='templates', static_folder='static')
model = joblib.load("crop_recommendation_model.pkl")

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Guna2854@",
    database="cropintellect"
)
cursor = db.cursor()

# crop_images = {
#     "rice": r"C:\Users\guna5\OneDrive\Desktop\CropIntellect\static\rice.jpg",
#     "coffee": r"C:\Users\guna5\OneDrive\Desktop\CropIntellect\static\coffee.jpg",
#     "apple": r"C:\Users\guna5\OneDrive\Desktop\CropIntellect\static\Apple.webp",
#     "banana": r"C:\Users\guna5\OneDrive\Desktop\CropIntellect\static\banana.webp",
#     "blackgram": r"C:\Users\guna5\OneDrive\Desktop\CropIntellect\static\blackgram.jpg",
#     "chickpea": r"C:\Users\guna5\OneDrive\Desktop\CropIntellect\static\chickpea.jpg",
#     "coconut": r"C:\Users\guna5\OneDrive\Desktop\CropIntellect\static\coconut.jpg",
#     "cotton": r"C:\Users\guna5\OneDrive\Desktop\CropIntellect\static\cotton.webp",
#     "grapes": r"C:\Users\guna5\OneDrive\Desktop\CropIntellect\static\grapes.jpg",
#     "jute": r"C:\Users\guna5\OneDrive\Desktop\CropIntellect\static\jute.jpg",
#     "kidneybeans": r"C:\Users\guna5\OneDrive\Desktop\CropIntellect\static\kidney beans.jpg",
#     "lentil": r"C:\Users\guna5\OneDrive\Desktop\CropIntellect\static\lentill.jpg",
#     "maize": r"C:\Users\guna5\OneDrive\Desktop\CropIntellect\static\maize.jpg",
#     "mango": r"C:\Users\guna5\OneDrive\Desktop\CropIntellect\static\mango.webp",
#     "mothbeans": r"C:\Users\guna5\OneDrive\Desktop\CropIntellect\static\moth bean.jpg",
#     "mungbean": r"C:\Users\guna5\OneDrive\Desktop\CropIntellect\static\mungbean.webp",
#     "muskmelon": r"C:\Users\guna5\OneDrive\Desktop\CropIntellect\static\muskmelon.jpg",
#     "orange": r"C:\Users\guna5\OneDrive\Desktop\CropIntellect\static\orange.jpg",
#     "papaya": r"C:\Users\guna5\OneDrive\Desktop\CropIntellect\static\papaya.jpg",
#     "pigeonpeas": r"C:\Users\guna5\OneDrive\Desktop\CropIntellect\static\pigeonpeas.jpg",
#     "pomegranate": r"C:\Users\guna5\OneDrive\Desktop\CropIntellect\static\pomegranate.jpeg",
#     "watermelon": r"C:\Users\guna5\OneDrive\Desktop\CropIntellect\static\watermelon.jpg"
# }

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

        query = "INSERT INTO contactdetails (fullname, emailid, phonenumber, message) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (fullname, emailid, phonenumber, message))
        db.commit()

        return render_template('contactus.html')

@app.route('/home')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)
