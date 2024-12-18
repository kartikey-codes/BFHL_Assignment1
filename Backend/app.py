from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import List, Optional
import pandas as pd
from loguru import logger
from datetime import datetime
import json

app = FastAPI()

file_path = 'Processed_Assignment1.xlsx'
accounts_df = pd.read_excel(file_path, sheet_name='Accounts')
policies_df = pd.read_excel(file_path, sheet_name='Policies')
claims_df = pd.read_excel(file_path, sheet_name='Claims')

class Account(BaseModel):
    AccountId: str
    Name: str
    Age: int
    City: str
    State: str
    Pincode: int

class Policy(BaseModel):
    HAN: str
    PolicyName: str

class Claim(BaseModel):
    Id: str
    CreatedDate: str
    CaseNumber: str
    HAN: Optional[str]
    BillAmount: float
    Status: str
    AccountId: str

@app.get("/")
def health_check():
    return {"status": "ok" , "timestamp": datetime.now()}

# Fetch customer info
@app.get("/customer/{account_id}")
def customer_information(account_id: str):
    customer = accounts_df[accounts_df['AccountId'] == account_id]
    if customer.empty:
        logger.error(f"AccountId {account_id} not found.")
        raise HTTPException(status_code=404, detail="Customer not found")

    policies = policies_df[policies_df['HAN'].isin(claims_df[claims_df['AccountId'] == account_id]['HAN'])]
    claims = claims_df[claims_df['AccountId'] == account_id]

    try:
        return {
            "customer": customer.fillna("").to_dict(orient='records')[0],
            "policies": policies.fillna("").to_dict(orient='records'),
            "claims": claims.fillna("").to_dict(orient='records')
        }
    except ValueError as e:
        logger.error(f"Error serializing response: {e}")
        raise HTTPException(status_code=500, detail="Serialization error")