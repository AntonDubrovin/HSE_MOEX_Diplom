class MOEXUrls:
    BASE_URL = "https://iss.moex.com/iss"

    SECURITIES = (
        f"{BASE_URL}/engines/{{engine}}/markets/{{market}}/boards/{{board}}/securities.json"
    )

    ANALYTICS = f"{BASE_URL}/statistics/engines/{{engine}}/markets/{{market}}/analytics.json"

    CANDLES = f"{BASE_URL}/engines/{{engine}}/markets/{{market}}/securities/{{secid}}/candles.json"

    DIVIDENDS = f"{BASE_URL}/securities/{{secid}}/dividends.json"

    HISTORY = f"{BASE_URL}/history/engines/{{engine}}/markets/{{market}}/securities/{{secid}}.json"
