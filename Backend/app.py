from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field, ValidationError
from typing import Optional
import pandas as pd
from loguru import logger
from datetime import datetime
from openpyxl import load_workbook
from etl import load_excel_data, update_excel
from models import Account, Policy, Claim, UpdateAccount, UpdatePolicy, UpdateClaim
from helper import log_change

app = FastAPI()

accounts_df, policies_df, claims_df = load_excel_data()

file_path = 'Processed_Assignment1.xlsx'

# Health check route
@app.get("/")
def health_check():
    return {"status": "ok", "timestamp": datetime.now().isoformat()}

@app.get("/customer/{account_id}")
def customer_information(account_id: str):
    customer = accounts_df[accounts_df['AccountId'] == account_id]
    if customer.empty:
        logger.warning(f"Customer not found for AccountId: {account_id}")
        raise HTTPException(status_code=404, detail="Customer not found")

    policies = policies_df[policies_df['HAN'].isin(claims_df[claims_df['AccountId'] == account_id]['HAN'])]
    claims = claims_df[claims_df['AccountId'] == account_id]

    try:
        return {
            "customer": customer.fillna("").to_dict(orient="records")[0],
            "policies": policies.fillna("").to_dict(orient="records"),
            "claims": claims.fillna("").to_dict(orient="records"),
        }
    except Exception as e:
        logger.error(f"Error serializing customer data for AccountId {account_id}: {e}")
        raise HTTPException(status_code=500, detail="Error processing customer data.")

@app.put("/update/account/{account_id}")
def update_account(account_id: str, updated_data: UpdateAccount):
    customer = accounts_df[accounts_df["AccountId"] == account_id]
    if customer.empty:
        logger.warning(f"AccountId {account_id} not found.")
        raise HTTPException(status_code=404, detail="Account not found")

   
    changes = {k: v for k, v in updated_data.dict(exclude_unset=True).items()}
    for column, value in changes.items():
        accounts_df.loc[accounts_df["AccountId"] == account_id, column] = value

    update_excel("Accounts", accounts_df)  
    log_change("Update", "Accounts", account_id, changes)

    logger.info(f"Logged changes for AccountId {account_id}.")
    return {"message": f"Account {account_id} updated successfully", "changes_logged": changes}

@app.put("/update/policy/{han}")
def update_policy(han: str, updated_data: UpdatePolicy):
    policy = policies_df[policies_df["HAN"] == han]
    if policy.empty:
        logger.warning(f"HAN {han} not found.")
        raise HTTPException(status_code=404, detail="Policy not found")

   
    changes = {k: v for k, v in updated_data.dict(exclude_unset=True).items()}
    for column, value in changes.items():
        policies_df.loc[policies_df["HAN"] == han, column] = value

    update_excel("Policies", policies_df)  # Update the Excel sheet
    log_change("Update", "Policies", han, changes)

    logger.info(f"Logged changes for HAN {han}.")
    return {"message": f"Policy {han} updated successfully", "changes_logged": changes}

@app.put("/update/claim/{claim_id}")
def update_claim(claim_id: str, updated_data: UpdateClaim):
    claim = claims_df[claims_df["Id"] == claim_id]
    if claim.empty:
        logger.warning(f"ClaimId {claim_id} not found.")
        raise HTTPException(status_code=404, detail="Claim not found")

    if updated_data.AccountId and updated_data.AccountId not in accounts_df["AccountId"].values:
        raise HTTPException(status_code=400, detail="AccountId does not exist.")
    if updated_data.HAN and updated_data.HAN not in policies_df["HAN"].values:
        raise HTTPException(status_code=400, detail="HAN does not exist.")

   
    changes = {k: v for k, v in updated_data.dict(exclude_unset=True).items()}
    for column, value in changes.items():
        claims_df.loc[claims_df["Id"] == claim_id, column] = value

    update_excel("Claims", claims_df)  # Update the Excel sheet
    log_change("Update", "Claims", claim_id, changes)

    logger.info(f"Logged changes for ClaimId {claim_id}.")
    return {"message": f"Claim {claim_id} updated successfully", "changes_logged": changes}

@app.post("/add/account")
def add_account(new_data: Account):
    
    global accounts_df

    if new_data.AccountId in accounts_df["AccountId"].values:
        raise HTTPException(status_code=400, detail="AccountId already exists.")

    try:
        new_entry = new_data.dict()
        accounts_df = pd.concat([accounts_df, pd.DataFrame([new_entry])], ignore_index=True)
        update_excel("Accounts", accounts_df)
        log_change("Add", "Accounts", new_data.AccountId, new_entry)
        logger.info(f"Added new account: {new_data.AccountId}")
        return {"message": f"New account added successfully.", "entry": new_data}
    except ValidationError as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(status_code=400, detail=f"Validation error: {e}")
    except Exception as e:
        logger.error(f"Error adding account: {e}")
        raise HTTPException(status_code=500, detail=f"Error adding account: {e}")


