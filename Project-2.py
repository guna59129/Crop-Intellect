import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import cv2
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.feature_selection import SelectKBest, f_classif

ds = pd.read_csv(r"C:\Users\guna5\Downloads\Crop_recommendation.csv")

ds.drop(columns=['Unnamed: 8', 'Unnamed: 9'], inplace=True)

ds.columns = ["NITROGEN", "PHOSPHORUS", "POTASSIUM", "TEMPERATURE", "HUMIDITY", "SOIL_PH", "RAINFALL", "CROP"]

print(ds.isnull().sum())

print(ds[ds.duplicated()])

X = ds.iloc[:, :-1]
y = ds.iloc[:, -1]

selector = SelectKBest(score_func=f_classif, k=7)
X_selected = selector.fit_transform(X, y)

X_train, X_test, y_train, y_test = train_test_split(X_selected, y, test_size=0.2, random_state=42)

rfc = RandomForestClassifier(max_depth=10, min_samples_leaf=5, n_estimators=100, max_features='sqrt')
rfc.fit(X_train, y_train)

y_pred = rfc.predict(X_test)
print(classification_report(y_test, y_pred))
print("Accuracy:", accuracy_score(y_test, y_pred))

joblib.dump(rfc, "crop_recommendation_model.pkl")

def predict_crop(model, nitrogen, phosphorus, potassium, temperature, humidity, soil_ph, rainfall):
    try:
        prediction = model.predict([[nitrogen, phosphorus, potassium, temperature, humidity, soil_ph, rainfall]])
        return prediction[0]
    except Exception as e:
        print("Error:", e)
        return None

def display_crop_image(crop_name):
    crop_images = {
        "rice": r"C:\Users\guna5\OneDrive\Desktop\Project Images\rice.jpg",
        "coffee": r"C:\Users\guna5\OneDrive\Desktop\Project Images\coffee.jpg",
    }
    image_path = crop_images.get(crop_name.lower())
    if image_path:
        img = cv2.imread(image_path)
        cv2.imshow(f"{crop_name.capitalize()} Image", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print(f"Image not found for crop: {crop_name}")

model = joblib.load("crop_recommendation_model.pkl")
predicted_crop = predict_crop(model, nitrogen=30, phosphorus=40, potassium=20, temperature=25, humidity=60, soil_ph=6.5, rainfall=200)
if predicted_crop:
    display_crop_image(predicted_crop)
