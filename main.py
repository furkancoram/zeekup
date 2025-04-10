from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Model ve tokenizer yükleniyor
model_name = "distilgpt2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

chat_history = []

# AI cevabı üretir
def generate_reply(message):
    inputs = tokenizer.encode(message + tokenizer.eos_token, return_tensors="pt")
    outputs = model.generate(inputs, max_length=100, pad_token_id=tokenizer.eos_token_id)
    reply = tokenizer.decode(outputs[0], skip_special_tokens=True)
    cleaned = reply[len(message):].strip()
    return cleaned if cleaned else "Hmm, anlamadım... 😅"

@app.get("/", response_class=HTMLResponse)
async def get_home(request: Request):
    return templates.TemplateResponse("chat.html", {
        "request": request,
        "chat_history": chat_history
    })

@app.post("/", response_class=HTMLResponse)
async def post_home(request: Request, message: str = Form(...)):
    bot_reply = generate_reply(message)
    chat_history.append(("user", message))
    chat_history.append(("bot", bot_reply))
    return templates.TemplateResponse("chat.html", {
        "request": request,
        "chat_history": chat_history
    })
