from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

# FastAPI başlat
app = FastAPI()

# HTML & Statik dosyalar
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Veritabanı ayarları
DATABASE_URL = "sqlite:///./messages.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# Mesaj tablosu
class Message(Base):
    __tablename__ = "message_log"

    id = Column(Integer, primary_key=True, index=True)
    user_message = Column(String)
    bot_reply = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

# Veritabanını oluştur (ilk çalıştırmada tabloyu kurar)
Base.metadata.create_all(bind=engine)

# Basit chatbot yanıtları
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

# Ana sayfa
@app.get("/", response_class=HTMLResponse)
async def get_home(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "response": None
    })

# Mesaj geldiğinde POST işlemi
@app.post("/", response_class=HTMLResponse)
async def post_home(request: Request, message: str = Form(...)):
    reply = chatbot_response(message)

    # Veritabanına kaydet
    db = SessionLocal()
    new_message = Message(user_message=message, bot_reply=reply)
    db.add(new_message)
    db.commit()
    db.close()

    return templates.TemplateResponse("index.html", {
        "request": request,
        "response": f"Siz: {message} → Zeekup AI: {reply}"
    from fastapi import Depends
from sqlalchemy.orm import Session

# Bağlantı kuran yardımcı fonksiyon
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Admin paneli - Mesaj geçmişi
@app.get("/history", response_class=HTMLResponse)
async def get_history(request: Request, db: Session = Depends(get_db)):
    messages = db.query(Message).order_by(Message.timestamp.desc()).all()
    return templates.TemplateResponse("history.html", {
        "request": request,
        "messages": messages
    })

