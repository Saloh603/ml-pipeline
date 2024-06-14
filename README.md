# ML Pipeline FastAPI Application
## Overview

This application allows users to update a machine learning pipeline with new data and make predictions using the latest trained model. It provides two main functionalities:
  1. Add Data: Update the machine learning pipeline with new training data.
  2. Prediction: Make predictions using the latest trained machine learning pipeline.

## Installation and Setup
### Prerequisites
  - Python 3.8 or later
  - FastAPI
  - Uvicorn
  - Pandas
  - Joblib
  - Scikit-learn

```sh
pip install -r requirements.txt
```
### Installation Steps
  1. Clone the repository:
     ```sh
     git clone https://github.com/yourusername/ml-pipeline.git
     cd ml-pipeline
     ```
  2. Create and activate a virtual environment:
     ```sh
     python -m venv .venv
     source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
     ```
  3. Run the application:
     ```sh
     python main.py
     ```
## File Structure
```sh
ml-pipeline/
│
├── main.py
├── update_pipeline.py
├── bank-loan-classification.ipynb
├── README.md
├── requirements.txt
├── prediction.py
├── pipeline/                # Directory where trained models are saved
└── .venv/                   # Virtual environment directory
```
## API Endpoints
### Add Data Endpoint
__URL__: _/add_data_

__Method__: POST

__Description__: Upload a CSV file containing new training data to update the machine learning pipeline.

__Request:__

file: A CSV file containing the training data. The CSV must include a "Personal Loan" column.

__Response:__
1. 200 OK
   ```json 
   {
    "message": "Pipeline updated successfully",
    "pipeline_path": "pipeline/pipeline_20240613_131504.joblib"
   }
   ```
2. 400 Bad Request:
   ```json
   {
    "detail": "Personal Loan column is missing"
   }
   ```
3. 500 Internal Server Error:
   ```json
   {
    "detail": "Error message"
   }
   ```
### Example:
```sh
curl -X POST "http://localhost:8000/add_data" -F "file=@path/to/your/file.csv"
```  

## Prediction Endpoint
__URL__: _/prediction_

__Method__: POST

__Description__: Make a prediction using the latest trained machine learning pipeline.

__Request:__

JSON body with the following fields:
```json
{
  "ID": int,
  "Age": int,
  "Experience": int,
  "Income": int,
  "ZIPCode": int,
  "Family": int,
  "CCAvg": float,
  "Education": int,
  "Mortgage": int,
  "SecuritiesAccount": int,
  "CDAccount": int,
  "Online": int,
  "CreditCard": int
}
```
__Response:__
1. 200 OK
   ```json
   {
    "prediction": int,
    "pipeline_path": "pipeline/pipeline_20240613_131504.joblib"
   }
2. 404 Not found
   ```json
   {
   "detail": "Pipeline not found. Train the model first."
   }
3. 500 Internal Server Error
   ```json
   {
    "detail": "Error message"
   }

## Explanation of Predictions
The prediction field in the response indicates the model's prediction regarding the "Personal Loan" status:

  1. __0__: The model predicts that the individual will not take a personal loan.
  2. __1__: The model predicts that the individual will take a personal loan.

### Example:
```sh
curl -X POST "http://localhost:8000/prediction" -H "Content-Type: application/json" -d '{
  "ID": 1,
  "Age": 25,
  "Experience": 2,
  "Income": 50000,
  "ZIPCode": 91107,
  "Family": 4,
  "CCAvg": 2.0,
  "Education": 2,
  "Mortgage": 0,
  "SecuritiesAccount": 1,
  "CDAccount": 0,
  "Online": 1,
  "CreditCard": 0
}'
```

