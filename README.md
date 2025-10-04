# earthquake-prediction
Earthquake Prediction &amp; Monitoring Dashboard — A Streamlit-based application that predicts earthquake magnitude, analyzes fault lines &amp; volcanic activity, and visualizes seismic patterns interactively.

# 🌍 Project RichterX – Earthquake Analysis, Prediction & Monitoring

## 📖 About the Project
This project analyzes global earthquake and volcanic data to identify patterns, predict earthquake magnitudes, and cluster seismic events.  
It combines **offline modeling (Jupyter Notebook, ML models)** with an **interactive Streamlit dashboard** for real-time monitoring and alerts.  

---

## 🎯 Objectives
- Predict earthquake magnitudes using machine learning.  
- Classify aftershocks and assess seismic risk.  
- Identify seismic clusters (using DBSCAN).  
- Provide a real-time interactive dashboard with alerts.  

---

## 📂 Dataset
- **Source:** [USGS Earthquake Catalog](https://earthquake.usgs.gov/earthquakes/feed/)  
- **Records processed:** ~9,000–9,500 (1 month sample).  
- **Features:** Magnitude, Depth, Latitude, Longitude, Time/Date, Event Type.  
- ⚠️ Note: Though it is fetching monthly data, the system supports yearly data ingestion, but full runs require **high compute resources**.  

---

## ⚙️ Methodology
### 🔹 Data Preprocessing
- Cleaning, normalization, outlier detection  
- Feature engineering: rolling stats, lag features, depth categories  

### 🔹 Supervised Learning (Prediction)
- Models tested: Logistic Regression, Random Forest, Gradient Boosting, XGBoost, LightGBM  
- ✅ Final Model: **Random Forest** (best trade-off between accuracy and speed)  

### 🔹 Unsupervised Learning (Clustering)
- Models tested: KMeans, DBSCAN  
- ✅ Final Choice: **DBSCAN** (handles irregular clusters + noise better)  

### 🔹 Validation
- Sliding-window cross-validation (train=2000, test=500) to simulate real-world temporal forecasting  

### 🔹 Deployment
- Streamlit dashboard with live USGS feed integration, model predictions, aftershock classification, and alerts  

---

## 📊 Results
- **Random Forest**: ROC-AUC ~0.99, PR-AUC ~0.85, F1 ~0.76  
- **DBSCAN**: Captured irregular cluster shapes, flagged noise points  
- **Streamlit App**: Functional with live data, real-time alerts, and interactive maps  

---

## 🚀 Streamlit App – How to Run
### 1. Clone Repository
```bash
git clone <your-repo-url>
cd <your-repo-folder>
```

---

### 2. Create and activate a virtual environment
# Create venv
python -m venv venv

# macOS / Linux
source venv/bin/activate

# Windows (PowerShell)
venv\Scripts\Activate.ps1

# Windows (CMD)
venv\Scripts\activate.bat

3. Install dependencies
pip install -r requirements.txt

4. Run the Streamlit app
streamlit run streamlit_app_1.py


The app will open in your browser at: [http://localhost:8501](http://localhost:8501)

---

## 🖼 Dashboard Features

- 🌐 **Real-time USGS earthquake feeds** (24hr, 7-day, 30-day)  
- 🗺 **Interactive global earthquake maps** (PyDeck / Folium)  
- 📊 **Magnitude prediction** with trained Random Forest model  
- ⚡ **Aftershock classification** with probability outputs  
- 🚨 **Alert system:** High / Moderate / Low risk  
- 📑 **Export results** to CSV  

---

## 📘 Documentation
- 📄 Full Project Report: *Project_Report.pdf*

---

## 🔮 Future Work
- 📡 Add seismic waveform features (P-wave, S-wave)  
- 🤖 Explore deep learning models (LSTMs, Transformers)  
- 📈 Implement probabilistic forecasting for uncertainty estimation  
- ☁️ Deploy dashboard to Streamlit Cloud / AWS / GCP for continuous monitoring  
- 📲 Integrate external alerts (SMS, Email, Webhooks)  

---

## 📚 References
- Allen, R. M., & Melgar, D. (2019). *Earthquake early warning: Advances, scientific challenges, and societal needs.* **Annual Review of Earth and Planetary Sciences, 47**, 361–388.  
- Breiman, L. (2001). *Random forests.* **Machine Learning, 45(1)**, 5–32.  
- Ester, M., Kriegel, H. P., Sander, J., & Xu, X. (1996). *A density-based algorithm for discovering clusters in large spatial databases with noise.* **KDD.**  
- USGS Earthquake Hazards Program. (2023). *Earthquake Catalog.* [https://earthquake.usgs.gov/](https://earthquake.usgs.gov/)  
- Streamlit Inc. (2023). *Streamlit: The fastest way to build and share data apps.* [https://streamlit.io](https://streamlit.io)
f Earth and Planetary Sciences, 47**, 361–388.  
- Breiman, L. (2001). *Random forests*. **Machine Learning, 45(1)**, 5–32.  
- Ester, M., Kriegel, H. P., Sander, J., & Xu, X. (1996). *A density-based algorithm for discovering clusters in large spatial databases with noise*. **KDD**.  
- USGS Earthquake Hazards Program. (2023). *Earthquake Catalog*. [https://earthquake.usgs.gov/](https://earthquake.usgs.gov/)  
- Streamlit Inc. (2023). *Streamlit: The fastest way to build and share data apps*. [https://streamlit.io](h
