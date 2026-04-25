# ⵣ Tamazight NLP - Arabic ➔ Tamazight Neural Translator

A Data Engineering and Artificial Intelligence project providing an automatic translation system from Arabic to Tamazight (Tifinagh script). The system relies on a Transformer model (NLLB-200) fine-tuned on the Tawnza dataset, exposed via a FastAPI REST application and a React user interface.

## Project Architecture
* **ML Model:** Transfer Learning on `facebook/nllb-200-distilled-600M`
* **Backend:** FastAPI, PyTorch, HuggingFace Transformers
* **Frontend:** React, Vite
* **Infrastructure:** Docker & Docker Compose

## Important Prerequisite: The AI Model
The language model generated during training weighs several gigabytes. Due to performance reasons and GitHub storage limits, **the model weights are not versioned in this repository**.

You must manually download the model folder and place it in the correct directory before running the application.

## Installation and Execution Guide

### 1. System Requirements
Ensure you have [Docker](https://docs.docker.com/get-docker/) and Docker Compose installed on your machine.

### 2. Clone the Repository
```bash
git clone [https://github.com/your-username/projet-nlp-tamazight.git](https://github.com/your-username/projet-nlp-tamazight.git)
cd projet-nlp-tamazight
```

### 3. Add the Model

The file structure must strictly look like this :

projet-nlp-tamazight/
├── backend/
│   ├── api_model/      <-- THE MODEL MUST BE PLACED HERE
│   │   ├── model.safetensors
│   │   ├── config.json
│   │   └── ...
│   ├── main.py
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
└── docker-compose.yml

### 4. Run the Application with Docker

```bash
docker-compose up --build -d
```

### 5. Access the Application

Once the containers are running, the services are accessible via your browser:

    Web Interface : http://localhost:5173

    Interactive API Documentation (Swagger): http://localhost:8000/docs

### 6. Stop the Application
```bash
docker-compose down
```

The project was built collaboratively by Aymane El Akkioui and Zakaria Bellil.

