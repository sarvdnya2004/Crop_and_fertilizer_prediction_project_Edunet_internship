import joblib

# Load the saved model
crop_model = joblib.load("crop_model.pkl")

# Print the classes the model was trained on
print("Crop Classes in Model:", crop_model.classes_)
