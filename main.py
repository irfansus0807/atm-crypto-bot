import time
import hmac
import hashlib
import requests
import json

# === GANTI DENGAN API KAMU SENDIRI ===
API_KEY = "bg_7031191f849adbd78a97d1aa93ec1fb2"
API_SECRET = "186c9367156e3c114b5777c7198742d657d93cdb0b50807b94bdb5d9d549311a"

BASE_URL = "https://api.bitget.com"

def get_signature(timestamp, method, request_path, body=""):
    message = f"{timestamp}{method}{request_path}{body}"
    signature = hmac.new(API_SECRET.encode(), message.encode(), hashlib.sha256).hexdigest()
    return signature

def send_signed_request(method, endpoint, params=None, data=None):
    timestamp = str(int(time.time() * 1000))
    request_path = endpoint
    body = json.dumps(data) if data else ""
    signature = get_signature(timestamp, method, request_path, body)

    headers = {
        "ACCESS-KEY": API_KEY,
        "ACCESS-SIGN": signature,
        "ACCESS-TIMESTAMP": timestamp,
        "Content-Type": "application/json"
    }

    url = BASE_URL + endpoint
    response = requests.request(method, url, headers=headers, params=params, data=body)
    return response.json()

def check_futures_balance():
    endpoint = "/api/mix/v1/account/account?productType=USDT-FUTURES"
    result = send_signed_request("GET", endpoint)
    return result

def start_strategy():
    print("📈 Menjalankan strategi Supreme ATM Crypto...")
    balance = check_futures_balance()
    print("💰 Saldo akun Futures kamu:")
    print(json.dumps(balance, indent=4))

if __name__ == "__main__":
    while True:
        start_strategy()
        print("🔁 Update berikutnya dalam 5 menit...")
        time.sleep(300)  # setiap 5 menit
