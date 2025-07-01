import os
import requests
from dotenv import load_dotenv

load_dotenv()

class FlightSearch:
    """
    フライト検索API (Travelpayouts API) と連携し、フライト情報を取得するクラス。
    """
    # Travelpayouts APIの認証キーを環境変数から取得
    TRAVELPAYOUTS_API_KEY = os.getenv("TRAVELPAYOUTS_API_KEY")
    # 使用する通貨
    TRAVELPAYOUTS_CURRENCY = "JPY"
    # フライト検索APIのエンドポイントURL
    FLIGHT_SEARCH_ENDPOINT = "https://api.travelpayouts.com/v2/prices/latest"
    
    def __init__(self, origin: str, destination: str):
        """
        FlightSearchクラスのコンストラクタ。
        APIリクエストに必要なヘッダーとパラメータを設定します。
        Args:
            origin (str): 出発地の都市コード。
            destination (str): 目的地の都市コード。
        """
        self.headers = {
            "X-Access-Token": self.TRAVELPAYOUTS_API_KEY
        }
        self.origin = origin
        self.destination = destination
        self.params = {
            "origin": self.origin,
            "destination": self.destination,
            "currency": self.TRAVELPAYOUTS_CURRENCY,
            "limit": 1,
            "period_type": "year",
            "one_way": True
        }

    def get_latest_cheapest_flight_in_a_year(self) -> dict:
        """
        指定された出発地と目的地に対する過去1年間で最も安いフライトを検索します。
        APIから取得したレスポンスを処理し、フライトデータが存在しない場合は空の辞書を返します。
        Returns:
            dict: 最も安いフライトのデータを含む辞書、または空の辞書。
        """
        response = requests.get(self.FLIGHT_SEARCH_ENDPOINT, params=self.params, headers=self.headers)
        response.raise_for_status()
        if len(response.json()["data"]) == 0:
            return {}
        return response.json()["data"][0]