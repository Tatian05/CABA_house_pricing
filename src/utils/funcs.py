import pandas as pd

def remove_outliers(df:pd.DataFrame, col:str):
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1

    # Límites para detectar outliers
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    # Filas con outliers
    outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)].index
    return df.drop(outliers).reset_index(drop=True)

def rework_price_and_expenses(df: pd.DataFrame, col:str, dolar_value):  
    prices_usd = df[df[col].str.contains("USD", na=False)].index
    
    df[col] = (
        df[col]
        .str.replace(r'[^0-9]', '', regex=True)
        .str.strip()
        .astype(int)
    )
    
    df.loc[prices_usd, col] = df.loc[prices_usd, col] * dolar_value
    
    return df[col]