import os
import requests
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

class FlightSearch:
    #This class is responsible for talking to the Flight Search API.
    TRAVELPAYOUTS_API_KEY = os.getenv("TRAVELPAYOUTS_API_KEY")
    TRAVELPAYOUTS_CURRENCY = "JPY"
    FLIGHT_SEARCH_ENDPOINT = "https://api.travelpayouts.com/v2/prices/month-matrix"
    
    def __init__(self, origin: str, destination: str):
        self.headers = {
            "X-Access-Token": self.TRAVELPAYOUTS_API_KEY
        }
        self.origin = origin
        self.destination = destination
        self.month = ""
        self.params = {
            "currency": self.TRAVELPAYOUTS_CURRENCY,
            "show_to_affiliates": "true",
            "origin": self.origin,
            "destination": self.destination,
            "month": self.month
        }

    def get_flight_prices(self, month: str) -> dict:
        self.params["month"] = month
        response = requests.get(self.FLIGHT_SEARCH_ENDPOINT, params=self.params, headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def get_cheapest_flight_in_six_months(self) -> dict:
        """
        現在の月から始まる今後約6ヶ月間（180日間）の最安フライトを検索します。
        このメソッドは、将来の180日間の各月に含まれるフライトデータを収集し、
        その中から最も安いフライトを特定します。APIの月単位のデータ取得特性を考慮し、
        対象期間に含まれるすべてのユニークな月のデータを取得します。
        """
        today = datetime.now()
        unique_months = set()
        
        # 明日から180日後までの日付を反復し、関連するすべてのユニークな月を収集します。
        for i in range(1, 181): # 明日(1日後)から180日後まで
            current_date = today + timedelta(days=i)
            unique_months.add(current_date.strftime("%Y-%m")) # YYYY-MM形式で月を格納

        all_flights = []
        # 収集したユニークな各月のフライトデータを取得します。
        for month_str in sorted(unique_months): # 処理順序を保証するためソート
            # APIが月のデータ全体を返すように、その月の最初の日を渡します。
            date_for_api = f"{month_str}-01"
            response = self.get_flight_prices(month=date_for_api)
            
            if response and response.get("data"): # dataキーが存在し、かつ空でないことを確認
                all_flights.extend(response["data"])

        if len(all_flights) == 0:
            return {}
        else:
            cheapest_flight = min(all_flights, key=lambda flight: flight["value"])
            return cheapest_flight
