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

    def fetch_all_saved_flight_data(self) -> list:
        """
        Google Sheetsから全てのフライト価格データを取得します。
        取得したデータは、出発日、出発地、目的地、最低往路価格、最低復路価格を含む辞書のリストとして整形されます。
        Returns:
            list: フライト価格データのリスト。
        """
        result = self.sheets_service.spreadsheets().values().get(
            spreadsheetId=self.SPREADSHEET_ID,
            range=self.RANGE_NAME
        ).execute()
        rows = result.get('values', [])
        saved_flight_data = [{"destination": row[1], 
               "departure_price": int(row[2]) if len(row) > 2 and row[2].isdigit() else 0, 
               "departure_date": row[3] if len(row) > 3 else None,
               "return_price": int(row[4]) if len(row) > 4 and row[4].isdigit() else 0,
               "return_date": row[5] if len(row) > 5 else None} 
              for row in rows]
        return saved_flight_data

    def update_saved_flight_data(self, object_id: int, price: int, depart_date: str, is_departure: bool):
        """
        Google Sheets の特定の行にあるフライト価格と日付を更新します。
        Args:
            object_id (int): 更新する行のID（0始まりのインデックス）。
            price (int): 更新する新しい価格。
            depart_date (str): 更新する出発日。
            is_departure (bool): 往路価格を更新する場合はTrue、復路価格を更新する場合はFalse。
        """
        # Google Sheetsのデータを更新
        row = object_id
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