from sqlalchemy.orm import Session
from . import models, schemas

# 商品検索
def search_product(db: Session, product_code: str):
    return db.query(models.Product).filter(models.Product.CODE == product_code).first()

# 購入処理
def purchase(db: Session, request: schemas.PurchaseRequest):
    total_amount = 0
    transaction = models.Transaction(
        EMP_CD=request.EMP_CD,
        STORE_CD=request.STORE_CD,
        POS_NO=request.POS_NO,
        TOTAL_AMT=0  # 一旦0をセットして後で合計金額を計算
    )
    db.add(transaction)
    db.commit()
    db.refresh(transaction)

    for item in request.items:
        product = db.query(models.Product).filter(models.Product.CODE == item.PRD_CODE).first()
        if product:
            detail = models.TransactionDetail(
                TRD_ID=transaction.TRD_ID,
                DTL_ID=item.PRD_ID,  # DTL_IDは適切にインクリメントする
                PRD_ID=product.PRD_ID,
                PRD_CODE=product.CODE,
                PRD_NAME=product.NAME,
                PRD_PRICE=product.PRICE
            )
            db.add(detail)
            total_amount += product.PRICE
    
    # 取引の合計金額を更新
    transaction.TOTAL_AMT = total_amount
    db.commit()
    db.refresh(transaction)

    return schemas.TransactionResponse(TRD_ID=transaction.TRD_ID, TOTAL_AMT=total_amount)
