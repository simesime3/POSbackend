from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app import models, schemas ,database
from app.models import Product
from datetime import datetime
from sqlalchemy.future import select
import logging

# 非同期セッションで商品を取得
# 商品コードに一致する商品を取得
def get_product_by_code(db: Session, code: str):
    return db.query(Product).filter(Product.CODE == code).first()

# ロガーを設定
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# 商品を追加する
def create_product(db: Session, code: str, name: str, price: int):
    db_product = Product(CODE=code, NAME=name, PRICE=price)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

# 取引履歴を取得
def get_transactions(db: Session, limit: int = 10):
    return db.query(Transaction).order_by(Transaction.DATETIME.desc()).limit(limit).all()


# 取引明細を追加する
def create_transaction_details(db: Session, trd_id: int, cart: list[schemas.TransactionDetailCreate]):
    """TransactionDetailを追加する"""
    try:
        for item in cart:
            transaction_detail = models.TransactionDetail(
                TRD_ID=trd_id,
                PRD_ID=item.PRD_ID,
                PRD_CODE=item.PRD_CODE,
                PRD_NAME=item.PRD_NAME,
                PRD_PRICE=item.PRD_PRICE,
                quantity=item.quantity,
            )
            db.add(transaction_detail)
        db.commit()  # 非同期セッションの場合は同期的にcommit
    except Exception as e:
        db.rollback()  # 同様に同期的にrollback
        logger.error(f"TransactionDetailの作成に失敗しました: {e}")
        raise HTTPException(status_code=500, detail=f"TransactionDetail作成に失敗しました: {str(e)}")


async def create_transaction(db: AsyncSession) -> models.Transaction:
    """TransactionをTOTAL_AMT=0で作成し、コミット"""
    try:
        transaction = models.Transaction(
            DATETIME=datetime.utcnow(),
            EMP_CD="9999999999",
            STORE_CD="30",
            POS_NO="90",
            TOTAL_AMT=0,
        )
        logger.info(f"作成直後の transaction の型: {type(transaction)}")  # 追加

        db.add(transaction)
        await db.commit()
        logger.info("✅ トランザクションのコミット完了")

        # ここでエラーが発生していないか確認
        await db.refresh(transaction)
        logger.info("✅ トランザクションの refresh 完了")


        logger.info(f"refresh 後の transaction の型: {type(transaction)}")  # 追加

        if not isinstance(transaction, models.Transaction):
            raise TypeError(f"作成された transaction が正しい型ではありません: {type(transaction)}")
    
        return transaction

    except Exception as e:
        await db.rollback()
        logger.error(f"Transactionの作成に失敗しました: {e}")
        raise HTTPException(status_code=500, detail=f"Transaction作成に失敗しました: {str(e)}")



async def add_transaction_details(db: AsyncSession, transaction_id: int, cart: list):
    for item in cart:
        # quantity を取得
        quantity = item.get("quantity", 1)
        
        # quantity 分だけ TransactionDetail を繰り返し作成
        for _ in range(quantity):
            transaction_detail = models.TransactionDetail(
                TRD_ID=transaction_id,
                PRD_ID=item["PRD_ID"],
                PRD_CODE=item["PRD_CODE"],
                PRD_NAME=item["PRD_NAME"],
                PRD_PRICE=item["PRD_PRICE"]
            )
            db.add(transaction_detail)
    
    # すべての TransactionDetail を一度にコミット
    await db.commit()


async def update_transaction_total(db: AsyncSession, trd_id: int):
    """TransactionのTOTAL_AMTを更新する"""
    try:
        result = await db.execute(
            select(models.TransactionDetail).filter(models.TransactionDetail.TRD_ID == trd_id)
        )
        details = result.scalars().all()
        
        # 商品価格の合計を計算
        total_amount = sum(d.PRD_PRICE for d in details)
        logger.info(f"total_amount : {total_amount}")
        
        # トランザクション情報を取得
        transaction = await db.get(models.Transaction, trd_id)
        if not transaction:
            raise HTTPException(status_code=404, detail="Transactionが見つかりません")
        
        # TOTAL_AMTを更新
        transaction.TOTAL_AMT = total_amount
        await db.commit()
        await db.refresh(transaction)
    except Exception as e:
        await db.rollback()
        logger.error(f"TOTAL_AMTの更新に失敗しました: {e}")
        raise HTTPException(status_code=500, detail=f"TOTAL_AMT更新に失敗しました: {str(e)}")
