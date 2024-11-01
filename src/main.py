import uuid

from fastapi import FastAPI
from score import run as predict

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/score")
async def score(data: dict):
    request_id = str(uuid.uuid4())
    print(f"Received request [{request_id}] with data [{data}].")
    prediction = await predict(data)
    print(f"Prediction of [{request_id}] with data [{data}]: {prediction}")
    return prediction
