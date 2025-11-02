# AI Kindergarten Teacher Assistant

This repository contains the source code for the AI Kindergarten Teacher Assistant, a tool designed to help teachers create standards-aligned lesson plans and activities.

## Project Structure

This project is organized as a monorepo with the following top-level directories:

-   `/frontend`: Contains the Next.js web application that serves as the user-facing portal.
-   `/services`: Contains backend microservices.
    -   `/ai_generation_service`: A Python-based service using FastAPI for the core AI logic and content generation.
-   `/knowledge_base`: Contains the source documents for educational standards (e.g., ELOF, MELS, MLS) that the AI uses for compliance.

## Getting Started

### Prerequisites

-   Node.js and npm (for the frontend)
-   Python 3 and pip (for the backend services)

### Running the Frontend

1.  Navigate to the frontend directory:
    ```bash
    cd frontend
    ```
2.  Install the dependencies:
    ```bash
    npm install
    ```
3.  Run the development server:
    ```bash
    npm run dev
    ```
    The application will be available at `http://localhost:3000`.

### Running the Backend AI Service

1.  Navigate to the AI service directory:
    ```bash
    cd services/ai_generation_service
    ```
2.  Create and activate the Python virtual environment:
    ```bash
    python -m venv .venv
    source .venv/bin/activate
    ```
3.  Install the Python dependencies into the virtual environment:
    ```bash
    pip install -r requirements.txt
    ```
4.  Run the FastAPI application using uvicorn:
    ```bash
    uvicorn main:app --reload
    ```
    The API will be available at `http://localhost:8000`.
