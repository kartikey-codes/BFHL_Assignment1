from fastapi import FastAPI , HTTPException
from pydantic import BaseModel
from typing import List, Optional
import pandas as pd
from datetime import datetime
import uvicorn

# Load the data
file_path = "./Processed_Assignment1.xlsx"
accounts_df = pd.read_excel(file_path, sheet_name="Accounts")
policies_df = pd.read_excel(file_path, sheet_name="Policies")
claims_df = pd.read_excel(file_path, sheet_name="Claims")

app = FastAPI()

@app.get("/")
async def health_check():
    return {"status": "Healthy", "timestamp": datetime.now()}