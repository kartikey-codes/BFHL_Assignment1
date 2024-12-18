from datetime import datetime
from loguru import logger
import pandas as pd
from fastapi import HTTPException

file_path = "./Assignment1.xlsx"

history_df = pd.DataFrame(columns=["Timestamp", "Operation", "SheetName", "RecordId", "Changes"])


def log_change(operation: str, sheet_name: str, record_id: str, changes: dict):
    """
    Log changes to the history DataFrame.
    """
    global history_df
    new_entry = {
        "Timestamp": datetime.now().isoformat(),
        "Operation": operation,
        "SheetName": sheet_name,
        "RecordId": record_id,
        "Changes": changes
    }
    history_df = pd.concat([history_df, pd.DataFrame([new_entry])], ignore_index=True)

    try:
        with pd.ExcelWriter(file_path, engine="openpyxl", mode="a") as writer:
            # Remove the existing History sheet if present
            workbook = writer.book
            if "History" in workbook.sheetnames:
                del workbook["History"]
            # Save updated history to the sheet
            history_df.to_excel(writer, sheet_name="History", index=False)
            print(history_df)
    except Exception as e:
        logger.error(f"Failed to save history to Excel: {e}")
        raise HTTPException(status_code=500, detail="Failed to log changes.")
