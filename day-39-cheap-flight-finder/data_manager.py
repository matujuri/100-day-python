from google.oauth2 import service_account
from googleapiclient.discovery import build

class DataManager:
    # This class is responsible for talking to Google Sheets.
    SPREADSHEET_ID = '1J9kxBoNM5cG_mGde6enGMi8Rv893uYQ4pRLRnNaL16E'  # Google SheetsのスプレッドシートID
    RANGE_NAME = 'Sheet1!A2:F'  # データの範囲を指定（1行目がヘッダー）

    def __init__(self):
        self.credentials = service_account.Credentials.from_service_account_file(
            'cheapest-flight-finder-464513-70046c2a2cc5.json',
            scopes=["https://www.googleapis.com/auth/spreadsheets"]
        )
        self.sheets_service = build('sheets', 'v4', credentials=self.credentials)
        self.price_data = self.price_data()

    def price_data(self) -> list:
        # Google Sheetsからデータを取得
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
        return [data["iataCode"] for data in self.price_data]

    def get_price_data(self, destination: str) -> tuple[int, int]:
        for data in self.price_data:
            if data["iataCode"] == destination:
                return (data["lowestDeparturePrice"], data["lowestReturnPrice"])
        return (0, 0)

    def update_price(self, object_id: int, price: int, depart_date: str, is_departure: bool):
        # Google Sheetsのデータを更新
        row = object_id + 2
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