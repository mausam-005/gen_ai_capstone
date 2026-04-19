import streamlit as st
import pickle
import os
from workflow import create_workflow

# Page config
st.set_page_config(
    page_title="AI Real Estate Advisor",
    layout="centered",
    page_icon="🏡",
    initial_sidebar_state="collapsed"
)

# Load CSS from external file to prevent IDE parsing bugs
def load_css(file_name):
    if os.path.exists(file_name):
        with open(file_name, "r") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css("style.css")

# ============= LOAD MODEL ARTIFACTS =============
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

# ============= HEADER =============
st.markdown("""
<div class="header-premium">
    <div class="header-content">
        <div class="header-badge">Property Analysis Dashboard</div>
        <h1>Bengaluru Real Estate</h1>
        <p>Advanced predictive intelligence and agentic investment advisory for property investments.</p>
    </div>
</div>
""", unsafe_allow_html=True)

# ============= API KEY CHECK =============
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
except (KeyError, FileNotFoundError):
    st.error("⚠️ Please add `GOOGLE_API_KEY` to `.streamlit/secrets.toml` to use this app")
    st.stop()

locations, area_types, availabilities = get_options()

# ============= FORM SECTION =============
st.markdown("""
<div class="form-section">
    <div class="form-header">
        <div class="form-header-text">
            <h2>Property Specifications</h2>
            <p>Define the parameters of the property you wish to analyze.</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

with st.form("property_form"):
    col1, col2 = st.columns(2)

    with col1:
        location = st.selectbox(
            "Neighborhood Location",
            options=locations,
            index=locations.index("Whitefield") if "Whitefield" in locations else 0,
            help="Select the specific area in Bengaluru"
        )

        bhk = st.selectbox(
            "Number of Bedrooms (BHK)",
            options=list(range(1, 11)),
            index=1
        )

        balcony = st.selectbox(
            "Number of Balconies",
            options=list(range(0, 6)),
            index=1
        )

    with col2:
        sqft = st.number_input(
            "Total Living Area (sq. ft.)",
            min_value=100,
            max_value=20000,
            value=1200,
            step=100
        )

        bath = st.selectbox(
            "Number of Bathrooms",
            options=list(range(1, 11)),
            index=1
        )

        area_type = st.selectbox(
            "Plot / Area Type",
            options=area_types,
            index=0
        )

    availability = st.selectbox(
        "Current Move-in Status",
        options=availabilities,
        index=0
    )

    st.markdown("")  # Spacer
    submit = st.form_submit_button("Run Analysis Pipeline", use_container_width=True)

# ============= RESULTS DISPLAY =============
if submit:
    with st.spinner("🔄 Running AI analysis pipeline..."):
        try:
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

            # Success Banner
            st.markdown('<div class="success-banner">Analysis Complete — Advisory Report Generated</div>', unsafe_allow_html=True)

            # Price Hero Card
            predicted_price = result['predicted_price']
            price_per_sqft = (predicted_price * 100000 / sqft) if sqft > 0 else 0
            st.markdown(f"""
            <div class="price-hero">
                <div class="price-content">
                    <div class="price-label">Estimated Market Valuation</div>
                    <div class="price-amount">₹ {predicted_price:.2f} L</div>
                    <div class="price-note">Based on ML Model Prediction & Current Neighborhood Data</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Metrics Grid
            st.markdown(f"""
            <div class="metrics-grid">
                <div class="metric-card">
                    <div class="metric-label">Total Area</div>
                    <div class="metric-value">{sqft:,} sq.ft.</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Configuration</div>
                    <div class="metric-value">{bhk} BHK</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Price / Sq. Ft.</div>
                    <div class="metric-value">₹{price_per_sqft:,.0f}</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Location</div>
                    <div class="metric-value" style="font-size: 1.2rem;">{location}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Section Divider
            st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

            # Advisory Report
            st.markdown("""
            <div class="report-header">
                <h2>AI Advisory Report</h2>
            </div>
            """, unsafe_allow_html=True)

            st.markdown('<div class="report-container">', unsafe_allow_html=True)
            st.markdown(result["final_report"])
            st.markdown('</div>', unsafe_allow_html=True)

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            st.info("Please try again with different parameters.")

# ============= FOOTER =============
st.markdown("""
<div class="app-footer">
    <p>Intelligent Real Estate Advisory Dashboard | Developed for Bengaluru Property Markets</p>
</div>
""", unsafe_allow_html=True)
