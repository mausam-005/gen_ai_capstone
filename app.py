import streamlit as st
import pickle
from workflow import create_workflow

# Page config
st.set_page_config(page_title="AI Real Estate Advisor", layout="wide", page_icon="🏢")

@st.cache_resource
def load_feature_columns():
    with open("output_artifacts/feature_columns.pkl", "rb") as f:
        columns = pickle.load(f)
    return columns

@st.cache_resource
def get_options():
    columns = load_feature_columns()
    locations = [col.replace("location_", "") for col in columns if col.startswith("location_")]
    area_types = [col.replace("area_type_", "") for col in columns if col.startswith("area_type_")]
    availabilities = [col.replace("availability_", "") for col in columns if col.startswith("availability_")]
    return locations, area_types, availabilities

st.title("🤖 Agentic AI Real Estate Advisory Assistant")
st.markdown("An autonomous AI assistant that predicts property values, retrieves market trends, and generates structured investment recommendations.")

st.sidebar.header("Configuration")
# Fetch the API key unconditionally from Streamlit Secrets securely.
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
except (KeyError, FileNotFoundError):
    st.error("⚠️ **Application Error**: `GOOGLE_API_KEY` was not found in Streamlit Secrets! Please add it to your Streamlit Cloud deployment settings to continue.")
    st.stop()



st.sidebar.markdown("---")
st.sidebar.markdown("""
### About
This system uses Agentic workflows (LangGraph), RAG (ChromaDB + semantic search), and a Machine Learning pipeline to valuate properties in Bengaluru.
""")

locations, area_types, availabilities = get_options()

with st.form("property_details_form"):
    st.subheader("Property Specifications")
    
    col1, col2 = st.columns(2)
    with col1:
        location = st.selectbox("Location", options=locations, index=locations.index("Whitefield") if "Whitefield" in locations else 0)
        sqft = st.number_input("Total Area (sq. ft.)", min_value=100, max_value=20000, value=1200)
        bhk = st.number_input("BHK", min_value=1, max_value=10, value=2)
    with col2:
        bath = st.number_input("Bathrooms", min_value=1, max_value=10, value=2)
        balcony = st.number_input("Balconies", min_value=0, max_value=5, value=1)
        area_type = st.selectbox("Area Type", options=area_types, index=0)
        availability = st.selectbox("Availability", options=availabilities, index=0)
        
    submit = st.form_submit_button("Generate Advisory Report")
    
if submit:
    if not api_key:
        st.error("Please provide your Google API Key in the sidebar.")
    else:
        with st.spinner("Analyzing market, predicting values, and generating report..."):
            app = create_workflow()
            initial_state = {
                "property_details": {
                    "location": location,
                    "sqft": sqft,
                    "bhk": bhk,
                    "bath": bath,
                    "balcony": balcony,
                    "area_type": area_type,
                    "availability": availability
                },
                "google_api_key": api_key,
                "predicted_price": 0.0,
                "market_insights": "",
                "final_report": ""
            }
            
            result = app.invoke(initial_state)
            
            st.success("Analysis Complete!")
            
            st.subheader(f"Valuation: ₹ {result['predicted_price']} Lakhs")
            
            st.divider()
            
            st.subheader("Agentic Advisory Report")
            st.markdown(result["final_report"])
