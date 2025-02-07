import streamlit as st
import joblib
import numpy as np

# Load models
crop_model = joblib.load("crop_model.pkl")
fertilizer_model = joblib.load("fertilizer_prediction_model.pkl")

# Custom styling
st.set_page_config(page_title="Smart Agri Predictor", layout="wide")
st.markdown(
    """
    <style>
    body {background-color: #121212; color: white;}
    .stApp {background-color: #121212;}
    .title {text-align: center; font-size: 40px; color: #00FFAA;}
    .sub-title {text-align: center; font-size: 25px; color: #FFAA00;}
    .stTextInput, .stNumberInput {border-radius: 10px;}
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<h1 class="title">🌾 Smart Agri Predictor 🌱</h1>', unsafe_allow_html=True)
st.markdown('<h3 class="sub-title">Get the Best Crop & Fertilizer Recommendations</h3>', unsafe_allow_html=True)
st.write("___")

# Sidebar navigation
st.sidebar.title("🔍 Choose Prediction Type")
option = st.sidebar.radio("", ["🌾 Crop Prediction", "💧 Fertilizer Recommendation"])

if option == "🌾 Crop Prediction":
    st.subheader("🌾 Enter Soil & Weather Conditions")

    # Input fields
    N = st.number_input("Nitrogen (N)", 0, 150, step=1, key="crop_n")
    P = st.number_input("Phosphorus (P)", 0, 150, step=1, key="crop_p")
    K = st.number_input("Potassium (K)", 0, 150, step=1, key="crop_k")
    temperature = st.number_input("Temperature (°C)", 0.0, 50.0, step=0.1, key="crop_temp")
    humidity = st.number_input("Humidity (%)", 0.0, 100.0, step=0.1, key="crop_humid")
    ph = st.number_input("Soil pH Level", 0.0, 14.0, step=0.1, key="crop_ph")
    rainfall = st.number_input("Rainfall (mm)", 0.0, 500.0, step=0.1, key="crop_rain")

    if st.button("🚜 Predict Best Crop"):
        input_data = np.array([[N, P, K, temperature, humidity, ph, rainfall]])
        prediction = crop_model.predict(input_data)[0]  # Predict crop
        crop_names = [
            "Rice", "Maize", "Chickpea", "Kidney Beans", "Pigeon Peas", "Moth Beans", "Mung Bean",
            "Black Gram", "Lentil", "Pomegranate", "Banana", "Mango", "Grapes", "Watermelon",
            "Muskmelon", "Apple", "Orange", "Papaya", "Coconut", "Cotton", "Jute", "Coffee"
        ]
        
        recommended_crop = crop_names[prediction] if prediction < len(crop_names) else "Unknown Crop"
        st.success(f"✅ Recommended Crop: **{recommended_crop}**")
# Fertilizer Prediction Section
elif option == "💧 Fertilizer Recommendation":
    st.subheader("💧 Enter Soil & Crop Details for Fertilizer")

    # Input fields
    N_fert = st.number_input("Nitrogen (N)", 0, 150, step=1, key="fert_n")
    P_fert = st.number_input("Phosphorus (P)", 0, 150, step=1, key="fert_p")
    K_fert = st.number_input("Potassium (K)", 0, 150, step=1, key="fert_k")
    temperature_fert = st.number_input("Temperature (°C)", 0.0, 50.0, step=0.1, key="fert_temp")
    humidity_fert = st.number_input("Humidity (%)", 0.0, 100.0, step=0.1, key="fert_humid")
    moisture_fert = st.number_input("Soil Moisture (%)", 0.0, 100.0, step=0.1, key="fert_moist")
    soil_type = st.selectbox("Soil Type", ["Sandy", "Loamy", "Black", "Red", "Clayey"], key="fert_soil")
    crop_type = st.selectbox("Crop Type", [
        "Rice", "Maize", "Chickpea", "Kidney Beans", "Pigeon Peas", "Moth Beans", "Mung Bean",
        "Black Gram", "Lentil", "Pomegranate", "Banana", "Mango", "Grapes", "Watermelon",
        "Muskmelon", "Apple", "Orange", "Papaya", "Coconut", "Cotton", "Jute", "Coffee"
    ], key="fert_crop")

    # Mapping soil type and crop type to numerical values
    soil_type_map = {"Sandy": 0, "Loamy": 1, "Black": 2, "Red": 3, "Clayey": 4}
    soil_encoded = soil_type_map[soil_type]

    crop_type_map = {name: i for i, name in enumerate([
        "Rice", "Maize", "Chickpea", "Kidney Beans", "Pigeon Peas", "Moth Beans", "Mung Bean",
        "Black Gram", "Lentil", "Pomegranate", "Banana", "Mango", "Grapes", "Watermelon",
        "Muskmelon", "Apple", "Orange", "Papaya", "Coconut", "Cotton", "Jute", "Coffee"
    ])}
    crop_encoded = crop_type_map[crop_type]

    if st.button("🌱 Recommend Fertilizer"):
        # Now, input_fertilizer has 8 features
        input_fertilizer = np.array([[N_fert, P_fert, K_fert, temperature_fert, humidity_fert, moisture_fert, soil_encoded, crop_encoded]])
        prediction_fertilizer = fertilizer_model.predict(input_fertilizer)[0]

        fertilizer_names = [
            "Urea", "DAP", "MOP", "Organic Manure", "Complex Fertilizer", "NPK 14-35-14", "NPK 10-26-26",
            "NPK 20-20-20", "NPK 17-17-17", "NPK 28-28-0"
        ]

        recommended_fertilizer = fertilizer_names[prediction_fertilizer] if prediction_fertilizer < len(fertilizer_names) else "Unknown Fertilizer"
        st.success(f"✅ Recommended Fertilizer: **{recommended_fertilizer}**")
