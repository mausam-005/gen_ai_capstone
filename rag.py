import os
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

DB_DIR = "./chroma_db"

market_insights = [
    "Whitefield: Expanding IT hub. High demand for 2BHK and 3BHK flats. Expected price appreciation: 5-8% annually due to expansion of Metro lines.",
    "Sarjapur Road: Popular among young IT professionals. Excellent connectivity to Outer Ring Road (ORR). Steady appreciation, rental yields are strong (around 4-5%).",
    "Electronic City: Affordable segment with good IT park connectivity. Metro yellow line completion is boosting property prices by roughly 5% over the past year.",
    "Indiranagar: Premium residential area. High property prices with limited new supply. Good for long-term hold and luxury living.",
    "Koramangala: Prime area, high demand, excellent social infrastructure. Very limited land availability drives prices up. Often sees 6-10% appreciation.",
    "Yelahanka: Emerging North Bangalore hub near the airport. Great for long term investment, large township projects are upcoming, 7% expected growth.",
    "Real Estate Regulation Authority (RERA) Karnataka mandates all projects over 500 sq meters or 8 apartments to be registered. A critical safety net for buyers.",
    "Stamp Duty in Karnataka is generally set at 5% for properties above 45 Lakhs, with a 10% cess and 2% surcharge on the stamp duty. Registration fee is 1%.",
    "Bengaluru real estate overall showed a 5-7% capital appreciation in the last year, driven by return-to-office trends and strong IT sector hiring."
]

def get_db():
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    if not os.path.exists(DB_DIR):
        print("Creating Chroma DB...")
        db = Chroma.from_texts(market_insights, embeddings, persist_directory=DB_DIR)
    else:
        db = Chroma(persist_directory=DB_DIR, embedding_function=embeddings)
    return db

def retrieve_insights(query: str, k=3):
    db = get_db()
    docs = db.similarity_search(query, k=k)
    return "\n".join([doc.page_content for doc in docs])
