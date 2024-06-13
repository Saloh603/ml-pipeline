from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
import datetime


app = FastAPI()

class DataItem(BaseModel):
    data: list

def update_pipeline(df, PIPELINE_PATH = "/pipeline/pipeline_.joblib"):
    X = df.drop("Personal Loan", axis=1)
    y = df['Personal Loan']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=0)

    try:
        pipeline = joblib.load(PIPELINE_PATH)
    except FileNotFoundError:
        print("Pipeline file not found. Creating a new one.")
        pipeline = Pipeline([
            ('scaler', StandardScaler()),
            ('classifier', RandomForestClassifier(random_state=0))
        ])

    pipeline.fit(X_train, y_train)
    PIPELINE_PATH = f"{PIPELINE_PATH.split('_')[0]}_{datetime.datetime.now()}.joblib"
    joblib.dump(pipeline, PIPELINE_PATH)
    y_pred = pipeline.predict(X_test)

    accuracy = metrics.accuracy_score(y_test, y_pred)
    print(f"Updated pipeline accuracy: {accuracy}")
    return PIPELINE_PATH


async def last_pipeline_path():
    import os
    files = os.listdir("pipeline/")
    files = [f for f in files if f.endswith(".joblib")]
    files = sorted(files, reverse=True)
    return files[0]


@app.post("/add_data")
async def add_data(item: DataItem):
    df = pd.DataFrame(item.data)
    if "Personal Loan" not in df.columns:
        raise HTTPException(status_code=400, detail="Personal Loan column is missing")

    pipeline_path = update_pipeline(df)
    return {"message": "Pipeline updated successfully", "pipeline_path": pipeline_path}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)