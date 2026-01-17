import os

import requests
from dotenv import load_dotenv
import yfinance as yf
import pandas as pd
from datetime import datetime

load_dotenv()
import json

all_nasdaq_100_symbols = [
    "NVDA",
    "MSFT",
    "AAPL",
    "GOOG",
    "GOOGL",
    "AMZN",
    "META",
    "AVGO",
    "TSLA",
    "NFLX",
    "PLTR",
    "COST",
    "ASML",
    "AMD",
    "CSCO",
    "AZN",
    "TMUS",
    "MU",
    "LIN",
    "PEP",
    "SHOP",
    "APP",
    "INTU",
    "AMAT",
    "LRCX",
    "PDD",
    "QCOM",
    "ARM",
    "INTC",
    "BKNG",
    "AMGN",
    "TXN",
    "ISRG",
    "GILD",
    "KLAC",
    "PANW",
    "ADBE",
    "HON",
    "CRWD",
    "CEG",
    "ADI",
    "ADP",
    "DASH",
    "CMCSA",
    "VRTX",
    "MELI",
    "SBUX",
    "CDNS",
    "ORLY",
    "SNPS",
    "MSTR",
    "MDLZ",
    "ABNB",
    "MRVL",
    "CTAS",
    "TRI",
    "MAR",
    "MNST",
    "CSX",
    "ADSK",
    "PYPL",
    "FTNT",
    "AEP",
    "WDAY",
    "REGN",
    "ROP",
    "NXPI",
    "DDOG",
    "AXON",
    "ROST",
    "IDXX",
    "EA",
    "PCAR",
    "FAST",
    "EXC",
    "TTWO",
    "XEL",
    "ZS",
    "PAYX",
    "WBD",
    "BKR",
    "CPRT",
    "CCEP",
    "FANG",
    "TEAM",
    "CHTR",
    "KDP",
    "MCHP",
    "GEHC",
    "VRSK",
    "CTSH",
    "CSGP",
    "KHC",
    "ODFL",
    "DXCM",
    "TTD",
    "ON",
    "BIIB",
    "LULU",
    "CDW",
    "GFS",
]

AV_KEY = os.getenv("ALPHAADVANTAGE_API_KEY")

def update_json(data: dict, SYMBOL: str):
    file_path = f'./daily_prices_{SYMBOL}.json'
    
    try:
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                old_data = json.load(f)
            
            # 合并新旧的"Time Series (60min)"，新data优先（相同时间戳用新数据覆盖）
            old_ts = old_data.get("Time Series (60min)", {})
            new_ts = data.get("Time Series (60min)", {})
            merged_ts = {**old_ts, **new_ts}  # 新数据覆盖旧数据中相同的时间戳
            
            # 创建新的数据字典，避免直接修改传入的data
            merged_data = data.copy()
            merged_data["Time Series (60min)"] = merged_ts
            
            # 如果新数据没有Meta Data，保留旧的Meta Data
            if "Meta Data" not in merged_data and "Meta Data" in old_data:
                merged_data["Meta Data"] = old_data["Meta Data"]
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(merged_data, f, ensure_ascii=False, indent=4)
        else:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        
        # QQQ 特殊处理：同时保存到另一个文件
        if SYMBOL == "QQQ":
            file_path_qqq = f'./Adaily_prices_{SYMBOL}.json'
            if os.path.exists(file_path_qqq):
                with open(file_path_qqq, 'r', encoding='utf-8') as f:
                    old_data = json.load(f)
                old_ts = old_data.get("Time Series (60min)", {})
                new_ts = data.get("Time Series (60min)", {})
                merged_ts = {**old_ts, **new_ts}
                merged_data = data.copy()
                merged_data["Time Series (60min)"] = merged_ts
                if "Meta Data" not in merged_data and "Meta Data" in old_data:
                    merged_data["Meta Data"] = old_data["Meta Data"]
                with open(file_path_qqq, 'w', encoding='utf-8') as f:
                    json.dump(merged_data, f, ensure_ascii=False, indent=4)
            else:
                with open(file_path_qqq, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)
                    
    except (IOError, json.JSONDecodeError, KeyError) as e:
        print(f"Error when update {SYMBOL}: {e}")
        raise
         

def get_daily_price_av(SYMBOL: str):
    FUNCTION = "TIME_SERIES_DAILY"
    OUTPUTSIZE = "full"
    APIKEY = AV_KEY
    url = (
        f"https://www.alphavantage.co/query?function={FUNCTION}&symbol={SYMBOL}&outputsize={OUTPUTSIZE}&apikey={APIKEY}"
    )
    r = requests.get(url)
    data = r.json()
    print(data)
    if data.get("Note") is not None or data.get("Information") is not None:
        print(f"Error")
        return
    update_json(data, SYMBOL)


