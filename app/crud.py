from sqlalchemy.orm import Session
from .models import Product, Transaction, TransactionDetail

# 商品を追加する
def create_product(db: Session, code: str, name: str, price: int):
    db_product = Product(CODE=code, NAME=name, PRICE=price)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

# 取引を追加する
def create_transaction(db: Session, total_amt: int):
    db_transaction = Transaction(TOTAL_AMT=total_amt)
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

# 取引明細を追加する
def create_transaction_detail(db: Session, trd_id: int, prd_id: int, prd_code: str, prd_name: str, prd_price: int):
    db_transaction_detail = TransactionDetail(TRD_ID=trd_id, PRD_ID=prd_id, PRD_CODE=prd_code, PRD_NAME=prd_name, PRD_PRICE=prd_price)
    db.add(db_transaction_detail)
    db.commit()
    db.refresh(db_transaction_detail)
    return db_transaction_detail

# 商品コードに一致する商品を取得
def get_product_by_code(db: Session, code: str):
    return db.query(Product).filter(Product.CODE == code).first()

# 取引IDで取引を検索
def get_transaction_by_id(db: Session, trd_id: int):
    return db.query(Transaction).filter(Transaction.TRD_ID == trd_id).first()