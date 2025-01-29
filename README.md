.
├── app/
│   ├── __init__.py
│   ├── main.py           # FastAPIのエントリーポイント
│   ├── database.py       # データベース接続の設定
│   ├── models.py         # SQLAlchemyモデル（テーブル定義）
│   ├── crud.py           # DB操作用の関数（CRUD操作）
│   ├── schemas.py        # Pydanticスキーマ（リクエスト/レスポンスのバリデーション）
│   ├── api/              # APIルート
│   │   ├── __init__.py
│   │   ├── product.py    # 商品に関連するAPI
│   │   ├── transaction.py # 取引に関連するAPI
│   ├── services/         # ビジネスロジック
│   │   ├── __init__.py
│   │   ├── product_service.py # 商品関連のビジネスロジック
│   │   ├── transaction_service.py # 取引関連のビジネスロジック
│   ├── utils/            # ユーティリティ（共通関数など）
│   │   ├── __init__.py
│   │   ├── helpers.py    # ヘルパー関数
├── requirements.txt      # 必要なライブラリ
├── .env                  # 環境変数設定（DB接続情報など）
└── alembic/              # マイグレーション用のディレクトリ（もし使う場合）
    ├── versions/         # マイグレーションファイル
    └── env.py            # alembic設定ファイル
