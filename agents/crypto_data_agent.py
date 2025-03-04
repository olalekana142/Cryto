import requests
from datetime import datetime, timedelta

class CryptoDataAgent:
    def __init__(self):
        self.base_url = "https://api.coingecko.com/api/v3"
        self.top_coins = ["bitcoin", "ethereum", "binancecoin", "ripple", "cardano", "solana"]
    
    def get_market_data(self, coin_id="bitcoin"):
        """Get detailed market data for a specific coin"""
        try:
            response = requests.get(
                f"{self.base_url}/coins/{coin_id}",
                params={
                    "localization": "false",
                    "tickers": "false",
                    "community_data": "false",
                    "developer_data": "false"
                }
            )
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            print(f"Error fetching market data: {e}")
            return None

    def get_trending_coins(self):
        """Get trending coins in the last 24h"""
        try:
            response = requests.get(f"{self.base_url}/search/trending")
            if response.status_code == 200:
                return response.json().get("coins", [])[:5]
            return []
        except Exception as e:
            print(f"Error fetching trending coins: {e}")
            return []

    def analyze_market_sentiment(self, market_data):
        """Analyze market sentiment based on price changes and market cap"""
        if not market_data:
            return "neutral"
        
        price_change = market_data.get("market_data", {}).get("price_change_percentage_24h", 0)
        if price_change > 5:
            return "very bullish"
        elif price_change > 2:
            return "bullish"
        elif price_change < -5:
            return "very bearish"
        elif price_change < -2:
            return "bearish"
        return "neutral"

    def get_advice(self, query):
        """Get comprehensive trading advice"""
        # Get trending coins
        trending = self.get_trending_coins()
        
        # Get market data for top coins
        market_insights = []
        for coin in self.top_coins:
            data = self.get_market_data(coin)
            if data:
                market_data = data.get("market_data", {})
                sentiment = self.analyze_market_sentiment(data)
                
                insights = {
                    "name": data.get("name"),
                    "symbol": data.get("symbol", "").upper(),
                    "current_price": market_data.get("current_price", {}).get("usd", 0),
                    "price_change_24h": market_data.get("price_change_percentage_24h", 0),
                    "market_cap_rank": data.get("market_cap_rank", 0),
                    "sentiment": sentiment
                }
                market_insights.append(insights)

        # Generate recommendations
        recommendations = []
        for insight in market_insights:
            if insight["sentiment"] in ["very bullish", "bullish"]:
                recommendations.append(f"Consider buying {insight['name']} ({insight['symbol']})")
            elif insight["sentiment"] in ["very bearish", "bearish"]:
                recommendations.append(f"Exercise caution with {insight['name']} ({insight['symbol']})")

        trending_recommendations = [
            f"Watch trending coin: {coin['item']['name']} ({coin['item']['symbol'].upper()})"
            for coin in trending
        ]

        return {
            "status": "success",
            "market_insights": market_insights,
            "trending_coins": trending_recommendations,
            "recommendations": recommendations,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
