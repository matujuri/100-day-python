import os
import requests
from dotenv import load_dotenv

load_dotenv()

class FlightSearch:
    """
    FlightSearchクラス
    このクラスはTravelpayouts APIと連携し、航空券の最安値を検索します。
    特定の出発地と目的地に対するフライト情報（出発日、価格など）を取得する機能を提供します。
    """
    # Travelpayouts APIの認証キーを環境変数から取得します。
    # このキーはAPIへのアクセスを許可するために必要です。
    TRAVELPAYOUTS_API_KEY = os.getenv("TRAVELPAYOUTS_API_KEY")
    # フライト検索に使用する通貨を指定します。
    TRAVELPAYOUTS_CURRENCY = "JPY"
    # フライト検索APIのエンドポイントURL。
    # このURLに対してHTTPリクエストを送信してフライト情報を取得します。
    FLIGHT_SEARCH_ENDPOINT = "https://api.travelpayouts.com/v2/prices/latest"
    
    def __init__(self, origin: str, destination: str):
        """
        FlightSearchクラスのコンストラクタ。
        APIリクエストに必要なヘッダーと検索パラメータを初期化します。
        
        Args:
            origin (str): 出発地の都市コード（例: "TYO"）。
            destination (str): 目的地の都市コード（例: "LON"）。
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
            "limit": 1, # 最も安いフライトを1件だけ取得します。
            "period_type": "year", # 過去1年間のフライトを検索対象とします。
            "one_way": True # 片道フライトの価格を検索します。
        }

    def get_latest_cheapest_flight_in_a_year(self) -> dict:
        """
        指定された出発地と目的地に対する過去1年間で最も安いフライトを検索します。
        Travelpayouts APIにリクエストを送信し、そのレスポンスからフライトデータを抽出します。
        
        Returns:
            dict: 最も安いフライトのデータを含む辞書。フライトが見つからない場合は空の辞書を返します。
                  返される辞書には、出発日 ('depart_date')、出発地 ('origin')、
                  目的地 ('destination')、価格 ('value') などが含まれます。
        """
        # APIにGETリクエストを送信します。
        # ヘッダーにはAPIキー、パラメータには検索条件を含めます。
        response = requests.get(self.FLIGHT_SEARCH_ENDPOINT, params=self.params, headers=self.headers)
        # HTTPエラーが発生した場合は例外を発生させます。
        response.raise_for_status()
        
        # レスポンスのJSONデータからフライトデータを取り出します。
        # レスポンスの 'data' フィールドはフライト情報のリストです。
        flight_data = response.json()["data"]
        
        # フライトデータが見つからない場合は空の辞書を返します。
        if not flight_data:
            return {}
        
        # 最も安いフライトデータ（最初の要素）を返します。
        return flight_data[0]