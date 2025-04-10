from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Chat geçmişini geçici tutuyoruz
chat_history = []

# Türkçe destekli küçük T5 modeli
model_name = "google/mt5-small"
tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=False)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

# AI cevabı üretir
def generate_reply(message: str) -> str:
    try:
        input_text = "soru: " + message + " cevap:"
        input_ids = tokenizer.encode(input_text, return_tensors="pt", max_length=512, truncation=True)
        output = model.generate(input_ids, max_length=100, num_return_sequences=1)
        reply = tokenizer.decode(output[0], skip_special_tokens=True)
        return reply.strip()
    except Exception as e:
        return f"🤖 Bir hata oluştu: {e}"

@app.get("/", response_class=HTMLResponse)
async def get_home(request: Request):
    return templates.TemplateResponse("chat.html", {
        "request": request,
        "chat_history": chat_history
    })

@app.post("/", response_class=HTMLResponse)
async def post_home(request: Request, message: str = Form(...)):
    reply = generate_reply(message)
    chat_history.append(("user", message))
    chat_history.append(("bot", reply))
    return templates.TemplateResponse("chat.html", {
        "request": request,
        "chat_history": chat_history
    })
