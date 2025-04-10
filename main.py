from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# FastAPI uygulaması başlatılıyor
app = FastAPI()

# Statik dosyalar ve HTML şablon klasörü
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Mesaj geçmişi (geçici bellek - RAM)
chat_history = []

# Basit cevap veren yapay zeka fonksiyonu
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

# Ana sayfa (GET)
@app.get("/", response_class=HTMLResponse)
async def get_home(request: Request):
    return templates.TemplateResponse("chat.html", {
        "request": request,
        "chat_history": chat_history
    })

# Mesaj gönderildiğinde (POST)
@app.post("/", response_class=HTMLResponse)
async def post_home(request: Request, message: str = Form(...)):
    bot_reply = chatbot_response(message)
    chat_history.append(("user", message))
    chat_history.append(("bot", bot_reply))
    return templates.TemplateResponse("chat.html", {
        "request": request,
        "chat_history": chat_history
    })
