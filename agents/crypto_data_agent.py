import requests
from datetime import datetime, timedelta

class CryptoDataAgent:
    def __init__(self):
        self.base_url = "https://api.coingecko.com/api/v3"
        self.top_coins = ["bitcoin", "ethereum", "binancecoin", "ripple", "cardano", "solana"]
    
    def get_market_data(self, coin_id="bitcoin"):
        """Get detailed market data for a specific coin"""
        try:
            # First try to get simple price data (faster and more reliable)
            price_response = requests.get(
                f"{self.base_url}/simple/price",
                params={
                    "ids": coin_id,
                    "vs_currencies": "usd",
                    "include_24hr_change": "true",
                    "include_market_cap": "true"
                }
            )
            
            if price_response.status_code == 200:
                price_data = price_response.json().get(coin_id, {})
                return {
                    "market_data": {
                        "current_price": {"usd": price_data.get("usd", 0)},
                        "price_change_percentage_24h": price_data.get("usd_24h_change", 0),
                        "market_cap": {"usd": price_data.get("usd_market_cap", 0)}
                    }
                }
            
            # Fallback to detailed API if simple price fails
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
            return "neutral", "No data available"
        
        price_change = market_data.get("market_data", {}).get("price_change_percentage_24h", 0)
        
        # Lower thresholds for more frequent recommendations
        if price_change > 3:
            return "very bullish", f"Strong upward momentum with {price_change:.1f}% gain"
        elif price_change > 1:
            return "bullish", f"Positive trend with {price_change:.1f}% gain"
        elif price_change < -3:
            return "very bearish", f"Sharp decline of {abs(price_change):.1f}%"
        elif price_change < -1:
            return "bearish", f"Downward trend of {abs(price_change):.1f}%"
        else:
            return "neutral", f"Stable price movement ({price_change:.1f}%)"

    def get_trading_suggestion(self, sentiment, price_change):
        """Generate trading suggestions based on sentiment and price change"""
        if sentiment == "very bullish":
            return f"Strong buy opportunity with upward momentum"
        elif sentiment == "bullish":
            return f"Consider gradual buying or holding"
        elif sentiment == "very bearish":
            return f"Consider taking profits or setting stop losses"
        elif sentiment == "bearish":
            return f"Watch for further price movements before trading"
        else:
            return f"Hold position and monitor market conditions"

    def get_advice(self, query):
        """Get comprehensive trading advice"""
        # Get trending coins
        trending = self.get_trending_coins()
        
        # Get market data for top coins
        market_insights = []
        recommendations = []
        
        for coin in self.top_coins:
            data = self.get_market_data(coin)
            if data:
                market_data = data.get("market_data", {})
                price_change = market_data.get("price_change_percentage_24h", 0)
                sentiment, reason = self.analyze_market_sentiment(data)
                
                insights = {
                    "name": coin.capitalize(),
                    "symbol": coin[:3].upper(),
                    "current_price": market_data.get("current_price", {}).get("usd", 0),
                    "price_change_24h": price_change,
                    "sentiment": sentiment,
                    "reason": reason
                }
                market_insights.append(insights)
                
                # Always add a trading suggestion
                suggestion = self.get_trading_suggestion(sentiment, price_change)
                recommendations.append(f"{coin.capitalize()}: {suggestion}")

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
