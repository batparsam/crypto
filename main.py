import requests
import os
from datetime import datetime
from pyrogram import Client

BOT_TOKEN = os.environ["BOT_TOKEN"]
API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]
CHANNEL_ID = os.environ["CHANNEL_ID"]  # مثلاً: -1001234567890

app = Client("crypto_bot", bot_token=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH)

def get_crypto_prices():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,toncoin,tether,dogecoin,solana,cardano,tron,usd-coin&vs_currencies=usd,irr"
    r = requests.get(url)
    if r.status_code != 200:
        return None
    data = r.json()
    return {
        "BTC_USD": data["bitcoin"]["usd"],
        "ETH_USD": data["ethereum"]["usd"],
        "TON_USD": data["toncoin"]["usd"],
        "USDT_USD": data["tether"]["usd"],
        "DOGE_USD": data["dogecoin"]["usd"],
        "SOL_USD": data["solana"]["usd"],
        "ADA_USD": data["cardano"]["usd"],
        "TRX_USD": data["tron"]["usd"],
        "USDC_USD": data["usd-coin"]["usd"],
        "BTC_IRR": data["bitcoin"].get("irr"),
        "ETH_IRR": data["ethereum"].get("irr"),
        "TON_IRR": data["toncoin"].get("irr"),
        "USDT_IRR": data["tether"].get("irr")
    }

def get_iran_prices():
    r = requests.get("https://api.tgju.org/v1/price/latest")
    if r.status_code != 200:
        return None
    data = r.json()["data"]
    return {
        "USD": int(data["price_dollar_rl"]["p"]),
        "Gold": int(data["geram18"]["p"]),
        "Coin": int(data["sekeb"]["p"]),
        "Euro": int(data["price_eur"]["p"]),
        "Ounce": int(data["ons"]["p"]),
        "Gold_Meson": int(data["mesghal"]["p"])
    }

def generate_message():
    crypto = get_crypto_prices()
    rial = get_iran_prices()
    now = datetime.now().strftime("%H:%M - %Y/%m/%d")

    if not crypto or not rial:
        return "❌ خطا در دریافت داده‌ها. لطفاً بعداً تلاش کنید."

    return f"""
✨ <b>گزارش لحظه‌ای بازار ارز و طلا</b>
📅 <i>{now}</i>
━━━━━━━━━━━━━━━━━━
<b>💵 بازار ایران:</b>
💰 دلار آزاد: {rial['USD']:,} تومان
💶 یورو: {rial['Euro']:,} تومان
🥇 طلای ۱۸ عیار: {rial['Gold']:,} تومان
📏 انس جهانی طلا: {rial['Ounce']:,} دلار
💠 هر مثقال طلا: {rial['Gold_Meson']:,} تومان
🪙 سکه امامی: {rial['Coin']:,} تومان
━━━━━━━━━━━━━━━━━━
<b>🌐 رمزارزها:</b>
🟠 BTC: ${crypto['BTC_USD']:,} | {crypto['BTC_IRR'] or 'نامشخص'} تومان
🔵 ETH: ${crypto['ETH_USD']:,} | {crypto['ETH_IRR'] or 'نامشخص'} تومان
🟢 TON: ${crypto['TON_USD']:,} | {crypto['TON_IRR'] or 'نامشخص'} تومان
💲 USDT: ${crypto['USDT_USD']:,} | {crypto['USDT_IRR'] or 'نامشخص'} تومان
🐶 DOGE: ${crypto['DOGE_USD']:,}
🧬 SOL: ${crypto['SOL_USD']:,}
🎯 ADA: ${crypto['ADA_USD']:,}
⚡ TRX: ${crypto['TRX_USD']:,}
🔷 USDC: ${crypto['USDC_USD']:,}
━━━━━━━━━━━━━━━━━━
📡 @VPNByBaT
"""

with app:
    msg = generate_message()
    app.send_photo(
        chat_id=CHANNEL_ID,
        photo="live_crypto_banner.jpg",  # عکس رو کنار main.py بزار
        caption=msg,
        parse_mode="html"
    )
