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
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,tether,dogecoin,solana,cardano,tron,usd-coin&vs_currencies=usd,irr"
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
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
    except Exception as e:
        return None

def generate_message():
    crypto = get_crypto_prices()
    now = datetime.now().strftime("%H:%M - %Y/%m/%d")

    if not crypto:
        return "❌ خطا در دریافت داده‌ها از منبع رمزارزها."

    return f"""
✨ <b>نرخ لحظه‌ای ارزهای دیجیتال</b>
📅 <i>{now}</i>
━━━━━━━━━━━━━━━━━━
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
        photo="live_crypto_banner.jpg",
        caption=msg,
        parse_mode=ParseMode.HTML
    )