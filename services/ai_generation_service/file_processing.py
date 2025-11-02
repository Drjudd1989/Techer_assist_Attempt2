import hashlib
import docx
from pypdf import PdfReader
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os

HASHES_FILE = "file_hashes.log"

def calculate_hash(file_content: bytes) -> str:
    """Calculates the SHA-256 hash of the file content."""
    sha256_hash = hashlib.sha256()
    sha256_hash.update(file_content)
    return sha256_hash.hexdigest()

def load_hashes() -> set:
    """Loads the set of known file hashes from the log file."""
    if not os.path.exists(HASHES_FILE):
        return set()
    with open(HASHES_FILE, "r") as f:
        return set(line.strip() for line in f)

def save_hash(file_hash: str):
    """Appends a new hash to the log file."""
    with open(HASHES_FILE, "a") as f:
        f.write(file_hash + "\n")

def get_text_from_pdf(pdf_path: str) -> str:
    """Extracts text from a PDF file."""
    text = ""
    with open(pdf_path, "rb") as f:
        pdf_reader = PdfReader(f)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def get_text_from_docx(docx_path: str) -> str:
    """Extracts text from a DOCX file."""
    text = ""
    doc = docx.Document(docx_path)
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text

def get_text_chunks(text: str) -> list:
    """Splits text into chunks."""
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = text_splitter.split_text(text)
    return chunks

def get_vector_embeddings(chunks: list) -> list:
    """Generates vector embeddings for a list of text chunks."""
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    embedded_texts = embeddings.embed_documents(chunks)
    return embedded_texts
