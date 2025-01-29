from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import crud, schemas, database

router = APIRouter()

# 取引の作成
@router.post("/transactions/")
def create_transaction(transaction: schemas.TransactionCreate, db: Session = Depends(database.get_db)):
    # トランザクション作成の処理
    db_transaction = models.Transaction(**transaction.dict())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

# 取引明細の作成
@router.post("/transaction-details/", response_model=schemas.TransactionDetail)
def create_transaction_detail(transaction_detail: schemas.TransactionDetailCreate, db: Session = Depends(database.get_db)):
    return crud.create_transaction_detail(db, transaction_detail.trd_id, transaction_detail.prd_id, transaction_detail.prd_code, transaction_detail.prd_name, transaction_detail.prd_price)
