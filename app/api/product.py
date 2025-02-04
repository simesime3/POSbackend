from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database import SessionLocal
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()

# データベースセッションを取得する依存関数
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/products/{code}", response_model=schemas.Product)
def read_product(code: str, db: Session = Depends(get_db)):
    # 商品をコードで検索（同期）
    db_product = crud.get_product_by_code(db, code)
    
    # 商品が見つからない場合、404エラーを返す
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Pydanticモデルを利用してレスポンスを返す
    return schemas.Product.from_orm(db_product)

