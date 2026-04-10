import requests
import json

URL = "http://localhost:5000/fraud/predict"

# ── Single Transaction Test ───────────────────────────────────────────────────
print("=" * 50)
print("TEST 1: Single Transaction (likely FRAUD)")
print("=" * 50)

fraud_transaction = {
    "step": 1,
    "type": "TRANSFER",
    "amount": 181.0,
    "nameOrig": "C1305486145",
    "oldbalanceOrg": 181.0,
    "newbalanceOrig": 0.0,       # balance drained to 0 → fraud signal
    "nameDest": "C553264065",
    "oldbalanceDest": 0.0,
    "newbalanceDest": 0.0,
    "isFlaggedFraud": 0
}

response = requests.post(URL, json=fraud_transaction)
result = response.json()
label = "🚨 FRAUD" if result[0]['prediction'] == 1 else "✅ LEGITIMATE"
print(f"Prediction: {label}")
print(json.dumps(result, indent=2))

# ── Single Transaction Test 2 ─────────────────────────────────────────────────
print("\n" + "=" * 50)
print("TEST 2: Single Transaction (likely LEGITIMATE)")
print("=" * 50)

legit_transaction = {
    "step": 10,
    "type": "PAYMENT",
    "amount": 500.0,
    "nameOrig": "C840083671",
    "oldbalanceOrg": 10000.0,
    "newbalanceOrig": 9500.0,    # partial spend → normal
    "nameDest": "M1979787155",
    "oldbalanceDest": 0.0,
    "newbalanceDest": 0.0,
    "isFlaggedFraud": 0
}

response = requests.post(URL, json=legit_transaction)
result = response.json()
label = "🚨 FRAUD" if result[0]['prediction'] == 1 else "✅ LEGITIMATE"
print(f"Prediction: {label}")
print(json.dumps(result, indent=2))

# ── Batch Test ────────────────────────────────────────────────────────────────
print("\n" + "=" * 50)
print("TEST 3: Batch of 3 Transactions")
print("=" * 50)

batch = [
    {
        "step": 1, "type": "TRANSFER", "amount": 50000.0,
        "nameOrig": "C111111111", "oldbalanceOrg": 50000.0,
        "newbalanceOrig": 0.0, "nameDest": "C222222222",
        "oldbalanceDest": 0.0, "newbalanceDest": 0.0, "isFlaggedFraud": 0
    },
    {
        "step": 5, "type": "CASH_OUT", "amount": 200000.0,
        "nameOrig": "C333333333", "oldbalanceOrg": 200000.0,
        "newbalanceOrig": 0.0, "nameDest": "C444444444",
        "oldbalanceDest": 0.0, "newbalanceDest": 0.0, "isFlaggedFraud": 0
    },
    {
        "step": 20, "type": "PAYMENT", "amount": 1500.0,
        "nameOrig": "C555555555", "oldbalanceOrg": 30000.0,
        "newbalanceOrig": 28500.0, "nameDest": "M999999999",
        "oldbalanceDest": 5000.0, "newbalanceDest": 6500.0, "isFlaggedFraud": 0
    }
]

response = requests.post(URL, json=batch)
results = response.json()
for i, r in enumerate(results):
    label = "🚨 FRAUD" if r['prediction'] == 1 else "✅ LEGITIMATE"
    print(f"Transaction {i+1}: {label}  (amount={r['amount']})")
