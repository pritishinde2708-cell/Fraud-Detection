# Transaction Fraud Detection — Complete Run Guide

---

## 📁 Project Structure (after unzip)

```
transaction-fraud-detection-main/
├── api/
│   ├── fraud/
│   │   └── Fraud.py          ← ML pipeline class
│   └── handler.py            ← Flask API server
├── data/raw/
│   └── fraud_0.1origbase.csv ← Dataset (49MB)
├── functions/
│   ├── minmaxscaler_cycle1.joblib
│   └── onehotencoder_cycle1.joblib
├── models/
│   └── model_cycle1.joblib   ← Trained XGBoost model
├── notebooks/
│   └── transaction-fraud-detection-cycle1.ipynb
└── requirements.txt
```

---

## ✅ STEP 1 — Install Dependencies

```bash
# Create and activate a virtual environment (recommended)
python -m venv venv

# On Windows
venv\Scripts\activate

# On Mac/Linux
source venv/bin/activate

# Install all required packages
pip install flask==1.1.2 pandas==1.1.5 numpy==1.19.4 scikit-learn==0.23.2 \
            xgboost==1.3.0 joblib==0.17.0 inflection category-encoders \
            imbalanced-learn lightgbm
```

---

## ✅ STEP 2 — Fix the Model Path Bug in Fraud.py

The original `Fraud.py` has a wrong path for loading joblib files.
**Replace the `__init__` method** in `api/fraud/Fraud.py`:

```python
# ORIGINAL (broken path):
self.minmaxscaler = joblib.load('../parameters/minmaxscaler_cycle1.joblib')
self.onehotencoder = joblib.load('../parameters/onehotencoder_cycle1.joblib')

# FIXED (correct path):
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
self.minmaxscaler = joblib.load(os.path.join(BASE_DIR, 'functions', 'minmaxscaler_cycle1.joblib'))
self.onehotencoder = joblib.load(os.path.join(BASE_DIR, 'functions', 'onehotencoder_cycle1.joblib'))
```

**Also fix `handler.py`** for the model path:

```python
# ORIGINAL (broken):
model = joblib.load('../models/model_cycle1.joblib')

# FIXED:
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
model = joblib.load(os.path.join(BASE_DIR, 'models', 'model_cycle1.joblib'))
```

---

## ✅ STEP 3 — Run the Flask API

```bash
# Navigate to the api folder
cd transaction-fraud-detection-main/api

# Start the server
python handler.py
```

You should see:
```
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
```

---

## ✅ STEP 4 — Test the API

### Option A — Using Python `requests`

```python
import requests
import json

url = "http://localhost:5000/fraud/predict"

# Single transaction (dict)
transaction = {
    "step": 1,
    "type": "TRANSFER",
    "amount": 181.0,
    "nameOrig": "C1305486145",
    "oldbalanceOrg": 181.0,
    "newbalanceOrig": 0.0,
    "nameDest": "C553264065",
    "oldbalanceDest": 0.0,
    "newbalanceDest": 0.0,
    "isFlaggedFraud": 0
}

response = requests.post(url, json=transaction)
result = response.json()
print(result)
# prediction: 1 = FRAUD, 0 = LEGITIMATE
```

### Option B — Using `curl` (Terminal)

```bash
curl -X POST http://localhost:5000/fraud/predict \
     -H "Content-Type: application/json" \
     -d '{
           "step": 1,
           "type": "TRANSFER",
           "amount": 181.0,
           "nameOrig": "C1305486145",
           "oldbalanceOrg": 181.0,
           "newbalanceOrig": 0.0,
           "nameDest": "C553264065",
           "oldbalanceDest": 0.0,
           "newbalanceDest": 0.0,
           "isFlaggedFraud": 0
         }'
```

### Option C — Batch Predictions (list of transactions)

```python
import requests

url = "http://localhost:5000/fraud/predict"

transactions = [
    {
        "step": 1, "type": "TRANSFER", "amount": 181.0,
        "nameOrig": "C1305486145", "oldbalanceOrg": 181.0,
        "newbalanceOrig": 0.0, "nameDest": "C553264065",
        "oldbalanceDest": 0.0, "newbalanceDest": 0.0, "isFlaggedFraud": 0
    },
    {
        "step": 2, "type": "CASH_OUT", "amount": 50000.0,
        "nameOrig": "C840083671", "oldbalanceOrg": 50000.0,
        "newbalanceOrig": 0.0, "nameDest": "C38997010",
        "oldbalanceDest": 0.0, "newbalanceDest": 0.0, "isFlaggedFraud": 0
    }
]

response = requests.post(url, json=transactions)
print(response.json())
```

---

## ✅ STEP 5 — Run the Jupyter Notebook (Optional, for Analysis)

```bash
pip install jupyter

cd transaction-fraud-detection-main/notebooks

jupyter notebook transaction-fraud-detection-cycle1.ipynb
```

---

## 📊 API Input Fields Reference

| Field | Type | Description |
|---|---|---|
| `step` | int | Hour of transaction (1 step = 1 hour) |
| `type` | str | CASH_IN, CASH_OUT, DEBIT, PAYMENT, TRANSFER |
| `amount` | float | Transaction amount |
| `nameOrig` | str | Origin account ID |
| `oldbalanceOrg` | float | Balance before transaction (origin) |
| `newbalanceOrig` | float | Balance after transaction (origin) |
| `nameDest` | str | Destination account ID |
| `oldbalanceDest` | float | Balance before transaction (destination) |
| `newbalanceDest` | float | Balance after transaction (destination) |
| `isFlaggedFraud` | int | System flag (0 or 1) |

---

## 📈 Model Performance (XGBoost)

| Metric | Score |
|---|---|
| Balanced Accuracy | 91.5% |
| Precision | 94.4% |
| Recall | 82.9% |
| F1 Score | 88.3% |

**Fraud = 1 | Legitimate = 0**
