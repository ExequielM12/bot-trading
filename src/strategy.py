def generar_senal(df):
    ultima = df.iloc[-1]
    
    if (
        ultima['rsi'] < 30
        and ultima['macd'] > ultima['macd_signal']
        and ultima['close'] > ultima['sma']
    ):
        return "compra"
    
    elif (
        ultima['rsi'] > 70
        and ultima['macd'] < ultima['macd_signal']
        and ultima['close'] < ultima['sma']
    ):
        return "venta"
    
    else:
        return "mantener"
