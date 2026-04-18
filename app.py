import streamlit as st
import pickle
from workflow import create_workflow

# Page config
st.set_page_config(
    page_title="AI Real Estate Advisor",
    layout="centered",
    page_icon="🏡",
    initial_sidebar_state="collapsed"
)

# Custom CSS - Clean & Modern Design
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Manrope:wght@600;700;800&display=swap');
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    :root {
        --primary: #0f172a;
        --primary-light: #1e3a8a;
        --accent: #06b6d4;
        --success: #10b981;
        --warning: #f59e0b;
        --danger: #ef4444;
        --bg-light: #f8fafc;
        --bg-lighter: #f1f5f9;
        --border-color: #e2e8f0;
        --text-primary: #0f172a;
        --text-secondary: #64748b;
        --text-tertiary: #94a3b8;
    }
    
    .main {
        max-width: 1000px;
        margin: 0 auto;
        background: white;
    }
    
    /* ============= HEADER SECTION ============= */
    .header-premium {
        background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 50%, #0369a1 100%);
        padding: 4rem 2.5rem;
        border-radius: 20px;
        color: white;
        margin-bottom: 3rem;
        box-shadow: 0 25px 50px rgba(15, 23, 42, 0.15);
        position: relative;
        overflow: hidden;
    }
    
    .header-premium::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 500px;
        height: 500px;
        background: radial-gradient(circle, rgba(255,255,255,0.1), transparent);
        border-radius: 50%;
    }
    
    .header-premium::after {
        content: '';
        position: absolute;
        bottom: -50%;
        left: -50%;
        width: 400px;
        height: 400px;
        background: radial-gradient(circle, rgba(6, 182, 212, 0.05), transparent);
        border-radius: 50%;
    }
    
    .header-content {
        position: relative;
        z-index: 1;
    }
    
    .header-premium h1 {
        margin: 0;
        font-size: 3.2rem;
        font-weight: 800;
        letter-spacing: -1px;
        margin-bottom: 0.75rem;
        line-height: 1.1;
    }
    
    .header-premium p {
        margin: 0;
        font-size: 1.15rem;
        opacity: 0.92;
        font-weight: 400;
        letter-spacing: -0.3px;
    }
    
    .header-badge {
        display: inline-block;
        background: rgba(255, 255, 255, 0.2);
        padding: 0.5rem 1rem;
        border-radius: 999px;
        font-size: 0.85rem;
        font-weight: 600;
        margin-bottom: 1rem;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.3);
    }
    
    /* ============= FORM SECTION ============= */
    .form-premium-wrapper {
        background: white;
        border-radius: 16px;
        padding: 2.5rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05), 0 10px 20px rgba(0, 0, 0, 0.05);
        margin-bottom: 2.5rem;
        border: 1px solid var(--border-color);
        transition: all 0.3s ease;
    }
    
    .form-premium-wrapper:hover {
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07), 0 20px 40px rgba(0, 0, 0, 0.08);
    }
    
    .form-title-premium {
        font-size: 1.75rem;
        font-weight: 700;
        color: var(--primary);
        margin-bottom: 0.5rem;
        letter-spacing: -0.5px;
    }
    
    .form-subtitle {
        font-size: 0.95rem;
        color: var(--text-secondary);
        margin-bottom: 2rem;
        font-weight: 400;
    }
    
    .input-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1.5rem;
        margin-bottom: 1.5rem;
    }
    
    @media (max-width: 768px) {
        .input-grid {
            grid-template-columns: 1fr;
            gap: 1.25rem;
        }
    }
    
    .stSelectbox {
        margin-bottom: 0.5rem;
    }
    
    .stSelectbox label {
        font-weight: 600;
        color: var(--text-primary);
        font-size: 0.95rem;
        margin-bottom: 0.5rem;
        display: block;
    }
    
    /* ============= BUTTON STYLING ============= */
    .stButton > button {
        background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 1rem 2.5rem;
        font-weight: 700;
        font-size: 1.1rem;
        width: 100%;
        letter-spacing: 0.3px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 10px 25px rgba(15, 23, 42, 0.2);
        cursor: pointer;
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.5s;
    }
    
    .stButton > button:hover {
        transform: translateY(-4px);
        box-shadow: 0 15px 35px rgba(15, 23, 42, 0.3);
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    .stButton > button:active {
        transform: translateY(-2px);
    }
    
    /* ============= RESULTS SECTION ============= */
    .results-premium {
        background: white;
        border-radius: 16px;
        padding: 3rem 2.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07), 0 20px 40px rgba(0, 0, 0, 0.08);
        animation: slideUpFade 0.5s ease-out;
    }
    
    @keyframes slideUpFade {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* ============= PRICE DISPLAY ============= */
    .price-hero {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        padding: 3rem 2rem;
        border-radius: 14px;
        text-align: center;
        margin-bottom: 3rem;
        box-shadow: 0 20px 45px rgba(16, 185, 129, 0.25);
        position: relative;
        overflow: hidden;
    }
    
    .price-hero::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 400px;
        height: 400px;
        background: radial-gradient(circle, rgba(255,255,255,0.1), transparent);
        border-radius: 50%;
    }
    
    .price-content {
        position: relative;
        z-index: 2;
    }
    
    .price-label {
        font-size: 0.9rem;
        font-weight: 700;
        opacity: 0.92;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-bottom: 0.75rem;
    }
    
    .price-amount {
        font-size: 4.5rem;
        font-weight: 800;
        margin: 0;
        margin-bottom: 0.5rem;
        letter-spacing: -1.5px;
        font-family: 'Manrope', sans-serif;
        line-height: 1;
    }
    
    .price-note {
        font-size: 0.95rem;
        opacity: 0.88;
        margin: 0;
    }
    
    /* ============= METRICS GRID ============= */
    .metrics-grid-premium {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1.25rem;
        margin-bottom: 3rem;
    }
    
    @media (max-width: 768px) {
        .metrics-grid-premium {
            grid-template-columns: repeat(2, 1fr);
            gap: 1rem;
        }
    }
    
    .metric-card-premium {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        padding: 1.75rem 1.5rem;
        border-radius: 12px;
        text-align: center;
        border: 1.5px solid var(--border-color);
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .metric-card-premium:hover {
        transform: translateY(-6px);
        border-color: var(--accent);
        box-shadow: 0 12px 24px rgba(6, 182, 212, 0.15);
    }
    
    .metric-icon {
        font-size: 1.8rem;
        margin-bottom: 0.75rem;
    }
    
    .metric-value-premium {
        font-size: 2.2rem;
        font-weight: 800;
        color: var(--primary);
        margin: 0.75rem 0;
        font-family: 'Manrope', sans-serif;
        letter-spacing: -0.5px;
    }
    
    .metric-label-premium {
        font-size: 0.8rem;
        font-weight: 700;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 0.8px;
        margin: 0;
    }
    
    /* ============= DIVIDERS ============= */
    .divider-premium {
        height: 2px;
        background: linear-gradient(90deg, transparent, var(--border-color), transparent);
        margin: 3rem 0;
        border: none;
    }
    
    /* ============= SUCCESS MESSAGE ============= */
    .success-banner {
        background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
        color: #065f46;
        padding: 1rem 1.5rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        border-left: 4px solid #10b981;
        font-weight: 600;
        text-align: center;
        animation: slideInLeft 0.3s ease;
    }
    
    @keyframes slideInLeft {
        from {
            opacity: 0;
            transform: translateX(-20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    /* ============= REPORT SECTION ============= */
    .report-premium {
        background: white;
        border-radius: 12px;
        padding: 2.5rem;
        border: 1.5px solid var(--border-color);
        line-height: 1.7;
    }
    
    .report-premium h2 {
        font-size: 1.4rem;
        font-weight: 700;
        color: var(--primary);
        margin-top: 2rem;
        margin-bottom: 1rem;
        padding-bottom: 1rem;
        border-bottom: 2px solid var(--accent);
    }
    
    .report-premium h2:first-child {
        margin-top: 0;
    }
    
    .report-premium h3 {
        font-size: 1.1rem;
        font-weight: 700;
        color: var(--text-primary);
        margin-top: 1.5rem;
        margin-bottom: 0.75rem;
    }
    
    .report-premium p {
        color: var(--text-secondary);
        margin: 0.75rem 0;
    }
    
    .report-premium ul {
        color: var(--text-secondary);
        margin-left: 1.5rem;
        margin-bottom: 1.5rem;
    }
    
    .report-premium li {
        margin-bottom: 0.5rem;
    }
    
    .report-premium strong {
        color: var(--primary);
        font-weight: 700;
    }
    
    /* ============= ACTION BADGES ============= */
    .action-badge {
        display: inline-block;
        padding: 0.75rem 1.5rem;
        border-radius: 8px;
        font-weight: 700;
        text-align: center;
        margin: 1.5rem 0;
        font-size: 1.05rem;
        letter-spacing: 0.5px;
    }
    
    .action-invest {
        background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
        color: #065f46;
        border: 2px solid #10b981;
    }
    
    .action-hold {
        background: linear-gradient(135deg, #fef3c7 0%, #fcd34d 100%);
        color: #78350f;
        border: 2px solid #f59e0b;
    }
    
    .action-caution {
        background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
        color: #7f1d1d;
        border: 2px solid #ef4444;
    }
    
    /* ============= DISCLAIMER ============= */
    .disclaimer-box {
        background: #fff7ed;
        border-left: 4px solid #f59e0b;
        padding: 1.5rem;
        border-radius: 8px;
        margin-top: 2rem;
    }
    
    .disclaimer-box p {
        color: #92400e;
        font-size: 0.95rem;
        margin: 0.5rem 0;
    }
    
    /* ============= RESPONSIVE ADJUSTMENTS ============= */
    @media (max-width: 640px) {
        .header-premium {
            padding: 2.5rem 1.5rem;
        }
        
        .header-premium h1 {
            font-size: 2.2rem;
        }
        
        .price-amount {
            font-size: 3rem;
        }
        
        .form-premium-wrapper {
            padding: 1.5rem;
        }
        
        .results-premium {
            padding: 1.5rem;
        }
        
        .price-hero {
            padding: 2rem 1.5rem;
        }
    }
    
    /* ============= ACCESSIBILITY ============= */
    .stButton > button:focus {
        outline: 2px solid var(--accent);
        outline-offset: 2px;
    }
</style>
""", unsafe_allow_html=True)

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

# Header
st.markdown("""
<div class="header-container">
    <h1>🏡 AI Real Estate Advisor</h1>
    <p>Smart Property Valuation & Investment Insights</p>
</div>
""", unsafe_allow_html=True)

# API Key Check
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
except (KeyError, FileNotFoundError):
    st.error("⚠️ Please add `GOOGLE_API_KEY` to `.streamlit/secrets.toml` to use this app")
    st.stop()

locations, area_types, availabilities = get_options()

# Form Section
st.markdown('<div class="form-container">', unsafe_allow_html=True)
st.markdown('<h2 class="form-title">Enter Property Details</h2>', unsafe_allow_html=True)

with st.form("property_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        location = st.selectbox(
            "📍 Location",
            options=locations,
            index=locations.index("Whitefield") if "Whitefield" in locations else 0,
            help="Select the property location in Bengaluru"
        )
        
        bhk = st.selectbox(
            "🛏️ Bedrooms (BHK)",
            options=list(range(1, 11)),
            index=1,
            help="Number of bedrooms"
        )
        
        balcony = st.selectbox(
            "🌳 Balconies",
            options=list(range(0, 6)),
            index=1,
            help="Number of balconies"
        )
    
    with col2:
        sqft = st.number_input(
            "📐 Total Area (sq. ft.)",
            min_value=100,
            max_value=20000,
            value=1200,
            step=100,
            help="Total area of the property"
        )
        
        bath = st.selectbox(
            "🚿 Bathrooms",
            options=list(range(1, 11)),
            index=1,
            help="Number of bathrooms"
        )
        
        area_type = st.selectbox(
            "🏗️ Area Type",
            options=area_types,
            index=0,
            help="Type of area (Built-up, Super Built-up, or Carpet area)"
        )
    
    availability = st.selectbox(
        "📅 Availability",
        options=availabilities,
        index=0,
        help="When the property is available"
    )
    
    # Submit button
    col_submit = st.columns([1, 2, 1])[1]
    with col_submit:
        submit = st.form_submit_button("🚀 Get Valuation", use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# Results Display
if submit:
    with st.spinner("🔄 Analyzing property..."):
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
            
            st.markdown('<div class="success-badge">✅ Analysis Complete!</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="results-container">', unsafe_allow_html=True)
            
            # Price Display
            predicted_price = result['predicted_price']
            st.markdown(f"""
            <div class="price-container">
                <div class="price-label">Estimated Property Value</div>
                <div class="price-value">₹ {predicted_price:.2f} L</div>
                <div class="price-subtext">Based on ML Analysis & Market Data</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Metrics
            col_m1, col_m2, col_m3, col_m4 = st.columns(4)
            
            with col_m1:
                st.markdown(f"""
                <div class="metric-box">
                    <div class="metric-title">Area</div>
                    <div class="metric-number">{sqft:,}</div>
                    <div class="metric-title">sq. ft.</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col_m2:
                st.markdown(f"""
                <div class="metric-box">
                    <div class="metric-title">BHK</div>
                    <div class="metric-number">{bhk}</div>
                    <div class="metric-title">Bedrooms</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col_m3:
                price_per_sqft = (predicted_price * 100000 / sqft)
                st.markdown(f"""
                <div class="metric-box">
                    <div class="metric-title">Price/SqFt</div>
                    <div class="metric-number">₹ {price_per_sqft:,.0f}</div>
                    <div class="metric-title">Per sq. ft.</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col_m4:
                st.markdown(f"""
                <div class="metric-box">
                    <div class="metric-title">Location</div>
                    <div class="metric-number" style="font-size: 1.5rem;">{location}</div>
                    <div class="metric-title">Bengaluru</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
            
            # Report
            st.markdown('<div class="report-container">', unsafe_allow_html=True)
            st.markdown(result["final_report"])
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            st.info("Please try again with different parameters")
