from fastapi import FastAPI, Request
from pydantic import BaseModel
import google.generativeai as genai
import pandas as pd
import os
import json
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

df = pd.read_csv("SHLTask1.csv")

app = FastAPI()

class QueryInput(BaseModel):
    query: str

@app.post("/get-assessments")
def get_assessments(input: QueryInput):
    prompt = f"""
You’re an expert assistant helping recruiters choose SHL assessments for this:
\"\"\"{input.query}\"\"\"

Pick up to 10 from:
{df.to_string(index=False)}

Return only a JSON list like this:
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

    model = genai.GenerativeModel("gemini-1.5-pro-001")
    response = model.generate_content(prompt)

    try:
        return json.loads(response.text)
    except:
        return {"error": "Could not parse AI response", "raw": response.text}
