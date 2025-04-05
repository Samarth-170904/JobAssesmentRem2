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


