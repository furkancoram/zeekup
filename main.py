from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import numpy as np
from sklearn.linear_model import LinearRegression

# FastAPI uygulamasını başlat
app = FastAPI()

# Statik dosya ve HTML şablon klasörlerini bağla
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Örnek verilerle model oluştur
X = np.array([[1], [2], [3], [4], [5]])
y = np.array([2, 4, 6, 8, 10])
model = LinearRegression()
model.fit(X, y)

# Ana sayfa - form görüntüsü (GET)
@app.get("/", response_class=HTMLResponse)
async def get_home(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "response": None
    })

# Form gönderimiyle tahmin yap (POST)
@app.post("/", response_class=HTMLResponse)
async def post_home(request: Request, message: float = Form(...)):
    input_value = np.array([[message]])
    prediction = model.predict(input_value)[0]
    
    # Noktadan sonrası silinsin diye int() kullanıyoruz
    return templates.TemplateResponse("index.html", {
        "request": request,
        "response": f"Girilen değer: {int(message)} → Tahmin: {int(prediction)}"
    })
