from fastapi import FastAPI, Request
from pydantic import BaseModel
import numpy as np
from sklearn.linear_model import LinearRegression
import uvicorn

# FastAPI uygulamasını başlatıyoruz
app = FastAPI()

# Örnek veri seti: X -> Girdi, y -> Tahmin edilecek çıktı
X = np.array([[1], [2], [3], [4], [5]])
y = np.array([2, 4, 6, 8, 10])

# Modeli eğitiyoruz
model = LinearRegression()
model.fit(X, y)

# İsteklerin formatı
class PredictRequest(BaseModel):
    value: float

# Ana API endpoint
@app.post("/predict")
async def predict(request: PredictRequest):
    input_value = np.array([[request.value]])
    prediction = model.predict(input_value)
    return {"input": request.value, "prediction": float(prediction[0])}
