import os
import shutil
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import google.generativeai as genai
from dotenv import load_dotenv
from pydantic import BaseModel
from starlette.responses import StreamingResponse
from file_processing import (
    calculate_hash,
    load_hashes,
    save_hash,
    get_text_from_pdf,
    get_text_from_docx,
    get_text_chunks,
)
from vector_db import add_vectors_to_db
from rag_chain import get_rag_chain

load_dotenv()

# Configure the Gemini API key at the application level
try:
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
except AttributeError:
    print("Missing GOOGLE_API_KEY environment variable.")


app = FastAPI()

# Load existing file hashes on startup
uploaded_file_hashes = load_hashes()

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


# -- Models --
class ChatRequest(BaseModel):
    message: str

# -- RAG Chain --
rag_chain = get_rag_chain()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/uploadfiles/")
async def create_upload_files(files: List[UploadFile] = File(...)):
    """
    Endpoint to upload multiple curriculum files, checking for duplicates,
    processing them, and storing their vector embeddings in the database.
    """
    saved_files = []
    skipped_files = []
    processed_files = []
    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)

    for file in files:
        file_content = await file.read()
        file_hash = calculate_hash(file_content)

        if file_hash in uploaded_file_hashes:
            skipped_files.append(file.filename)
            continue

        file_path = os.path.join(upload_dir, file.filename)
        with open(file_path, "wb") as buffer:
            buffer.write(file_content)

        uploaded_file_hashes.add(file_hash)
        save_hash(file_hash)
        saved_files.append(file.filename)

        # Process the file content for embeddings
        text = ""
        if file.filename.endswith(".pdf"):
            text = get_text_from_pdf(file_path)
        elif file.filename.endswith(".docx"):
            text = get_text_from_docx(file_path)

        if text:
            text_chunks = get_text_chunks(text)
            if text_chunks:
                add_vectors_to_db(text_chunks, file.filename)
                processed_files.append(file.filename)


    message = ""
    if processed_files:
        message += f"Successfully uploaded and processed {len(processed_files)} files: {', '.join(processed_files)}. "
    if skipped_files:
        message += f"Skipped {len(skipped_files)} duplicate files: {', '.join(skipped_files)}."

    return {"message": message or "No new files to upload."}


@app.post("/chat")
async def chat(chat_request: ChatRequest):
    """
    Endpoint to handle chat requests using the RAG chain.
    """
    async def stream_response():
        async for chunk in rag_chain.astream(chat_request.message):
            yield chunk

    return StreamingResponse(stream_response(), media_type="text/event-stream")


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
