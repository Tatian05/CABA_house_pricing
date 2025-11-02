import kagglehub
import pandas as pd

def ingesta() -> pd.DataFrame:
    try:
        path = kagglehub.dataset_download("martinbasualdo/property-prices-in-caba-zonaprop-data")

        #alquileres
        df_alquileres = pd.read_pickle(f"{path}/alquiler_departamentos_consolidado.pkl")
        
        #ventas
        df_ventas = pd.read_pickle(f"{path}/venta_departamentos_consolidado.pkl")

        df = pd.concat([df_alquileres, df_ventas], ignore_index=True)

        print("Datos extraídos correctamente.")
        return df
    except Exception as e:
        print(f"Error al intentar extraer los datos de la fuente: {e}")
        return None