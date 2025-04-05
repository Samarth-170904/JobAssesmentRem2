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

# Function to get AI recommendations
def get_gemini_recommendations(query):
    model = genai.GenerativeModel("gemini-1.5-pro-001")

    prompt = f"""
You’re an expert assistant helping recruiters and HR professionals choose the best SHL assessments for hiring.

Here’s a job description or requirement:
\"\"\"{query}\"\"\"

Based on this, suggest up to 10 relevant assessments from the list below.

Available assessments:
{df.to_string(index=False)}

For each recommendation, return a JSON object with:
- "Name" (name of the assessment),
- "URL" (link to the assessment),
- "Duration" (in minutes),
- "Type" (e.g. Cognitive, Behavioral, Technical),
- "Remote" (Yes or No),
- "Adaptive" (Yes or No)

Please return only the JSON list like this:
[
  {{
    "Name": "Assessment Name",
    "URL": "https://...",
    "Duration": 45,
    "Type": "Cognitive",
    "Remote": "Yes",
    "Adaptive": "Yes"
  }},
  ...
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