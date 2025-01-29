import mysql.connector
from mysql.connector import Error

# MySQLデータベース接続情報
host = "localhost"  # データベースホスト
user = "root"       # MySQLのユーザー名
password = ""  # MySQLのパスワード
database = "pos_app"  # 使用するデータベース名

# テーブル作成SQL
create_tables_query = """
-- 商品マスタテーブルの作成
CREATE TABLE IF NOT EXISTS products (
    PRD_ID INT AUTO_INCREMENT PRIMARY KEY,
    CODE CHAR(13) NOT NULL UNIQUE,
    NAME VARCHAR(50) NOT NULL,
    PRICE INT NOT NULL
);

-- 取引テーブルの作成
CREATE TABLE IF NOT EXISTS transactions (
    TRD_ID INT AUTO_INCREMENT PRIMARY KEY,
    DATETIME TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    EMP_CD CHAR(10) DEFAULT '9999999999',
    STORE_CD CHAR(5) DEFAULT '30',
    POS_NO CHAR(3) DEFAULT '90',
    TOTAL_AMT INT NOT NULL
);

-- 取引明細テーブルの作成
CREATE TABLE IF NOT EXISTS transaction_details (
    TRD_ID INT,
    DTL_ID INT AUTO_INCREMENT PRIMARY KEY,
    PRD_ID INT,
    PRD_CODE CHAR(13),
    PRD_NAME VARCHAR(50),
    PRD_PRICE INT,
    FOREIGN KEY (TRD_ID) REFERENCES transactions(TRD_ID),
    FOREIGN KEY (PRD_ID) REFERENCES products(PRD_ID)
);
"""

# データベースに接続してテーブルを作成する関数
def create_tables():
    try:
        # MySQLに接続
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )

        if connection.is_connected():
            cursor = connection.cursor()
            # テーブル作成クエリを実行
            cursor.execute(create_tables_query)
            connection.commit()
            print("テーブルが正常に作成されました。")

    except Error as e:
        print(f"エラーが発生しました: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    create_tables()
