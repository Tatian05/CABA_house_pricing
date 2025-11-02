import pandas as pd
from configparser import ConfigParser
from sqlalchemy import create_engine
import os

def database_connection(conf_file_path:str, section:str, sql_driver:str):
    try:
        parser = ConfigParser()
        parser.read(conf_file_path)
        
        db={}
        if parser.has_section(section):
            params = parser.items(section)
            db = { param[0] : param[1] for param in params }
            
            engine = create_engine(f"{sql_driver}://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['dbname']}")
            return engine
        else:
            print(f"Section {section} has been not found in the config file.")
            return None
    except Exception as e:
        print(f"Error trying to connect to database: {e}")
        return None


def df_to_sql(conn, df: pd.DataFrame, schema:str, table_name:str, if_exists='fail'):
    try:
        df.to_sql(con=conn, schema=schema, name=table_name, if_exists=if_exists, index=False)
        print(f"Table '{table_name}' loaded successfully.")
    except Exception as e:
        print(f"Error saving '{table_name}' to SQL: {e}")