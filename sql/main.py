from fastapi import FastAPI, UploadFile, HTTPException
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
import pandas as pd

app = FastAPI()

Base = declarative_base()
metadata = MetaData()

SQLALCHEMY_DATABASE_URL = "mssql+pyodbc://sa:sa@KARTIKEY-PC/bfhl_assignment1?driver=ODBC+Driver+17+for+SQL+Server"
engine = create_engine(SQLALCHEMY_DATABASE_URL)

@app.post("/upload-excel/")
async def upload_excel(file: UploadFile):
    try:
        
        excel_data = pd.ExcelFile(await file.read())
        
        for sheet_name in excel_data.sheet_names:
          
            df = excel_data.parse(sheet_name)

            columns = []
            for col in df.columns:
                col_type = String if df[col].dtype == 'object' else Float if 'float' in str(df[col].dtype) else Integer
                columns.append(Column(col, col_type))

            table = Table(sheet_name, metadata, *columns, extend_existing=True)
            metadata.create_all(engine)

            df.to_sql(sheet_name, con=engine, if_exists='append', index=False)

        return {"message": "Excel data loaded successfully."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process Excel file: {e}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
