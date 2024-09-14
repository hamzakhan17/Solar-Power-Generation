#!/usr/bin/env python
# coding: utf-8

# In[6]:


# import joblib

# try:
#     model = joblib.load('solarproject.pkl')
#     print("Model loaded successfully.")
# except Exception as e:
#     print(f"An error occurred while loading the model: {e}")


# In[8]:


import streamlit as st
import pandas as pd
import joblib

# Set page configuration
st.set_page_config(page_title="Solar Power Generation Prediction", layout="wide")

# Custom CSS for styling the input boxes and other elements
st.markdown(
    f"""
    <style>
    /* Set background image */
    .stApp {{
        background-image: url('https://www.twi-global.com/image-library/hero/solar-panels-istock-185272727.jpg');
        background-size: cover;
        background-position: center;
    }}

    /* Style for input boxes */
    .stNumberInput > div {{
        background-color: #000000;  /* Black background for input box */
        border-radius: 5px;
        border: none;
    }}
    
    input[type="number"] {{
        color: #00FF00;  /* Green input text */
        background-color: #000000;  /* Black input field background */
    }}

    /* Adjust the labels to be white for better visibility */
    label {{
        color: white;
        font-size: 18px;
    }}
    
    /* Style for the prediction button */
    .stButton>button {{
        background-color: green;
        color: white;
        border-radius: 5px;
        width: 100px;
        height: 40px;
        font-size: 16px;
        font-weight: bold;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Load the model
try:
    model = joblib.load('solarproject.pkl') 
    st.write("Model loaded successfully.")
except Exception as e:
    model = None
    st.error(f"An error occurred while loading the model: {e}")

# Function to make predictions
def predict_power_generated(features):
    if model is None:
        st.error("Model is not loaded. Prediction cannot be performed.")
        return None
    
    df = pd.DataFrame([features])
    
    try:
        prediction = model.predict(df)
        return prediction[0]
    except Exception as e:
        st.error(f"Prediction failed: {e}")
        return None

# Streamlit app title
st.title("Solar Power Generation Prediction")

st.write("Enter the environmental variables to predict the solar power generation:")

# User input for the 10 features in two columns
col1, col2 = st.columns(2)

with col1:
    distance_to_solar_noon = st.number_input("Distance to Solar Noon (minutes)", key="distance_to_solar_noon")
    temperature = st.number_input("Temperature (°C)", key="temperature")
    wind_direction = st.number_input("Wind Direction (°)", key="wind_direction")
    sky_cover = st.number_input("Sky Cover (oktas)", key="sky_cover")
    humidity = st.number_input("Humidity (%)", key="humidity")

with col2:
    wind_speed = st.number_input("Wind Speed (km/h)", key="wind_speed")
    visibility = st.number_input("Visibility (km)", key="visibility")
    average_wind_speed = st.number_input("Average Wind Speed (km/h)", key="average_wind_speed")
    average_pressure = st.number_input("Average Pressure (hPa)", key="average_pressure")

# Prediction button
if st.button("Predict"):
    features = {
        "distance-to-solar-noon": distance_to_solar_noon,
        "temperature": temperature,
        "wind-direction": wind_direction,
        "wind-speed": wind_speed,
        "sky-cover": sky_cover,
        "visibility": visibility,
        "humidity": humidity,
        "average-wind-speed-(period)": average_wind_speed,
        "average-pressure-(period)": average_pressure,
    }
    
    prediction = predict_power_generated(features)
    
    if prediction is not None:
        st.success(f"Predicted Power Generated: {prediction:.2f} kW")
    else:
        st.error("Prediction could not be made. Please check the model and inputs.")

