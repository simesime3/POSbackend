from sqlalchemy import Column, Integer, String, ForeignKey, CHAR, TIMESTAMP
from sqlalchemy.orm import relationship
from .database import Base
from pydantic import BaseModel
from typing import List
from .schemas import TransactionDetailCreate  # TransactionDetailCreateがschemas.pyにある場合
import logging

# 商品マスタテーブルの定義
class Product(Base):
    __tablename__ = 'products'
    
    PRD_ID = Column(Integer, primary_key=True, autoincrement=True)
    CODE = Column(CHAR(13), unique=True, nullable=False)
    NAME = Column(String(50), nullable=False)
    PRICE = Column(Integer, nullable=False)

    # 取引明細との関連を定義
    transaction_details = relationship("TransactionDetail", back_populates="product")


# ロガーを設定
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


# 取引テーブルの定義
class Transaction(Base):
    __tablename__ = 'transactions'

    TRD_ID = Column(Integer, primary_key=True, autoincrement=True)
    DATETIME = Column(TIMESTAMP, default="CURRENT_TIMESTAMP")
    EMP_CD = Column(CHAR(10), default="9999999999")
    STORE_CD = Column(CHAR(5), default="30")
    POS_NO = Column(CHAR(3), default="90")
    TOTAL_AMT = Column(Integer, default=0)

    # 取引明細との関連
    transaction_details = relationship("TransactionDetail", back_populates="transaction")

    def __init__(self, DATETIME=None, EMP_CD=None, STORE_CD=None, POS_NO=None, TOTAL_AMT=0):
        super().__init__(DATETIME=DATETIME, EMP_CD=EMP_CD, STORE_CD=STORE_CD, POS_NO=POS_NO, TOTAL_AMT=TOTAL_AMT)
        # ログの設定
        logger.info(f"新しい取引オブジェクトが作成されました: DATETIME={DATETIME}, EMP_CD={EMP_CD}, STORE_CD={STORE_CD}, POS_NO={POS_NO}, TOTAL_AMT={TOTAL_AMT}")
        
    # 取引の追加とコミット時にログを記録する関数
    def add_transaction(self, db):
        try:
            logger.info(f"取引をデータベースに追加中: {self}")
            db.add(self)  # トランザクションを追加
            db.commit()   # コミットしてデータベースに反映
            logger.info(f"取引がデータベースに追加されました: TRD_ID={self.TRD_ID}")
            db.refresh(self)  # データベースから最新の状態を反映
            logger.info(f"取引情報を再読み込みしました: TRD_ID={self.TRD_ID}")
        except Exception as e:
            logger.error(f"取引の追加中にエラーが発生しました: {e}")
            db.rollback()  # エラーが発生した場合はロールバック
            raise

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


class PurchaseRequest(BaseModel):
    cart: List[TransactionDetailCreate]  # This could be the list of items in the cart

    class Config:
        orm_mode = True