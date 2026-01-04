import requests, time

def whale_rotation():
    print("Base — Whale Rotation (same whale buys new token after selling old)")
    whale_trades = {}  # wallet → last sold token pair

    while True:
        try:
            r = requests.get("https://api.dexscreener.com/latest/dex/transactions/base?limit=400")
            for tx in r.json().get("transactions", []):
                if tx.get("valueUSD", 0) < 100_000: continue

                wallet = tx["from"].lower()
                pair = tx["pairAddress"]
                side = tx["side"]

                if wallet not in whale_trades:
                    whale_trades[wallet] = None

                if side == "sell":
                    whale_trades[wallet] = pair
                elif side == "buy" and whale_trades[wallet] and whale_trades[wallet] != pair:
                    old_token = "unknown"
                    new_token = tx["token0"]["symbol"] if "WETH" in tx["token1"]["symbol"] else tx["token1"]["symbol"]
                    print(f"WHALE ROTATION\n"
                          f"Wallet {wallet[:10]}... rotated\n"
                          f"Into: {new_token}\n"
                          f"USD: ${tx['valueUSD']:,.0f}\n"
                          f"https://dexscreener.com/base/{pair}\n"
                          f"https://basescan.org/address/{wallet}\n"
                          f"→ Smart money moved — follow or fade\n"
                          f"{'ROTATION'*20}")
                    whale_trades[wallet] = pair

        except:
            pass
        time.sleep(1.8)

if __name__ == "__main__":
    whale_rotation()
