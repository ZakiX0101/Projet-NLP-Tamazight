from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

app = FastAPI(title="API Traduction Arabe-Tamazight")

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MODEL_PATH = "./api_model"
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

print("Chargement du modèle...")

tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_PATH).to(device)

# Ce modèle est fine-tuné spécifiquement pour arabe→tamazight.
# Il n'y a pas de token de langue cible dans le vocabulaire car le modèle
# n'a qu'une seule langue de sortie. On utilise directement le decoder_start_token_id.
SRC_LANG = "arb_Arab"

print(f"Modèle chargé sur {device}.")
print(f"decoder_start_token_id: {model.config.decoder_start_token_id}")


class TranslationRequest(BaseModel):
    text: str


@app.post("/translate")
async def translate(request: TranslationRequest):
    tokenizer.src_lang = SRC_LANG
    inputs = tokenizer(request.text, return_tensors="pt").to(device)

    output_tokens = model.generate(
        **inputs,
        max_length=256,
        num_beams=4,
        early_stopping=True,
    )

    translated_text = tokenizer.decode(output_tokens[0], skip_special_tokens=True)
    return {"source_ar": request.text, "target_zgh": translated_text}