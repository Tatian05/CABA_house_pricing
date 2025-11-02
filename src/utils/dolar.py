import requests

def valor_dolar_oficial():
    url = "https://dolarapi.com/v1/dolares/oficial"

    try:
        res = requests.get(url).json()

        print("Oficial dolar extracted successfully.")
        return [res["compra"], res["venta"]]
    except Exception as e:
        print(f"Error requesting the API: {e}")
        return None
