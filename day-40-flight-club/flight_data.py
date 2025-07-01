class FlightData:
    """
    FlightDataクラス
    このクラスは、フライト検索結果から得られる航空券データを構造化するために使用されます。
    出発日、出発地、目的地、価格などのフライトに関する詳細情報を保持します。
    """
    def __init__(self, depart_date: str, origin: str, destination: str, value: int, is_departure: bool = True, index: int = 0):
        """
        FlightDataクラスのコンストラクタ。
        フライトの各属性を初期化します。
        
        Args:
            depart_date (str): 出発日（例: "2023-10-26"）。
            origin (str): 出発地の都市コード（例: "TYO"）。
            destination (str): 目的地の都市コード（例: "LON"）。
            value (int): フライトの価格。
            is_departure (bool): そのデータが往路（True）か復路（False）かを示します。デフォルトはTrueです。
            index (int): Google Sheets上でこのフライトデータが保存されている行番号（1始まり）。
                         データ更新時に特定の行を識別するために使用されます。デフォルトは0です。
        """
        self.depart_date = depart_date
        self.origin = origin
        self.destination = destination
        self.value = value
        self.is_departure = is_departure
        self.index = index # sheet更新用
        
    def __str__(self):
        """
        FlightDataオブジェクトの文字列表現を返します。
        デバッグやログ出力時にフライトデータを分かりやすく表示するために使用されます。
        """
        return f"FlightData(depart_date={self.depart_date}, origin={self.origin}, destination={self.destination}, value={self.value})"