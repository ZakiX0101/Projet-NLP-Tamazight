# ⵣ Tamazight NLP - Traducteur Arabe → Tamazight (NLPTMZ)

A full-stack NLP application that translates Arabic text into Tamazight (Tifinagh script) using a fine-tuned **NLLB (No Language Left Behind)** Seq2Seq model.  
Built with **FastAPI** (backend) + **React/Vite** (frontend), fully containerized with **Docker Compose**.

---

## Architecture

```
Projet-NLP-Tamazight/
├── backend/
│   ├── api_model/          ← YOU must place your model here (see below)
│   ├── main.py             ← FastAPI app (POST /translate)
│   ├── requirements.txt
│   └── dockerfile
├── frontend/
│   ├── src/
│   └── dockerfile
├── docker-compose.yml
└── nllb.ipynb              ← Training / fine-tuning notebook
```

---

##  Prerequisites: Place Your Model Files

> [!IMPORTANT]
> The model is **not included** in this repository.  
> You must provide your own fine-tuned model before running the app.

Place your fine-tuned Hugging Face model files in the following directory:

```
backend/api_model/
```

This folder must contain at minimum:

| File | Description |
|---|---|
| `config.json` | Model configuration |
| `tokenizer_config.json` | Tokenizer configuration |
| `sentencepiece.bpe.model` | SentencePiece vocabulary |
| `model.safetensors` (or `pytorch_model.bin`) | Model weights |

You can export/save a fine-tuned model from Hugging Face like this:

```python
model.save_pretrained("./backend/api_model")
tokenizer.save_pretrained("./backend/api_model")
```

Or download a compatible model from the [Hugging Face Hub](https://huggingface.co/models):

---

## Running with Docker 

### 1. Clone the repository

```bash
git clone https://github.com/ZakiX0101/Projet-NLP-Tamazight.git
cd Projet-NLP-Tamazight
```

### 2. Add your model

Follow the [section above](#-prerequisites-place-your-model-files) to populate `backend/api_model/`.

### 3. Build and start all services

```bash
docker compose up --build
```

| Service | URL |
|---|---|
| **Frontend** (React UI) | http://localhost:5173 |
| **Backend** (FastAPI) | http://localhost:8000 |
| **API Docs** (Swagger) | http://localhost:8000/docs |

### 4. Stop the application

```bash
docker compose down
```

---

## API Reference

### `POST /translate`

Translates Arabic text to Tamazight.

**Request body:**
```json
{
  "text": "مرحبا بالعالم"
}
```

**Response:**
```json
{
  "source_ar": "مرحبا بالعالم",
  "target_zgh": "ⴰⵣⵓⵍ ⴼ ⵓⵎⴰⴷⴰⵍ"
}
```

---

## Training / Fine-tuning

The Jupyter notebook `nllb.ipynb` at the root of the repository contains the full training pipeline used to fine-tune the NLLB model on an Arabic–Tamazight parallel corpus.

---

##  Tech Stack

| Layer | Technology |
|---|---|
| Model | NLLB (Seq2Seq, Hugging Face Transformers) |
| Backend | FastAPI, PyTorch, Uvicorn |
| Frontend | React 18, Vite, CSS |
| Containerization | Docker, Docker Compose |

---

## Authors

Aymane El Akkioui & Zakariae Bellil — NLP Project
