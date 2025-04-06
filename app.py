import os
import streamlit as st
import google.generativeai as genai
import pandas as pd
from dotenv import load_dotenv
import json

# Load API key securely
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)

# Load SHL Assessments Dataset
DATA_FILE = "SHLTask1.csv"
df = pd.read_csv(DATA_FILE)

available_assessments = df[["Name", "URL", "Duration", "Type", "Remote", "Adaptive"]].to_dict(orient="records")


# Function to get AI recommendations
def get_gemini_recommendations(query):
    model = genai.GenerativeModel("gemini-1.5-pro-001")

    prompt = f"""
    You are an AI assistant helping match job descriptions to SHL assessments.

    Here is the job description:
    \"\"\"{query}\"\"\"

    Pick the 10 most relevant assessments from this list:
    {available_assessments}

    Return a JSON list like this:
    [
    {{
        "Name": "Assessment Name",
        "URL": "https://...",
        "Duration": 45,
        "Type": "Cognitive",
        "Remote": "Yes",
        "Adaptive": "Yes"
    }}
    ]
    """



    response = model.generate_content(prompt)
    result_text = response.text

    try:
        recommendations = json.loads(result_text)
        return pd.DataFrame(recommendations)
    except json.JSONDecodeError:
        st.error("Hmm, I couldn't parse the AI's response. Here's what it said:")
        st.code(result_text)
        return pd.DataFrame()
    
    # Streamlit UI
st.set_page_config(page_title="Job Assessment Recommender")
st.title("Job Assessment Recommender")
st.markdown("Need help choosing the right assessments for a role? Just paste the job description below, and I’ll find the best matches for you.")

query = st.text_area("✍️ Paste the Job Description or Role Details Below", height=200)

if st.button("Get Assessment Recommendations"):
    if query.strip():
        st.info("🔍 Looking for the most relevant assessments...")
        recommendations = get_gemini_recommendations(query)

        if not recommendations.empty:
            st.success("✅ Here are some assessments that could be a great fit!")
            st.dataframe(recommendations, use_container_width=True)
        else:
            st.warning("I couldn’t find any matches. Try refining the job description or being more specific.")
    else:
        st.error("Please enter something about the job role before hitting the button.")
