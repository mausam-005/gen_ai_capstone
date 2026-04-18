import pickle
try:
    with open('output_artifacts/scaler.pkl', 'rb') as f:
        scaler = pickle.load(f)
    print("Scaler type:", type(scaler))
    print("Scaler details:", scaler)
except Exception as e:
    print("No scaler or error:", e)

try:
    with open('output_artifacts/model.pkl', 'rb') as f:
        model = pickle.load(f)
    print("Model type:", type(model))
except Exception as e:
    print("No model or error:", e)
