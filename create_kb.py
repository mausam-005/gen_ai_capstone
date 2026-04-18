import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings

def initialize_knowledge_base():
    # Documents related to Bengaluru Real Estate Trends
    market_insights = [
        "Whitefield: Expanding IT hub. High demand for 2BHK and 3BHK. Expected price appreciation: 5-8% annually due to new Metro lines.",
        "Sarjapur Road: Popular among IT professionals. Excellent connectivity to Outer Ring Road. Steady appreciation, rental yields are strong (around 4-5%).",
        "Electronic City: Affordable segment with good IT park connectivity. Metro yellow line completion is boosting property prices.",
        "Indiranagar: Premium residential area. High property prices with limited new supply. Good for long-term hold and luxury living.",
        "Koramangala: Prime area, high demand, excellent social infrastructure. Very limited land availability drives prices up.",
        "Yelahanka: Emerging North Bangalore hub near the airport. Great for long term investment, large township projects are upcoming.",
        "Real Estate Regulation Authority (RERA) Karnataka mandates all projects over 500 sq meters or 8 apartments to be registered. Always verify RERA compliance before investing.",
        "Stamp Duty in Karnataka is generally set at 5% for properties above 45 Lakhs, with a 10% cess and 2% surcharge on the stamp duty. Registration fee is 1%.",
        "Bengaluru real estate overall showed a 5-7% capital appreciation in the last year, driven by return-to-office trends and strong IT sector hiring."
    ]
    
    if "GOOGLE_API_KEY" not in os.environ:
        print("GOOGLE_API_KEY not found in environment. Please set it before running this.")
        return
        
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    
    # Check if DB exists
    db_dir = "./chroma_db"
    if not os.path.exists(db_dir):
        print("Creating Chroma DB...")
        Chroma.from_texts(market_insights, embeddings, persist_directory=db_dir)
        print("Knowledge base created successfully.")
    else:
        print("Chroma DB already exists.")

if __name__ == "__main__":
    initialize_knowledge_base()
