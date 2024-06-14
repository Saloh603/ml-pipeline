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
__URL__: /add_data

Method: POST

Description: Upload a CSV file containing new training data to update the machine learning pipeline.
