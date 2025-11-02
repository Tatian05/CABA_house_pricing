import pandas as pd

from utils.funcs import *
from utils.dolar import valor_dolar_oficial
from utils.consts import NEIGHBORHOODS_CABA

def transformation(raw_df:pd.DataFrame):

    #Columns to lower and some renames
    raw_df = (
        raw_df
        .rename(columns=lambda x: str.lower(x))
        .rename(columns={
            "id": "flat_id",
            "location": "neighborhood",
            "expensas": "expenses",
            "scrap_date": "fetch_date"
        })
    )

    #Change date format
    raw_df["fetch_date"] = raw_df["fetch_date"].dt.strftime("%d-%m-%Y")
    
    #Remove prices and expenses without values
    indexes_to_drop = raw_df[(raw_df["price"] == "Consultar precio") | (raw_df["expenses"].isna())].index
    raw_df = raw_df.drop(indexes_to_drop).reset_index(drop=True)
    
    #Get the neighborhood
    raw_df["neighborhood"] = (
        raw_df["neighborhood"]
        .str.lower()
        .apply(lambda x: next((b for b in NEIGHBORHOODS_CABA if b in x), None))
        .str.capitalize()
    )
    raw_df = raw_df.dropna(subset="neighborhood", ignore_index=True)
    
    #Rework price and expenses columns
    buy, sell = valor_dolar_oficial()
    dolar_intermedio = (buy + sell) / 2
    
    raw_df["price"] = rework_price_and_expenses(raw_df, "price", dolar_intermedio)

    raw_df["expenses"] = rework_price_and_expenses(raw_df, "expenses", dolar_intermedio)

    #Get features from list
    raw_df["features"] = (
        raw_df["features"]
        .apply(lambda x: 
            ''.join(f"{c}-" for c in x) if isinstance(x, list) else x
        ).astype(str)
    )
    
    raw_df["m²"] = raw_df["features"].str.extract(r'(\d+)\s*m²', expand=False).astype(float).fillna(0).astype(int)
    raw_df["n_room"] = raw_df["features"].str.extract(r'(\d+)\s*amb', expand=False).astype(float).fillna(0).astype(int)
    raw_df["n_bed"] = raw_df["features"].str.extract(r'(\d+)\s*dorm', expand=False).astype(float).fillna(0).astype(int)
    raw_df["n_bath"] = raw_df["features"].str.extract(r'(\d+)\s*baño', expand=False).astype(float).fillna(0).astype(int)
    raw_df["has_park"] = raw_df["features"].str.extract(r'(\d+)\s*coch', expand=False).astype(float).fillna(0).astype(int)

    #Change colums types
    processed_df = raw_df.astype({
        "flat_id": "int",
        "neighborhood": "string",
        "address": "string",
        "description": "string",
        "link": "string",
        "type_operation": "string"
    })

    #Reorder columns
    processed_df = processed_df[["flat_id", "price", "expenses", "neighborhood", "address", "features",
                        "description", "fetch_date", "type_operation", "m²", "n_room", "n_bed", "n_bath",
                        "has_park"]]
    
    #--- Remove outliers ---
    alquileres_df = remove_outliers(processed_df[processed_df["type_operation"] == "alquiler"], "price")
    ventas_df = remove_outliers(processed_df[processed_df["type_operation"] == "venta"], "price")
    
    processed_df = pd.concat([alquileres_df, ventas_df], ignore_index=True)
    
    print("Data transformed successfully.")
    return processed_df