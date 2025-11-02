import os
import shutil
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Configure CORS
origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure the Gemini API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/uploadfiles/")
async def create_upload_files(files: List[UploadFile] = File(...)):
    """
    Endpoint to upload multiple curriculum files.
    """
    saved_files = []
    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)

    for file in files:
        file_path = os.path.join(upload_dir, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        saved_files.append(file.filename)

    return {"message": f"Successfully uploaded {len(saved_files)} files: {', '.join(saved_files)}"}


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
