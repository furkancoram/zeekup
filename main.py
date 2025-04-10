from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from datetime import datetime

from collections import Counter

# FastAPI uygulaması
app = FastAPI()

# HTML + Statik dosyalar
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Veritabanı kurulumu
DATABASE_URL = "sqlite:///./messages.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# Mesaj modeli
class Message(Base):
    __tablename__ = "message_log"
    id = Column(Integer, primary_key=True, index=True)
    user_message = Column(String)
    bot_reply = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

# Veritabanı oluştur
Base.metadata.create_all(bind=engine)

# Basit cevap veren bot
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

# Anasayfa GET
@app.get("/", response_class=HTMLResponse)
async def get_home(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "response": None
    })

# Anasayfa POST
@app.post("/", response_class=HTMLResponse)
async def post_home(request: Request, message: str = Form(...)):
    reply = chatbot_response(message)
    db = SessionLocal()
    new_message = Message(user_message=message, bot_reply=reply)
    db.add(new_message)
    db.commit()
    db.close()
    return templates.TemplateResponse("index.html", {
        "request": request,
        "response": f"Siz: {message} → Zeekup AI: {reply}"
    })

# DB bağlantı helper
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Admin Panel - /history
@app.get("/history", response_class=HTMLResponse)
async def get_history(request: Request, db: Session = Depends(get_db)):
    messages = db.query(Message).order_by(Message.timestamp.desc()).all()
    total_count = db.query(Message).count()
    
    # Bugünün tarihine göre filtre
    today = datetime.utcnow().date()
    today_count = db.query(Message).filter(Message.timestamp >= datetime(today.year, today.month, today.day)).count()

    # En son mesaj
    last_msg = messages[0].timestamp.strftime('%d.%m.%Y %H:%M') if messages else "Henüz mesaj yok"

    # En çok geçen kelime
    all_words = " ".join([msg.user_message for msg in messages]).lower().split()
    common_word = Counter(all_words).most_common(1)
    most_used_word = common_word[0][0] if common_word else "Yok"

    return templates.TemplateResponse("history.html", {
        "request": request,
        "messages": messages,
        "total_count": total_count,
        "today_count": today_count,
        "last_msg": last_msg,
        "most_used_word": most_used_word
    })
