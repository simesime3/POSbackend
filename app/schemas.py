from pydantic import BaseModel
from typing import List

# 商品詳細基底クラス
class TransactionDetailBase(BaseModel):
    PRD_CODE: str
    PRD_NAME: str
    PRD_PRICE: int

# 商品詳細（取引に紐づく詳細情報）
class TransactionDetail(TransactionDetailBase):
    TRD_ID: int
    DTL_ID: int
    PRD_ID: int

    class Config:
        orm_mode = True

# 商品詳細作成用スキーマ（取引詳細を作成するため）
class TransactionDetailCreate(BaseModel):
    PRD_ID: int
    PRD_CODE: str
    PRD_NAME: str
    PRD_PRICE: int

    class Config:
        orm_mode = True

# 取引（取引全体）の基底クラス
class TransactionBase(BaseModel):
    DATETIME: str
    EMP_CD: str
    STORE_CD: str
    POS_NO: str
    TOTAL_AMT: int

# 取引モデル（取引全体と取引詳細の関連）
class Transaction(TransactionBase):
    TRD_ID: int
    transaction_details: List[TransactionDetail]  # 取引詳細のリスト

    class Config:
        orm_mode = True

# 取引作成用スキーマ
class TransactionCreate(BaseModel):
    total_amt: int  # 取引金額

    class Config:
        orm_mode = True

# 商品（商品情報）
class ProductBase(BaseModel):
    CODE: str
    NAME: str
    PRICE: int

# 商品モデル（商品詳細情報）
class Product(ProductBase):
    PRD_ID: int
    # transaction_details: List[TransactionDetail] = []  # この商品に紐づく取引詳細のリスト

    class Config:
        orm_mode = True
        from_attributes = True