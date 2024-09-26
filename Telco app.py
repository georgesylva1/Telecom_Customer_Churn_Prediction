# Step 1: Load necessary libraries
import os
import pandas as pd
import numpy as np
import streamlit as st
import joblib
import tensorflow as tf
from tensorflow.keras.models import load_model

# Step 2: Load the preprocessor
preprocessor_path = 'data_preprocessor.joblib'
if not os.path.exists(preprocessor_path):
    st.error(f"Preprocessor file not found at: {preprocessor_path}")
    preprocessor = None
else:
    preprocessor = joblib.load(preprocessor_path)

# Step 3: Load the best model
model_path = 'neural_network_model.keras'
if not os.path.exists(model_path):
    st.error(f"Model file not found at: {model_path}")
    best_nn_model = None
else:
    best_nn_model = load_model(model_path)

# Step 4: Define the function to predict
def predict(input_data):
    if preprocessor is None or best_nn_model is None:
        st.error("Model or preprocessor not loaded.")
        return None, None, None

    try:
        # Preprocess the input data
        input_df = pd.DataFrame([input_data], columns=[
            'tenure', 'MonthlyCharges', 'TotalCharges',
            'gender', 'SeniorCitizen', 'Partner', 'Dependents', 
            'PhoneService', 'MultipleLines', 'InternetService', 
            'OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 
            'TechSupport', 'StreamingTV', 'StreamingMovies', 
            'Contract', 'PaperlessBilling', 'PaymentMethod'
        ])
        processed_input = preprocessor.transform(input_df)  # Apply the preprocessor

        # Make prediction
        prediction = best_nn_model.predict(processed_input)
        churn_probability = prediction[0][0]  # Extract the prediction value
        churn_comment = "High likelihood of leaving" if churn_probability > 0.5 else "Low likelihood of leaving"
        
        # Calculate discount only for those likely to churn
        discount_percentage = min(churn_probability * 20, 20) if churn_probability > 0.5 else 0

        return churn_probability, churn_comment, discount_percentage

    except Exception as e:
        st.error(str(e))
        return None, None, None

# Step 5: Create the Streamlit app layout
st.title("Telco Customer Churn Prediction")
st.markdown("### Enter Customer Details")

# Create input fields
input_data = {}
input_data['tenure'] = st.number_input("Tenure (months)", min_value=0.0)
input_data['MonthlyCharges'] = st.number_input("Monthly Charges ($)", min_value=0.0)
input_data['TotalCharges'] = st.number_input("Total Charges ($)", min_value=0.0)
input_data['gender'] = st.selectbox("Gender", ["Male", "Female"])
input_data['SeniorCitizen'] = st.selectbox("Senior Citizen (1/0)", [0, 1])
input_data['Partner'] = st.selectbox("Partner (Yes/No)", ["Yes", "No"])
input_data['Dependents'] = st.selectbox("Dependents (Yes/No)", ["Yes", "No"])
input_data['PhoneService'] = st.selectbox("Phone Service (Yes/No)", ["Yes", "No"])
input_data['MultipleLines'] = st.selectbox("Multiple Lines (Yes/No/No phone service)", ["Yes", "No", "No phone service"])
input_data['InternetService'] = st.selectbox("Internet Service (DSL/Fiber optic/No)", ["DSL", "Fiber optic", "No"])
input_data['OnlineSecurity'] = st.selectbox("Online Security (Yes/No/No internet service)", ["Yes", "No", "No internet service"])
input_data['OnlineBackup'] = st.selectbox("Online Backup (Yes/No/No internet service)", ["Yes", "No", "No internet service"])
input_data['DeviceProtection'] = st.selectbox("Device Protection (Yes/No/No internet service)", ["Yes", "No", "No internet service"])
input_data['TechSupport'] = st.selectbox("Tech Support (Yes/No/No internet service)", ["Yes", "No", "No internet service"])
input_data['StreamingTV'] = st.selectbox("Streaming TV (Yes/No/No internet service)", ["Yes", "No", "No internet service"])
input_data['StreamingMovies'] = st.selectbox("Streaming Movies (Yes/No/No internet service)", ["Yes", "No", "No internet service"])
input_data['Contract'] = st.selectbox("Contract (Month-to-month/One year/Two year)", ["Month-to-month", "One year", "Two year"])
input_data['PaperlessBilling'] = st.selectbox("Paperless Billing (Yes/No)", ["Yes", "No"])
input_data['PaymentMethod'] = st.selectbox("Payment Method (Electronic check/Mailed check/Bank transfer(automatic)/Credit card(automatic))", 
                                            ["Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"])

# Create a predict button
if st.button("Predict"):
    churn_probability, churn_comment, discount_percentage = predict(input_data)

    if churn_probability is not None:
        st.success(f"Predicted value: {churn_probability:.2f}\n"
                   f"Comment: {churn_comment}\n"
                   f"Recommended discount: {discount_percentage:.2f}%")
