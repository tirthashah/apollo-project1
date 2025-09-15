# 🔹 Gemini (LangChain) imports
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage
import pandas as pd



# -----------------------------
# Initialize Gemini Model
# -----------------------------

details ={
    "chaherla ekdum nahi chahye jese dil mki tabbat i si chahera ek khab bhi chahera e fool bhi "
    "this is being so called andthe details are showing the things "
}
# AI generated note using Gemini
details = {
    "first_name": "yash",
    "company": "openAI",
    "title": "The CEO of openAI",
    "location": "US"
}
prompt = (
    f"Write a warm, professional LinkedIn connection note (40–80 words, under 300 characters) "
    f"for {details['first_name']} who works at {details['company']} as {details['title']} in {details['location']}. "
    f"Make it conversational and authentic: start with a polite greeting, mention something specific about their role or "
    f"{details['company']}'s focus (from nextgensoft.io or industry highlights), "
    f"highlight a shared interest in emerging tech, innovation, or leadership, "
    f"and end with a friendly call-to-connect. and dont add like [mention a specific area, e.g., natural language processing]  this message is directly sended to the person so right accordingly "
)
try:
    response = gemini([HumanMessage(content=prompt)])
    message = response.content.strip()
    print(message)
except Exception as gemini_err:
    print(f"⚠️ Gemini failed: {str(gemini_err)}")
    message = f"Hi {details['first_name']}, let's connect!"
