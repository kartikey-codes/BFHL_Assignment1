# models.py

from pydantic import BaseModel, Field
from typing import Optional

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

class UpdateAccount(BaseModel):
    Name: Optional[str] = Field(None, example="John Doe")
    Age: Optional[int] = Field(None, example=30)
    City: Optional[str] = Field(None, example="New York")
    State: Optional[str] = Field(None, example="NY")
    Pincode: Optional[int] = Field(None, example=10001)

class UpdatePolicy(BaseModel):
    PolicyName: Optional[str] = Field(None, example="Premium Health Plan")

class UpdateClaim(BaseModel):
    CreatedDate: Optional[str] = Field(None, example="2024-01-01")
    CaseNumber: Optional[str] = Field(None, example="C12345")
    HAN: Optional[str] = Field(None, example="HAN001")
    BillAmount: Optional[float] = Field(None, example=5000.00)
    Status: Optional[str] = Field(None, example="Approved")
    AccountId: Optional[str] = Field(None, example="A12345")
