import os
import oracledb
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.dialects.oracle import (
    FLOAT,
)
from src.secrets import AnsibleDecoder


class DB_Connection:
    def __init__(self):
        print("Connecting to db")
        #password = os.getenv('ORACLE_PWD')
        password = AnsibleDecoder.default_config().get_secrets('db')['ORACLE_PWD']
        host='database'
        self.connection = oracledb.connect(
            user="system",
            password=password,
            dsn=f"{host}:1521/FREE")
        # create engine
        self.engine = create_engine('oracle+oracledb://', creator=lambda: self.connection)
        self.cursor = self.connection.cursor()
        print("Connected")


    def drop(self, table_name: str) -> None:
        print(f"Dropping table {table_name}")
        self.cursor.execute(f"""
            begin
                execute immediate 'drop table {table_name}';
                exception when others then if sqlcode <> -942 then raise; end if;
            end;""")

    def append_df(self, df: pd.DataFrame, table_name: str) -> None:
        print(f"Appending data to db {table_name}")
        dtype = {i: FLOAT for i in df.columns}
        # export test DataFrame with pandas to_sql
        df.to_sql(table_name, con=self.engine, if_exists='append', index=False, dtype=dtype)

    def get_df(self, table_name: str) -> pd.DataFrame:
        print(f"Get data from {table_name}")
        query = f"SELECT * FROM {table_name}"
        return pd.read_sql(query, self.engine)


if __name__ == '__main__':
    connection = DB_Connection()
    df = pd.read_csv('data/test_X.csv')
    connection.drop('test')
    connection.append_df(df, 'test')
    connection.append_df(df, 'test')
    df_get = connection.get_df('test')
    connection.drop('test')
    connection = DB_Connection()
    connection = DB_Connection()
    print(len(df), len(df_get))
