import requests
import os
from datetime import datetime
from pyrogram import Client
from pyrogram.enums import ParseMode

BOT_TOKEN = os.environ["BOT_TOKEN"]
API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]
CHANNEL_ID = "@VPNByBaT"

app = Client("crypto_bot", bot_token=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH)

def get_crypto_prices():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,tether,dogecoin,solana,cardano,tron,usd-coin&vs_currencies=usd"
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        data = r.json()
        return {
            "BTC": data["bitcoin"]["usd"],
            "ETH": data["ethereum"]["usd"],
            "USDT": data["tether"]["usd"],
            "DOGE": data["dogecoin"]["usd"],
            "SOL": data["solana"]["usd"],
            "ADA": data["cardano"]["usd"],
            "TRX": data["tron"]["usd"],
            "USDC": data["usd-coin"]["usd"],
        }
    except:
        return None

def generate_message():
    crypto = get_crypto_prices()
    now = datetime.now().strftime("%H:%M - %Y/%m/%d")

    if not crypto:
        return "❌ خطا در دریافت داده‌های رمزارز."

    msg = f"""
✨ <b>قیمت لحظه‌ای ارزهای دیجیتال</b>
📅 <i>{now}</i>
━━━━━━━━━━━━━━━━━━
🟠 BTC: ${crypto['BTC']:,}
🔵 ETH: ${crypto['ETH']:,}
💲 USDT: ${crypto['USDT']:,}
🐶 DOGE: ${crypto['DOGE']:,}
🧬 SOL: ${crypto['SOL']:,}
🎯 ADA: ${crypto['ADA']:,}
⚡ TRX: ${crypto['TRX']:,}
🔷 USDC: ${crypto['USDC']:,}
━━━━━━━━━━━━━━━━━━
📡 @VPNByBaT
"""
    return msg

with app:
    msg = generate_message()
    app.send_photo(
        chat_id=CHANNEL_ID,
        photo="live_crypto_banner.jpg",  # تصویر کنار فایل قرار داشته باشه
        caption=msg,
        parse_mode=ParseMode.HTML
    )