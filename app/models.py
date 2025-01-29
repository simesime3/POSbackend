from sqlalchemy import Column, Integer, String, ForeignKey, CHAR, TIMESTAMP
from sqlalchemy.orm import relationship
from .database import Base

# 商品マスタテーブルの定義
class Product(Base):
    __tablename__ = 'products'
    
    PRD_ID = Column(Integer, primary_key=True, autoincrement=True)
    CODE = Column(CHAR(13), unique=True, nullable=False)
    NAME = Column(String(50), nullable=False)
    PRICE = Column(Integer, nullable=False)

    # 取引明細との関連を定義
    transaction_details = relationship("TransactionDetail", back_populates="product")

# 取引テーブルの定義
class Transaction(Base):
    __tablename__ = 'transactions'
    
    TRD_ID = Column(Integer, primary_key=True, autoincrement=True)
    DATETIME = Column(TIMESTAMP, default="CURRENT_TIMESTAMP")
    EMP_CD = Column(CHAR(10), default="9999999999")
    STORE_CD = Column(CHAR(5), default="30")
    POS_NO = Column(CHAR(3), default="90")
    TOTAL_AMT = Column(Integer, nullable=False)

    # 取引明細との関連を定義
    transaction_details = relationship("TransactionDetail", back_populates="transaction")

# 取引明細テーブルの定義
class TransactionDetail(Base):
    __tablename__ = 'transaction_details'
    
    TRD_ID = Column(Integer, ForeignKey('transactions.TRD_ID'), primary_key=True)
    DTL_ID = Column(Integer, primary_key=True, autoincrement=True)
    PRD_ID = Column(Integer, ForeignKey('products.PRD_ID'))
    PRD_CODE = Column(CHAR(13))
    PRD_NAME = Column(String(50))
    PRD_PRICE = Column(Integer)

    # 関連するテーブルとの関係
    transaction = relationship("Transaction", back_populates="transaction_details")
    product = relationship("Product", back_populates="transaction_details")
