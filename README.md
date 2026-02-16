# RIDE_FORECASTING_MODEL

🔗 **Live App:**  
https://rideforecastingmodel-8fobxjezgukcsnbgsu4rdg.streamlit.app/

📌 Project Overview

Ride demand forecasting is critical for ride-hailing platforms like Ola to ensure optimal driver allocation, reduced wait times, and efficient surge management.
This project focuses on predicting hourly ride demand using historical ride data, weather conditions, temporal features, and location-based patterns.

The system combines machine learning, data analysis, and API-based real-time prediction to simulate a production-ready demand forecasting solution.

🎯 Objectives

Predict ride demand based on time, weather, and location

Identify peak demand hours across different locations

Analyze the impact of weather and temporal factors on ride demand

Build a deployable API for real-time ride demand prediction

📊 Dataset Description

The dataset includes historical ride records with the following features:

Ride count (target variable)

Weather information (temperature, humidity, windspeed, weather type)

Temporal features (hour, day, month, weekday)

Location information (clustered Mumbai locations)

Lag and rolling features for demand trends

User types (casual and registered users)

🔍 Methodology
1. Data Preprocessing

Handled missing values using statistical imputation

Capped outliers using percentile-based clipping

Created time-based features from datetime

Generated lag and rolling demand features

Clustered locations to simulate city-level demand zones

2. Exploratory Data Analysis (EDA)

Analyzed ride demand trends by hour, month, and location

Studied the effect of weather on ride demand

Identified peak hours and high-demand locations

Visualized correlations between features

3. Feature Engineering

Lag features (previous 1–5 hours demand)

Rolling averages for short-term trends

One-hot encoding for categorical variables

Location encoding for spatial patterns

4. Model Development

Trained and evaluated multiple models:

Linear Regression

Random Forest Regressor

Gradient Boosting Regressor (final model)

Gradient Boosting was selected based on superior performance metrics.

5. Model Evaluation

Models were evaluated using:

R² Score

Mean Absolute Error (MAE)

Mean Squared Error (MSE)

📈 Key Insights

Ride demand peaks during morning and evening commute hours

Weather conditions like rain significantly increase demand

Certain locations consistently show higher ride volumes

Lagged demand is a strong predictor of future demand

🛠️ Tools & Technologies

Python

Pandas, NumPy

Matplotlib, Seaborn

Scikit-learn

FastAPI

Joblib

🚀 Project Outcome

This project demonstrates how machine learning can be used to:

Forecast ride demand effectively

Support operational decision-making for ride-hailing platforms

Enable real-time, API-driven predictions in a production-like setup

🔮 Future Enhancements

Integrate real-time weather data using external APIs

Expand prediction to multiple cities across India

Add a live dashboard for business users

