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

def get_usd_to_irr():
    try:
        r = requests.get("https://api.exchangerate.host/convert?from=USD&to=IRR", timeout=10)
        r.raise_for_status()
        return r.json()["result"]
    except:
        return 65000  # پیش‌فرض دلار اگر API قطع شد

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

def format_toman(v):
    return f"{int(v):,}"

def generate_message():
    crypto = get_crypto_prices()
    usd_price = get_usd_to_irr()
    now = datetime.now().strftime("%H:%M - %Y/%m/%d")

    if not crypto:
        return "❌ خطا در دریافت داده‌های رمزارز."

    msg = f"""
✨ <b>نرخ لحظه‌ای ارزهای دیجیتال</b>
📅 <i>{now}</i>
━━━━━━━━━━━━━━━━━━
💵 <b>دلار آزاد:</b> {format_toman(usd_price)} تومان
━━━━━━━━━━━━━━━━━━
🟠 BTC: ${crypto['BTC']:,} | {format_toman(crypto['BTC'] * usd_price)} تومان
🔵 ETH: ${crypto['ETH']:,} | {format_toman(crypto['ETH'] * usd_price)} تومان
💲 USDT: ${crypto['USDT']:,} | {format_toman(crypto['USDT'] * usd_price)} تومان
🐶 DOGE: ${crypto['DOGE']:,} | {format_toman(crypto['DOGE'] * usd_price)} تومان
🧬 SOL: ${crypto['SOL']:,} | {format_toman(crypto['SOL'] * usd_price)} تومان
🎯 ADA: ${crypto['ADA']:,} | {format_toman(crypto['ADA'] * usd_price)} تومان
⚡ TRX: ${crypto['TRX']:,} | {format_toman(crypto['TRX'] * usd_price)} تومان
🔷 USDC: ${crypto['USDC']:,} | {format_toman(crypto['USDC'] * usd_price)} تومان
━━━━━━━━━━━━━━━━━━
📡 @VPNByBaT
"""
    return msg

with app:
    msg = generate_message()
    app.send_photo(
        chat_id=CHANNEL_ID,
        photo="live_crypto_banner.jpg",
        caption=msg,
        parse_mode=ParseMode.HTML
    )