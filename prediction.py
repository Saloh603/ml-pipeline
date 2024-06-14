from fastapi import FastAPI, HTTPException, APIRouter
from pydantic import BaseModel
import pandas as pd
import joblib
import os

app = APIRouter()

class DataItem(BaseModel):
    ID: int
    Age: int
    Experience: int
    Income: int
    ZIPCode: int
    Family: int
    CCAvg: float
    Education: int
    Mortgage: int
    SecuritiesAccount: int
    CDAccount: int
    Online: int
    CreditCard: int

async def last_pipeline_path():
    pipeline_directory = "pipeline"
    pipeline_files = [f for f in os.listdir(pipeline_directory) if f.startswith("pipeline_")]
    if not pipeline_files:
        return None

    pipeline_files.sort(reverse=True)
    return os.path.join(pipeline_directory, pipeline_files[0])

@app.post("/prediction")
async def predict(item: DataItem):
    pipeline_path = await last_pipeline_path()
    if not pipeline_path:
        raise HTTPException(status_code=404, detail="Pipeline not found. Train the model first.")

    try:
        pipeline = joblib.load(pipeline_path)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Pipeline not found. Train the model first.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    data = pd.DataFrame([item.dict()])
    prediction = pipeline.predict(data)
    return {"prediction": int(prediction[0]), "pipeline_path": pipeline_path}
