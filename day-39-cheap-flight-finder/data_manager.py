from google.oauth2 import service_account
from googleapiclient.discovery import build

class DataManager:
    """
    Google Sheets と連携し、フライト価格データの読み書きを行うクラス。
    """
    # Google SheetsのスプレッドシートID
    SPREADSHEET_ID = '1J9kxBoNM5cG_mGde6enGMi8Rv893uYQ4pRLRnNaL16E'
    # データの範囲を指定（1行目がヘッダー）
    RANGE_NAME = 'Sheet1!A2:F'

    def __init__(self):
        """
        DataManagerクラスのコンストラクタ。
        Google Sheets APIへの認証を設定し、初期データを読み込みます。
        """
        self.credentials = service_account.Credentials.from_service_account_file(
            'cheapest-flight-finder-464513-70046c2a2cc5.json',
            scopes=["https://www.googleapis.com/auth/spreadsheets"]
        )
        self.sheets_service = build('sheets', 'v4', credentials=self.credentials)
        self.price_data = self._fetch_all_price_data()

    def _fetch_all_price_data(self) -> list:
        """
        Google Sheetsから全てのフライト価格データを取得します。
        取得したデータは、IATAコード、最低往路価格、最低復路価格を含む辞書のリストとして整形されます。
        Returns:
            list: フライト価格データのリスト。
        """
        result = self.sheets_service.spreadsheets().values().get(
            spreadsheetId=self.SPREADSHEET_ID,
            range=self.RANGE_NAME
        ).execute()
        
        rows = result.get('values', [])
        price_data = [{"iataCode": row[1], 
               "lowestDeparturePrice": int(row[2]) if len(row) > 2 and row[2].isdigit() else 0, 
               "lowestReturnPrice": int(row[4]) if len(row) > 4 and row[4].isdigit() else 0} 
              for row in rows]
        return price_data

    def get_destination_data(self) -> list:
        """
        現在ロードされている価格データから全ての目的地のIATAコードのリストを取得します。
        Returns:
            list: 目的地のIATAコードのリスト。
        """
        return [data["iataCode"] for data in self.price_data]
    
    def get_departure_price(self, destination: str) -> int:
        """
        指定された目的地の最低往路価格を取得します。
        Args:
            destination (str): 目的地のIATAコード。
        Returns:
            int: 最低往路価格。
        """
        return next(
            (data["lowestDeparturePrice"] for data in self.price_data if data["iataCode"] == destination),
            0
        )
    
    def get_return_price(self, destination: str) -> int:
        """
        指定された目的地の最低復路価格を取得します。
        Args:
            destination (str): 目的地のIATAコード。
        Returns:
            int: 最低復路価格。
        """
        return next(
            (data["lowestReturnPrice"] for data in self.price_data if data["iataCode"] == destination),
            0
        )

    def update_price(self, object_id: int, price: int, depart_date: str, is_departure: bool):
        """
        Google Sheets の特定の行にあるフライト価格と日付を更新します。
        Args:
            object_id (int): 更新する行のID（0始まりのインデックス）。
            price (int): 更新する新しい価格。
            depart_date (str): 更新する出発日。
            is_departure (bool): 往路価格を更新する場合はTrue、復路価格を更新する場合はFalse。
        """
        # Google Sheetsのデータを更新
        row = object_id + 2 # スプレッドシートの行は1から始まり、ヘッダー行があるため+2
        if is_departure:
            range_ = f'Sheet1!C{row}'  # Departure Priceを更新
            value = price
        else:
            range_ = f'Sheet1!E{row}'  # Return Priceを更新
            value = price
        
        # Google Sheetsのセルを更新
        body = {
            'values': [[value]]
        }
        self.sheets_service.spreadsheets().values().update(
            spreadsheetId=self.SPREADSHEET_ID,
            range=range_,
            valueInputOption="RAW",
            body=body
        ).execute()
        
        # 日付の更新
        date_range = f'Sheet1!D{row}' if is_departure else f'Sheet1!F{row}'
        body_date = {
            'values': [[depart_date]]
        }
        self.sheets_service.spreadsheets().values().update(
            spreadsheetId=self.SPREADSHEET_ID,
            range=date_range,
            valueInputOption="RAW",
            body=body_date
        ).execute()
        
        # データ更新後、price_dataを再取得して最新の状態を反映
        self.price_data = self._fetch_all_price_data()