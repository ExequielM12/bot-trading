import pandas as pd
from src.indicators import calcular_rsi, calcular_macd, calcular_sma
from src.utils import log, enviar_telegram
from binance.exceptions import BinanceAPIException

# 📥 Obtener datos de mercado
def obtener_datos(client, symbol, interval):
    try:
        klines = client.get_klines(symbol=symbol, interval=interval, limit=100)
        
        # Validar que klines tiene datos
        if not klines or not isinstance(klines, list):
            raise ValueError("Respuesta vacía o inválida de Binance")

        df = pd.DataFrame(klines, columns=[
            "timestamp", "open", "high", "low", "close", "volume",
            "close_time", "quote_asset_volume", "number_of_trades",
            "taker_buy_base", "taker_buy_quote", "ignore"
        ])
        df["close"] = pd.to_numeric(df["close"])
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
        df.set_index("timestamp", inplace=True)

        # Agregamos los indicadores
        df["sma"] = calcular_sma(df["close"], periodo=10)
        df["rsi"] = calcular_rsi(df["close"], period=14)
        df["macd"], df["signal"] = calcular_macd(df["close"])

        return df.dropna()

    except BinanceAPIException as e:
        mensaje = f"⚠️ Binance API error: {e.message}"
        log(mensaje)
        enviar_telegram(mensaje)
    except ValueError as e:
        mensaje = f"⚠️ Error de datos: {str(e)}"
        log(mensaje)
        enviar_telegram(mensaje)
    except Exception as e:
        mensaje = f"⚠️ Excepción inesperada: {str(e)}"
        log(mensaje)
        enviar_telegram(mensaje)

    # En todos los casos de error, devolver DataFrame vacío
    return pd.DataFrame()

# 📊 Generar señal con múltiples indicadores
def generar_senal(df):
    if df.empty or len(df) < 2:
        return "esperar"

    ultima = df.iloc[-1]
    anterior = df.iloc[-2]

    compra = (
        ultima["macd"] > ultima["signal"] and
        anterior["macd"] <= anterior["signal"] and
        ultima["rsi"] < 70 and
        ultima["close"] > ultima["sma"]
    )

    venta = (
        ultima["macd"] < ultima["signal"] and
        anterior["macd"] >= anterior["signal"] and
        ultima["rsi"] > 30 and
        ultima["close"] < ultima["sma"]
    )

    if compra:
        return "compra"
    elif venta:
        return "venta"
    else:
        return "esperar"
