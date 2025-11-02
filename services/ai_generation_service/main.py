import os
from fastapi import FastAPI
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Configure the Gemini API key
# Make sure to set the GOOGLE_API_KEY environment variable in a .env file
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/generate")
def generate_text():
    """
    A simple endpoint to test the Gemini integration.
    """
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content("Say 'Hello, World!' in a creative way.")
        return {"response": response.text}
    except Exception as e:
        return {"error": str(e)}
