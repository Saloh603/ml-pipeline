from fastapi import FastAPI, HTTPException, UploadFile, File
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
import datetime
from io import StringIO
import os

app = FastAPI()


def update_pipeline(df, pipeline_directory="pipeline"):
    if not os.path.exists(pipeline_directory):
        os.makedirs(pipeline_directory)

    X = df.drop("Personal Loan", axis=1)
    y = df['Personal Loan']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=0)

    pipeline_path = os.path.join(pipeline_directory, "pipeline_.joblib")
    try:
        pipeline = joblib.load(pipeline_path)
    except (FileNotFoundError, ValueError):
        print("Pipeline file not found or incompatible. Creating a new one.")
        pipeline = Pipeline([
            ('scaler', StandardScaler()),
            ('classifier', RandomForestClassifier(random_state=0))
        ])

    pipeline.fit(X_train, y_train)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    new_pipeline_path = os.path.join(pipeline_directory, f"pipeline_{timestamp}.joblib")
    joblib.dump(pipeline, new_pipeline_path)
    y_pred = pipeline.predict(X_test)

    accuracy = metrics.accuracy_score(y_test, y_pred)
    print(f"Updated pipeline accuracy: {accuracy}")
    return new_pipeline_path

@app.post("/add_data")
async def add_data(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        df = pd.read_csv(StringIO(contents.decode('utf-8')))
        if "Personal Loan" not in df.columns:
            raise HTTPException(status_code=400, detail="Personal Loan column is missing")

        pipeline_path = update_pipeline(df)
        return {"message": "Pipeline updated successfully", "pipeline_path": pipeline_path}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
