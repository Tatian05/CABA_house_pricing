import pandas as pd
import sys, os

from storage import *
from utils.consts import NEIGHBORHOODS_CABA

def normalization(df: pd.DataFrame):
    dim_operations = (
        df[["type_operation"]]
        .drop_duplicates()
        .reset_index(drop=True)
        .reset_index(names="type_operation_id")
    )
    
    dim_operations["type_operation_id"] += 1

    #------

    dim_neighborhoods = pd.DataFrame(NEIGHBORHOODS_CABA, columns=["neighborhood"])
    dim_neighborhoods["neighborhood"] = dim_neighborhoods["neighborhood"].str.capitalize()
    dim_neighborhoods["neighborhood_id"] = pd.Series(range(1, len(dim_neighborhoods) + 1)).astype(int)
    
    #------

    dim_departments = df[["flat_id", "neighborhood", "address", "description", "m²",
                          "n_room", "n_bed", "n_bath", "has_park"]]
    dim_departments = (
        dim_departments
        .drop_duplicates("flat_id")
        .reset_index(drop=True)
    )
    
    dim_departments["neighborhood"] = (
        dim_departments
        .merge(dim_neighborhoods, on="neighborhood", how="left")["neighborhood_id"]
        .astype(int)
    )
    
    dim_departments = dim_departments.rename(columns={"neighborhood": "neighborhood_id"})

    #------

    fact_prices = df[["flat_id", "type_operation", "price", "expenses", "fetch_date"]]
    fact_prices["type_operation"] = (
        fact_prices
        .merge(dim_operations, on="type_operation", how="left")["type_operation_id"]
        .astype(int)
    )
    
    fact_prices = (
        fact_prices
        .rename(columns={
            "type_operation": "type_operation_id"
        })
        .reset_index(drop=True)
        .reset_index(names="publication_id")
    )
    
    #---- SQL Connection
    
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(base_dir, "../dbconfig.conf")
        
        engine = database_connection(config_path, "database", "postgresql+psycopg2")
    
        with engine.connect() as conn:
            df_to_sql(conn=conn, df=dim_operations, schema="caba_house_pricing", table_name="dim_operations")
            df_to_sql(conn=conn, df=dim_neighborhoods, schema="caba_house_pricing", table_name="dim_neighborhoods")
            df_to_sql(conn=conn, df=dim_departments, schema="caba_house_pricing", table_name="dim_departments", if_exists='replace')
            df_to_sql(conn=conn, df=fact_prices, schema="caba_house_pricing", table_name="fact_prices", if_exists='replace')
    except Exception as e:
        print(f"Error loading data to database: {e}")