import time
import os
from binance.client import Client
from binance.exceptions import BinanceAPIException
from src.bot import obtener_datos, generar_senal
from src.utils import enviar_telegram, log
from health_server import start_health_server  # 👈 NUEVO

# 🔑 Claves desde entorno
API_KEY = 'gQ1zKIzSdnMxEF7ftfHJ9pWazTtMj5h7kRqmmxdKZdksGREBmW8XY9ePaoMQ2q2d'
API_SECRET = 'hMdv03PtaVHZpZAF0DDWRsG3Ms2hTm3NCDOpxnIAWYdAGMulXvQo0zfRxPCGFmjc'
BASE_URL = 'https://testnet.binance.vision'

# 🎯 Configuración general
SYMBOL = "BTCUSDT"
INTERVAL = "2m"
USDT_INICIAL = 20

# 🤖 Cliente de Binance
client = Client(API_KEY, API_SECRET)
client.API_URL = BASE_URL

start_health_server()  # 👈 NUEVO: Levanta el servidor HTTP

try:
    account_info = client.get_account()
    balance = account_info["balances"]
    for asset in balance:
        if asset["asset"] == "USDT":
            print(f"Saldo USDT: {asset['free']}")
except BinanceAPIException as e:
    log(f"Error al obtener el balance: {e.message}")

def ejecutar_operacion(senal):
    try:
        if senal == "compra":
            precio_actual = float(client.get_symbol_ticker(symbol=SYMBOL)["price"])
            cantidad = round(USDT_INICIAL / precio_actual, 6)
            client.order_market_buy(symbol=SYMBOL, quoteOrderQty=USDT_INICIAL)
            enviar_telegram("🟢 Compra ejecutada")
            log("✅ Orden de COMPRA ejecutada")

        elif senal == "venta":
            balance = client.get_asset_balance(asset="SOL")
            cantidad = round(float(balance["free"]), 6)
            if cantidad > 0:
                client.order_market_sell(symbol=SYMBOL, quantity=cantidad)
                enviar_telegram("🔴 Venta ejecutada")
                log("✅ Orden de VENTA ejecutada")
    except BinanceAPIException as e:
        enviar_telegram(f"⚠️ Error en la orden: {e.message}")
        log(f"❌ Error: {e.message}")

def ejecutar_bot():
    while True:
        df = obtener_datos(client, SYMBOL, INTERVAL)
        senal = generar_senal(df)
        enviar_telegram(f"Señal: {senal.upper()}")
        log(f"📊 Señal generada: {senal.upper()}")
        ejecutar_operacion(senal)
        time.sleep(120)

if __name__ == "__main__":
    ejecutar_bot()
