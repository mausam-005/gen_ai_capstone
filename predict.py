import pickle
import numpy as np

# Load artifacts once
with open("output_artifacts/model.pkl", "rb") as f:
    model = pickle.load(f)

with open("output_artifacts/scaler.pkl", "rb") as f:
    scaler = pickle.load(f)

with open("output_artifacts/feature_columns.pkl", "rb") as f:
    feature_columns = pickle.load(f)

def predict_price(location, sqft, bhk, bath, balcony, area_type, availability):
    # Initialize input array
    x = np.zeros(len(feature_columns))
    
    # Numerical features
    x[0] = bhk
    x[1] = sqft
    x[2] = bath
    x[3] = balcony
    
    # Categorical features - Area Type
    area_feature = f"area_type_{area_type}"
    if area_feature in feature_columns:
        loc_index = feature_columns.index(area_feature)
        x[loc_index] = 1
        
    # Categorical features - Location
    loc_feature = f"location_{location}"
    if loc_feature in feature_columns:
        loc_index = feature_columns.index(loc_feature)
        x[loc_index] = 1
        
    # Categorical features - Availability
    avail_feature = f"availability_{availability}"
    if avail_feature in feature_columns:
        loc_index = feature_columns.index(avail_feature)
        x[loc_index] = 1
        
    # Scale feature [only numerical or everything?] 
    # Usually StandardScaler is used on all features if applied wholesale. 
    # Let's apply it on the 2D array representation
    x_scaled = scaler.transform([x])
    
    predicted_log_price = model.predict(x_scaled)[0]
    
    # Not sure if price is log transformed, standard scaler might reverse it? 
    # Assuming standard prediction returns normal price or needs exponentiation.
    # Usually in regression of price, some people use log. We'll return it as is.
    return round(predicted_log_price, 2)
