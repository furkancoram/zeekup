from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import numpy as np
from sklearn.linear_model import LinearRegression

app = FastAPI()

# HTML şablonlar ve statik dosyalar
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Model verisi
X = np.array([[1], [2], [3], [4], [5]])
y = np.array([2, 4, 6, 8, 10])
model = LinearRegression()
model.fit(X, y)

# Ana sayfa (GET)
@app.get("/", response_class=HTMLResponse)
async def get_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "response": None})

# Form gönderildiğinde tahmin işlemi (POST)
@app.post("/", response_class=HTMLResponse)
async def post_home(request: Request, message: float = Form(...)):
    input_value = np.array([[message]])
    prediction = model.predict(input_value)[0]
    return templates.TemplateResponse("index.html", {
        "request": request,
        "response": f"Girilen değer: {message} → Tahmin: {round(prediction, 2)}"
    })
