from sqlalchemy.orm import Session
from app.models import TransactionDetail
from fastapi import APIRouter, Depends, HTTPException

router = APIRouter()

def add_to_transaction_detail(db: Session, transaction_id: int, item: dict):
    """商品詳細をtransaction_detailに追加する"""
    transaction_detail = TransactionDetail(
        trd_id=transaction_id,
        prd_id=item['prd_id'],
        prd_code=item['prd_code'],
        prd_name=item['prd_name'],
        prd_price=item['prd_price'],
    )
    db.add(transaction_detail)
    db.commit()

def calculate_total_amount(db: Session, transaction_id: int) -> float:
    """transaction_idに基づいて合計金額を計算"""
    transaction_details = db.query(TransactionDetail).filter(models.TransactionDetail.trd_id == transaction_id).all()
    total_amount = sum(item.prd_price * item.quantity for item in transaction_details)
    return total_amount
