from main import *



app = FastAPI()

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

@app.post("/predict")
async def predict(item: DataItem):
    PIPELINE_PATH = await last_pipeline_path()
    try:
        pipeline = joblib.load(PIPELINE_PATH)
    except FileNotFoundError:
        return {"error": "Pipeline not found. Train the model first."}

    data = pd.DataFrame([item.dict()])
    prediction = pipeline.predict(data)
    return {"prediction": int(prediction[0])}
