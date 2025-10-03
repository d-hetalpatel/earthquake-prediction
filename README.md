# earthquake-prediction
Earthquake Prediction &amp; Monitoring Dashboard — A Streamlit-based application that predicts earthquake magnitude, analyzes fault lines &amp; volcanic activity, and visualizes seismic patterns interactively.

# Earthquake Prediction & Monitoring Dashboard

This repository contains a Streamlit application and supporting resources for earthquake prediction and monitoring.  
The project integrates machine learning, geospatial data, and interactive visualizations to provide insights into seismic activity.

## Features
- **Machine Learning Model**: Trained using historical earthquake data (saved as `earthquake_models_and_data.pkl`).
- **Geospatial Analysis**: Incorporates fault line (`gem_active_faults_harmonized.shp`) and volcanic activity (`volcanoes_all_list.csv`) datasets.
- **Interactive Dashboard**: Built with Streamlit to visualize predictions, aftershock classification, and regional risk.
- **Visualizations**: Includes time-series plots, heatmaps, and geospatial maps for better understanding seismic patterns.

## Repository Structure
earthquake-prediction/
│── streamlit_app_eq.py # Streamlit app (main entry point)
│── PO_64 Project RichterX1.ipynb # Jupyter notebook for experiments
│── earthquake_models_and_data.pkl # Trained ML model
│── gem_active_faults_harmonized.shp # Fault line dataset
│── volcanoes_all_list.csv # Volcanic activity dataset
│── requirements.txt # Python dependencies
│── README.md # Documentation
