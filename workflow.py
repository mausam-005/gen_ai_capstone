import os
from typing import TypedDict, Dict, Any
from langgraph.graph import StateGraph, START, END
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from predict import predict_price
from rag import retrieve_insights

class AgentState(TypedDict):
    property_details: Dict[str, Any]
    predicted_price: float
    market_insights: str
    final_report: str
    google_api_key: str

def predict_node(state: AgentState):
    details = state["property_details"]
    price = predict_price(
        location=details.get("location", ""),
        sqft=details.get("sqft", 1000),
        bhk=details.get("bhk", 2),
        bath=details.get("bath", 2),
        balcony=details.get("balcony", 1),
        area_type=details.get("area_type", "Super built-up  Area"),
        availability=details.get("availability", "Ready To Move")
    )
    return {"predicted_price": price}

def retrieve_node(state: AgentState):
    location = state["property_details"].get("location", "")
    insights = retrieve_insights(f"Real estate market trends for {location} in Bengaluru")
    return {"market_insights": insights}

def generate_advisory_node(state: AgentState):
    details = state["property_details"]
    price = state["predicted_price"]
    insights = state["market_insights"]
    api_key = state.get("google_api_key", "")
    
    if not api_key:
        return {"final_report": "Error: Google API Key is missing. Cannot generate advisory report."}
        
    if api_key.lower() == "demo":
        mock_report = f"""### 1. Property Valuation & Market Summary
The property is valued at ₹ {price} Lakhs. Based on the provided insights:
{insights}
This represents a standard valuation aligned with the current expanding trends in this specific sector.

### 2. Comparable Property Analysis (Comps)
Theoretically, properties of similar configuration ({details.get('bhk')} BHK, {details.get('sqft')} sq.ft.) in {details.get('location')} demonstrate analogous yields.

### 3. Action Recommendation
**INVEST** - Driven by strong local factors and anticipated growth, this is a reasonable entry point.

### 4. Financial & Legal Disclaimer
*Disclaimer: This is an AI-generated advisory demo utilizing fixed model templates rather than live API calls. Do not base financial decisions solely on this.*"""
        return {"final_report": mock_report}

    llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", google_api_key=api_key, max_tokens=1024)
    
    prompt = PromptTemplate(
        input_variables=["location", "bhk", "sqft", "price", "insights"],
        template='''You are an expert AI Real Estate Advisor.
Generate a structured advisory report for a property in Bengaluru with the following details:
Location: {location}
Size: {bhk} BHK, {sqft} sq.ft.
Predicted Price Valuation: ₹{price} Lakhs 

Market Insights Retrieved:
{insights}

Your report must be in Markdown format and include these specific sections verbatim:
### 1. Property Valuation & Market Summary
Outline the property valuation and an overview of the local market. Provide reasoning on why this valuation makes sense based on the insights.

### 2. Comparable Property Analysis (Comps)
Theoretically analyze how similar properties might fare in this area based on standard trends.

### 3. Action Recommendation
Give a Buy/Invest recommendation (with reasons). Focus on long-term value, rental yield potential, etc.

### 4. Financial & Legal Disclaimer
Ensure standard financial and legal disclaimers about predictions models and real estate market risks.
'''
    )
    
    chain = prompt | llm
    
    try:
        report = chain.invoke({
            "location": details.get("location"),
            "bhk": details.get("bhk"),
            "sqft": details.get("sqft"),
            "price": price,
            "insights": insights
        })
        return {"final_report": report.content}
    except Exception as e:
        error_msg = f"**Error:** Could not generate advisory report. This is most likely due to an invalid Google API Key.\n\n_Details:_ {str(e)}\n\nTry entering exactly `demo` in the API Key field to see a mocked response without an API key."
        return {"final_report": error_msg}

def create_workflow():
    workflow = StateGraph(AgentState)
    
    workflow.add_node("predict", predict_node)
    workflow.add_node("retrieve", retrieve_node)
    workflow.add_node("advisory", generate_advisory_node)
    
    # Linear graph
    workflow.add_edge(START, "predict")
    workflow.add_edge("predict", "retrieve")
    workflow.add_edge("retrieve", "advisory")
    workflow.add_edge("advisory", END)
    
    return workflow.compile()
