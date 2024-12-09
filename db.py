import psycopg2
import pandas as pd
class Database():
    def __init__(self):
        #데이터베이스 연결
        self.db=psycopg2.connect(
            host='56.155.9.34',
            user='postgres',
            password='0714',
            port=5432,
            database='card'
            )

        self.cursor=self.db.cursor()
    def __del__(self):
        self.db.close()
        self.cursor.close()
        

    def execute(self,query,args={}):
        self.cursor.execute(query,args)
        #결과 가져오기
        data = self.cursor.fetchall()
        columns = [desc[0] for desc in self.cursor.description]

        return pd.DataFrame(data, columns=columns)

    def commit(self):
        self.db.commit()

Category=Database()
Category_df = Category.execute("SELECT * FROM Category;")

CardInfo=Database()
CardInfo_df = CardInfo.execute("SELECT * FROM CardInfo;")

Benefit=Database()
Benefit_df = Benefit.execute("SELECT * FROM Benefit;")
