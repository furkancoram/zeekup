from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

# HTML ve CSS dizinlerini bağla
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Basit kural tabanlı yanıt üretici fonksiyon
def chatbot_response(message: str) -> str:
    msg = message.lower()

    if "merhaba" in msg:
        return "Merhaba! Ben Zeekup AI 🤖 Sana nasıl yardımcı olabilirim?"
    elif "hava" in msg:
        return "Hava durumunu bilemiyorum ama umarım güneşlidir! ☀️"
    elif "teşekkür" in msg:
        return "Rica ederim kankam! 🙌"
    elif "adın ne" in msg:
        return "Ben Zeekup AI! Senin dijital kankan 😎"
    elif "ne yapabilirsin" in msg:
        return "Sana bilgi verebilirim, sayı tahmini yapabilirim, yakında çok daha fazlasını!"
    else:
        return "Üzgünüm, bunu tam anlayamadım 😅 Ama öğrenmeye açığım!"

# GET → Ana sayfa
@app.get("/", response_class=HTMLResponse)
async def get_home(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "response": None
    })

# POST → Chat mesajı geldiğinde
@app.post("/", response_class=HTMLResponse)
async def post_home(request: Request, message: str = Form(...)):
    bot_reply = chatbot_response(message)
    return templates.TemplateResponse("index.html", {
        "request": request,
        "response": f"Siz: {message} → Zeekup AI: {bot_reply}"
    })
