# transaction.py
from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from app import crud, schemas, database
from . import transaction_detail
from typing import List
from app.models import PurchaseRequest

import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)  # You can set this to DEBUG or INFO depending on your needs
logger = logging.getLogger(__name__)

router = APIRouter()

# 商品詳細登録と取引の登録
@router.post("/purchase/")
async def purchase_transaction(request: Request, db: AsyncSession = Depends(database.get_db_async)):
    request_body = await request.json()
    logger.info(f"受け取った request: {request_body}")
    logger.info(f"db のタイプ: {type(db)}")

    try:
        cart = request_body.get("cart", [])
        for item in cart:
            if "quantity" not in item:
                item["quantity"] = 1  # quantity がない場合、デフォルトで1を設定

        # 1. Transaction を TOTAL_AMT=0 で作成し、コミット
        transaction = await crud.create_transaction(db)

        # 2. TRD_ID を取得し、TransactionDetail を登録
        transaction_id = transaction.TRD_ID
        await crud.add_transaction_details(db, transaction_id, cart)

        # 3. 合計金額を計算し、Transaction を更新
        await crud.update_transaction_total(db, transaction_id)

        logger.info(f"取引が完了しました。ID: {transaction_id}")
        return {"message": "購入処理が成功しました", "transaction_id": transaction_id}

    except Exception as e:
        logger.error(f"購入処理中にエラーが発生しました: {e}")
        return {"error": "購入処理に失敗しました", "details": str(e)}

# # app/transaction.py

# from fastapi import APIRouter, Request

# router = APIRouter()

# @router.post("/purchase/")
# async def purchase_transaction(request: Request):
#     # リクエストボディを取得
#     request_body = await request.json()  # JSON形式のリクエストボディを取得
#     print("Received request body:", request_body)  # ログに出力
#     return {"message": "Request received successfully", "data": request_body}