def get_daily_price_yf(SYMBOL: str):

    print(f"Fetching data for {SYMBOL} using yfinance...")
    
    # Fetch data
    ticker = yf.Ticker(SYMBOL)
    # Get sufficient history to match "compact" (100 data points) or slightly more. 
    # AlphaVantage compact is 100 data points. 6mo is usually sufficient for 100 trading days (~21 days/mo * 6 = 126).
    hist = ticker.history(period="6mo")
    
    # Check if empty
    if hist.empty:
        print(f"Error: No data found for {SYMBOL}")
        return

    # Take the last 100 records to match Alpha Vantage 'compact' behavior roughly, or just keep all.
    # The requirement is "output format... should be same". AV creates a JSON with "Meta Data" and "Time Series (Daily)".
    # We will format the last 100 (or all provided by 6mo) to be safe.
    # Let's stick to last 100 to be closest to 'compact'.
    hist = hist.tail(100)
    
    # Sort descending by date (AV format usually has latest first in key enumeration, though JSON is unordered, 
    # but AV users often expect it).
    # Actually AV JSON keys are dates.
    # Reverse to process latest first if we want to construct 'last refreshed' easily.
    hist = hist.sort_index(ascending=False)
    
    last_refreshed = hist.index[0].strftime('%Y-%m-%d')
    
    # Construct Meta Data
    meta_data = {
        "1. Information": "Daily Prices (open, high, low, close) and Volumes",
        "2. Symbol": SYMBOL,
        "3. Last Refreshed": last_refreshed,
        "4. Output Size": "Compact",
        "5. Time Zone": "US/Eastern" # yfinance usually converts to local or UTC, but stock market is US/Eastern.
    }
    
    # Construct Time Series
    time_series = {}
    for index, row in hist.iterrows():
        date_str = index.strftime('%Y-%m-%d')
        time_series[date_str] = {
            "1. open": f"{row['Open']:.4f}",
            "2. high": f"{row['High']:.4f}",
            "3. low": f"{row['Low']:.4f}",
            "4. close": f"{row['Close']:.4f}",
            "5. volume": str(int(row['Volume']))
        }

    data = {
        "Meta Data": meta_data,
        "Time Series (Daily)": time_series
    }
    
    # Print data similar to AV function
    # print(data) # AV function prints data, might be too verbose if large, but let's match existing behavior or skip to avoid spam.
    # The existing function does `print(data)`.
    # print(json.dumps(data, indent=4)) 
    
    update_json(data, SYMBOL)


def get_intraday_price_yf(SYMBOL: str, interval: str = "60m"):
   
    # Map interval to standardized format
    # user asked for "60min", yfinance uses "60m"
    if interval == "60min":
        interval = "60m"

    print(f"Fetching intraday ({interval}) data for {SYMBOL} using yfinance...")
    
    ticker = yf.Ticker(SYMBOL)
    # 730 days is the max limit for hourly data in yfinance
    # fetching 1 month is usually sufficient for recent intraday analysis
    hist = ticker.history(period="1mo", interval=interval)
    
    if hist.empty:
        print(f"Error: No intraday data found for {SYMBOL}")
        return

    # Sort descending
    hist = hist.sort_index(ascending=False)
    
    last_refreshed = hist.index[0].strftime('%Y-%m-%d %H:%M:%S')
    
    meta_data = {
        "1. Information": f"Intraday ({interval}) Prices and Volumes",
        "2. Symbol": SYMBOL,
        "3. Last Refreshed": last_refreshed,
        "4. Interval": interval,
        "5. Output Size": "Compact",
        "6. Time Zone": "US/Eastern"
    }
    
    time_series_key = f"Time Series ({interval})" # e.g. "Time Series (60m)"
    
    time_series = {}
    for index, row in hist.iterrows():
        # Alpha Vantage uses "yyyy-MM-dd HH:mm:ss" for intraday keys
        date_str = index.strftime('%Y-%m-%d %H:%M:%S')
        time_series[date_str] = {
            "1. open": f"{row['Open']:.4f}",
            "2. high": f"{row['High']:.4f}",
            "3. low": f"{row['Low']:.4f}",
            "4. close": f"{row['Close']:.4f}",
            "5. volume": str(int(row['Volume']))
        }

    data = {
        "Meta Data": meta_data,
        time_series_key: time_series
    }
    
    update_json(data, SYMBOL)

def get_daily_price(SYMBOL: str):
    
    if AV_KEY:
        get_daily_price_av(SYMBOL)
    else:
        get_intraday_price_yf(SYMBOL)

if __name__ == "__main__":
    for symbol in all_nasdaq_100_symbols:
        get_daily_price(symbol)

    get_daily_price("QQQ")
