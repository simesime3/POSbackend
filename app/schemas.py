from pydantic import BaseModel
from typing import List, Optional

class TransactionDetailBase(BaseModel):
    PRD_CODE: str
    PRD_NAME: str
    PRD_PRICE: int

class TransactionDetail(TransactionDetailBase):
    TRD_ID: int
    DTL_ID: int
    PRD_ID: int

    class Config:
        orm_mode = True

class TransactionBase(BaseModel):
    DATETIME: str
    EMP_CD: str
    STORE_CD: str
    POS_NO: str
    TOTAL_AMT: int

class Transaction(TransactionBase):
    TRD_ID: int
    transaction_details: List[TransactionDetail]

    class Config:
        orm_mode = True

class TransactionCreate(BaseModel):
    total_amt: int  # 取引金額

    class Config:
        orm_mode = True

# 取引明細作成用スキーマ
class TransactionDetailCreate(BaseModel):
    trd_id: int
    prd_id: int
    prd_code: str
    prd_name: str
    prd_price: int

    class Config:
        orm_mode = True

class ProductBase(BaseModel):
    CODE: str
    NAME: str
    PRICE: int

class Product(ProductBase):
    PRD_ID: int
    transaction_details: List[TransactionDetail] = []

    class Config:
        orm_mode = True
        from_attributes = True