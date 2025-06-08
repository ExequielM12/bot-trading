import pandas as pd

def calcular_sma(serie, periodo=10):
    return serie.rolling(window=periodo).mean()

def calcular_rsi(serie, periodo=14):
    delta = serie.diff()
    ganancia = delta.where(delta > 0, 0)
    perdida = -delta.where(delta < 0, 0)

    media_ganancia = ganancia.rolling(window=periodo).mean()
    media_perdida = perdida.rolling(window=periodo).mean()

    rs = media_ganancia / media_perdida
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calcular_macd(serie, rapida=12, lenta=26, señal=9):
    ema_rapida = serie.ewm(span=rapida, adjust=False).mean()
    ema_lenta = serie.ewm(span=lenta, adjust=False).mean()
    macd = ema_rapida - ema_lenta
    linea_senal = macd.ewm(span=señal, adjust=False).mean()
    histograma = macd - linea_senal
    return macd, linea_senal, histograma
