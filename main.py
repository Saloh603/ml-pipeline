from fastapi import FastAPI
from update_pipeline import app as add_data_app
from prediction import app as prediction_app

app = FastAPI()
app.include_router(prediction_app)
app.include_router(add_data_app)
# app.mount("", add_data_app)
# app.mount("", prediction_app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
