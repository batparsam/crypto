import requests
import os
from datetime import datetime
from pyrogram import Client

# 🛡 مقادیر از Secrets خوانده می‌شن
BOT_TOKEN = os.environ["BOT_TOKEN"]
API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]

# 📡 کانال مستقیم
CHANNEL_ID = "@VPNByBaT"

app = Client("crypto_bot", bot_token=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH)

def get_crypto_prices():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,tether,dogecoin,solana,cardano,tron,usd-coin&vs_currencies=usd,irr"
    r = requests.get(url)
    if r.status_code != 200:
        return None
    data = r.json()
    return {
        "BTC_USD": data.get("bitcoin", {}).get("usd"),
        "ETH_USD": data.get("ethereum", {}).get("usd"),
        "USDT_USD": data.get("tether", {}).get("usd"),
        "DOGE_USD": data.get("dogecoin", {}).get("usd"),
        "SOL_USD": data.get("solana", {}).get("usd"),
        "ADA_USD": data.get("cardano", {}).get("usd"),
        "TRX_USD": data.get("tron", {}).get("usd"),
        "USDC_USD": data.get("usd-coin", {}).get("usd"),
        "BTC_IRR": data.get("bitcoin", {}).get("irr"),
        "ETH_IRR": data.get("ethereum", {}).get("irr"),
        "USDT_IRR": data.get("tether", {}).get("irr"),
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
        photo="live_crypto_banner.jpg",  # عکس باید کنار main.py باشه
        caption=msg,
        parse_mode="html"
    )