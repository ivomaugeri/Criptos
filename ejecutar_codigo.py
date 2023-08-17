import requests
import pandas as pd
from datetime import datetime, timedelta
from google.colab import files

def get_binance_historical_data(symbol, interval, start_time, end_time):
    base_url = 'https://api.binance.com/api/v3/klines'
    params = {
        'symbol': symbol,
        'interval': interval,
        'startTime': start_time,
        'endTime': end_time,
        'limit': 1000  # Número máximo de registros por solicitud
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    df = pd.DataFrame(data, columns=['Open time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close time',
                                     'Quote asset volume', 'Number of trades', 'Taker buy base asset volume',
                                     'Taker buy quote asset volume', 'Ignore'])

    # Convertir las columnas de tiempo y precios a tipos adecuados
    df['Open time'] = pd.to_datetime(df['Open time'], unit='ms')
    df['Close time'] = pd.to_datetime(df['Close time'], unit='ms')
    df[['Open', 'High', 'Low', 'Close', 'Volume', 'Quote asset volume']] = \
        df[['Open', 'High', 'Low', 'Close', 'Volume', 'Quote asset volume']].astype(float)

    return df


symbols = [
    "BTC", "XNO", "XRP", "LINK", "DOT", "UNI", "CAKE", "THETA", "GRT", "MKR", "ATOM", "MATIC",
    "FIL", "BNB", "IOTA", "ALGO", "HBAR", "NEAR", "LTC", "FTT", "AAVE", "AMP", "HNT", "TEL",
    "DAG", "SHR", "BYG", "TYC", "FTM", "LUNA", "UBI", "ADA", "QTUM", "GLMR", "ATL", "SAND",
    "MSU", "MANA", "ATLAS", "LPT", "UOS", "SOL", "OCEAN", "NOVA", "CRO", "XLM", "ICP", "KLAY",
    "EGLD", "ONE", "HAKA", "ORARE", "VET", "ROSE", "ENJ", "LRC", "CHZ", "NEXO", "KDA", "RVN",
    "ANC", "ACA", "LITH", "CHK", "PYR", "MSU", "CRPT", "EVDC", "CSPN", "ALPINE", "STREETH",
    "REQ", "BVR", "EXS", "CGG", "RAMP", "MZR", "YOM", "CQT", "HPW", "GAL", "EGO", "LIGHT",
    "PUC", "KVT", "SFUND", "rGLD", "EWT", "BITSU", "MMAPS", "GREEN", "RENS"
]

# Función para ejecutar el código y guardar los datos
def execute_code():
    # Obtener la marca de tiempo de hace 3 meses
    end_time = int(datetime.now().timestamp() * 1000)
    start_time = int((datetime.now() - timedelta(days=90)).timestamp() * 1000)

    # Crear un DataFrame vacío para almacenar los datos de todas las criptomonedas
    all_data = pd.DataFrame()

    for symbol in symbols:
        df = get_binance_historical_data(symbol + "USDT", "1d", start_time, end_time)
        df["Symbol"] = symbol  # Agregar columna para identificar la criptomoneda
        all_data = all_data.append(df)

    # Obtener la ruta del archivo CSV
    csv_file = "VolsmartICOs.csv"

    # Guardar los datos en un archivo CSV
    all_data.to_csv(csv_file, index=False)

    print(f'Datos guardados exitosamente en "{csv_file}"')

    # Descargar el archivo CSV
    files.download(csv_file)

execute_code()