@app.post("/add/policy")
def add_policy(new_data: Policy):

    global policies_df

    if new_data.HAN in policies_df["HAN"].values:
        raise HTTPException(status_code=400, detail="HAN already exists.")

    try:
        new_entry = new_data.dict()
        policies_df = pd.concat([policies_df, pd.DataFrame([new_entry])], ignore_index=True)
        update_excel("Policies", policies_df)
        log_change("Add", "Policies", new_data.HAN, new_entry)
        logger.info(f"Added new policy: {new_data.HAN}")
        return {"message": f"New policy added successfully.", "entry": new_data}
    except ValidationError as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(status_code=400, detail=f"Validation error: {e}")
    except Exception as e:
        logger.error(f"Error adding policy: {e}")
        raise HTTPException(status_code=500, detail=f"Error adding policy: {e}")


@app.post("/add/claim")
def add_claim(new_data: Claim):
    
    global claims_df

    if new_data.AccountId and new_data.AccountId not in accounts_df["AccountId"].values:
        raise HTTPException(status_code=400, detail="AccountId does not exist.")
    if new_data.HAN and new_data.HAN not in policies_df["HAN"].values:
        raise HTTPException(status_code=400, detail="HAN does not exist.")

    try:
        new_entry = new_data.dict()
        claims_df = pd.concat([claims_df, pd.DataFrame([new_entry])], ignore_index=True)
        update_excel("Claims", claims_df)
        log_change("Add", "Claims", new_data.Id, new_entry)
        logger.info(f"Added new claim: {new_data.Id}")
        return {"message": f"New claim added successfully.", "entry": new_data}
    except ValidationError as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(status_code=400, detail=f"Validation error: {e}")
    except Exception as e:
        logger.error(f"Error adding claim: {e}")
        raise HTTPException(status_code=500, detail=f"Error adding claim: {e}")


@app.delete("/delete/account/{account_id}")
def delete_account(account_id: str):
    
    global accounts_df, claims_df

    try:
        account = accounts_df[accounts_df["AccountId"] == account_id]
        if account.empty:
            raise HTTPException(status_code=404, detail=f"AccountId {account_id} not found.")
        accounts_df = accounts_df[accounts_df["AccountId"] != account_id]
        related_claims = claims_df[claims_df["AccountId"] == account_id]
        claims_df = claims_df[claims_df["AccountId"] != account_id]
        update_excel("Accounts", accounts_df)
        update_excel("Claims", claims_df)
        log_change("Delete", "Accounts", account_id, {"deleted": account.to_dict(orient="records"), "related_claims": related_claims.to_dict(orient="records")})
        logger.info(f"Deleted AccountId {account_id}. Also deleted {len(related_claims)} related claims.")
        return {"message": f"Account {account_id} and related claims deleted successfully."}
    except Exception as e:
        logger.error(f"Error deleting account {account_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Error deleting account {account_id}: {e}")


@app.delete("/delete/policy/{han}")
def delete_policy(han: str):
    global policies_df

    try:
        policy = policies_df[policies_df["HAN"] == han]
        if policy.empty:
            raise HTTPException(status_code=404, detail=f"HAN {han} not found.")
        policies_df = policies_df[policies_df["HAN"] != han]
        update_excel("Policies", policies_df)
        log_change("Delete", "Policies", han, {"deleted": policy.to_dict(orient="records")})
        logger.info(f"Deleted HAN {han}.")
        return {"message": f"Policy {han} deleted successfully."}
    except Exception as e:
        logger.error(f"Error deleting policy {han}: {e}")
        raise HTTPException(status_code=500, detail=f"Error deleting policy {han}: {e}")


@app.delete("/delete/claim/{claim_id}")
def delete_claim(claim_id: str):
    global claims_df

    try:
        claim = claims_df[claims_df["Id"] == claim_id]
        if claim.empty:
            raise HTTPException(status_code=404, detail=f"ClaimId {claim_id} not found.")
        claims_df = claims_df[claims_df["Id"] != claim_id]
        update_excel("Claims", claims_df)
        log_change("Delete", "Claims", claim_id, {"deleted": claim.to_dict(orient="records")})
        logger.info(f"Deleted ClaimId {claim_id}.")
        return {"message": f"Claim {claim_id} deleted successfully."}
    except Exception as e:
        logger.error(f"Error deleting claim {claim_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Error deleting claim {claim_id}: {e}")
