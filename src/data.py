import pandas as pd
from binance.client import Client
from src.logger import log

def obtener_datos(client: Client, symbol: str, interval: str, limit: int = 100) -> pd.DataFrame:
    log("⏳ Obteniendo datos de Binance...")
    klines = client.get_klines(symbol=symbol, interval=interval, limit=limit)
    
    df = pd.DataFrame(klines, columns=[
        'timestamp', 'open', 'high', 'low', 'close', 'volume',
        'close_time', 'quote_asset_volume', 'number_of_trades',
        'taker_buy_base_volume', 'taker_buy_quote_volume', 'ignore'
    ])
    
    df['open'] = df['open'].astype(float)
    df['high'] = df['high'].astype(float)
    df['low'] = df['low'].astype(float)
    df['close'] = df['close'].astype(float)
    df['volume'] = df['volume'].astype(float)
    
    return df
