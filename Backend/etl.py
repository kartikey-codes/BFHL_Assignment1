import pandas as pd
from openpyxl import load_workbook
from loguru import logger
from fastapi import HTTPException

file_path = 'Processed_Assignment1.xlsx'

def load_excel_data():
    try:
        accounts_df = pd.read_excel(file_path, sheet_name='Accounts')
        policies_df = pd.read_excel(file_path, sheet_name='Policies')
        claims_df = pd.read_excel(file_path, sheet_name='Claims')
        logger.info("Excel data loaded successfully.")
        return accounts_df, policies_df, claims_df
    except Exception as e:
        logger.error(f"Error loading Excel file: {e}")
        raise HTTPException(status_code=500, detail="Failed to load Excel data.")

def update_excel(sheet_name: str, updated_df: pd.DataFrame):
    try:
        with pd.ExcelWriter(file_path, engine="openpyxl", mode="a", if_sheet_exists="overlay") as writer:
            workbook = writer.book
            if sheet_name in workbook.sheetnames:
                del workbook[sheet_name]
            updated_df.to_excel(writer, sheet_name=sheet_name, index=False)
            logger.info(f"Updated Excel sheet: {sheet_name}")
    except Exception as e:
        logger.error(f"Failed to update Excel sheet {sheet_name}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to update Excel sheet {sheet_name}.")
