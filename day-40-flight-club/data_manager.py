from google.oauth2 import service_account
from googleapiclient.discovery import build
from user_data import UserData
from flight_data import FlightData

class DataManager:
    """
    DataManagerクラス
    このクラスはGoogle Sheetsと連携し、フライト価格データの読み書きを行います。
    Google Sheets APIを使用して、フライトの目的地、価格、出発日、復路日などの情報を管理します。
    """
    # Google SheetsのスプレッドシートID。
    # このIDは、Google SheetsのURLから取得できます。
    SPREADSHEET_ID = '1J9kxBoNM5cG_mGde6enGMi8Rv893uYQ4pRLRnNaL16E'
    # データの範囲を指定（1行目はヘッダー行のため、A2からF列までを対象とします）。
    RANGE_NAME = 'Flight!A2:F'

    def __init__(self):
        """
        DataManagerクラスのコンストラクタ。
        Google Sheets APIへの認証を設定し、APIサービスオブジェクトを初期化します。
        認証情報はサービスアカウントキーファイルから読み込まれます。
        """
        self.credentials = service_account.Credentials.from_service_account_file(
            'cheapest-flight-finder-464513-70046c2a2cc5.json',
            scopes=["https://www.googleapis.com/auth/spreadsheets"]
        )
        self.sheets_service = build('sheets', 'v4', credentials=self.credentials)

    def fetch_all_saved_flight_data(self, origin: str) -> list[FlightData]:
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
        
        saved_flight_data = []
        for index, row in enumerate(rows):
            destination = row[1] if len(row) > 1 else None
            # 価格は文字列として取得されるため、数値に変換できるかチェックし、変換できない場合は0を設定します。
            departure_price = int(row[2]) if len(row) > 2 and row[2].isdigit() else 0
            departure_date = row[3] if len(row) > 3 else None
            return_price = int(row[4]) if len(row) > 4 and row[4].isdigit() else 0
            return_date = row[5] if len(row) > 5 else None
            
            saved_flight_data.append(FlightData(
                origin=origin,
                destination=destination,
                value=departure_price,
                depart_date=departure_date,
                is_departure=True,
                index=index+2
            ))
            saved_flight_data.append(FlightData(
                origin=destination,
                destination=origin,
                value=return_price,
                depart_date=return_date,
                is_departure=False,
                index=index+2
            ))
        return saved_flight_data

    def update_saved_flight_data(self, sheet_row_number: int, price: int, depart_date: str, is_departure: bool):
        """
        Google Sheetsの特定の行にあるフライト価格と日付を更新します。
        指定された行番号とフライトの種類（往路または復路）に基づいて、
        対応する価格と日付のセルを更新します。
        
        Args:
            sheet_row_number (int): 更新するGoogle Sheetsの行番号（1始まり）。
                                     DataManager.RANGE_NAMEがA2から始まるため、実際の行番号と一致させます。
            price (int): 更新する新しい価格。
            depart_date (str): 更新する出発日または復路日。
            is_departure (bool): 往路のデータを更新する場合はTrue、復路のデータを更新する場合はFalse。
        """
        # 価格を更新するセルの範囲を決定します。
        # 往路価格はC列、復路価格はE列に保存されます。
        if is_departure:
            price_range = f'Flight!C{sheet_row_number}'
        else:
            price_range = f'Flight!E{sheet_row_number}'
        
        # Google Sheetsの価格セルを更新します。
        price_body = {
            'values': [[price]]
        }
        self.sheets_service.spreadsheets().values().update(
            spreadsheetId=self.SPREADSHEET_ID,
            range=price_range,
            valueInputOption="RAW", # RAWオプションは入力値をそのまま扱います。
            body=price_body
        ).execute()
        
        # 日付を更新するセルの範囲を決定します。
        # 往路日はD列、復路日はF列に保存されます。
        date_range = f'Flight!D{sheet_row_number}' if is_departure else f'Flight!F{sheet_row_number}'
        
        # Google Sheetsの日付セルを更新します。
        date_body = {
            'values': [[depart_date]]
        }
        self.sheets_service.spreadsheets().values().update(
            spreadsheetId=self.SPREADSHEET_ID,
            range=date_range,
            valueInputOption="RAW", # RAWオプションは入力値をそのまま扱います。
            body=date_body
        ).execute()

    def add_user_data(self, user_data: UserData):
        """
        Google Sheetsにユーザー情報を追加します。
        """
        user_range = 'User!A2:C'
        user_body = {
            'values': [[user_data.first_name, user_data.last_name, user_data.email]]
        }
        self.sheets_service.spreadsheets().values().update(
            spreadsheetId=self.SPREADSHEET_ID,
            range=user_range,
            valueInputOption="RAW", # RAWオプションは入力値をそのまま扱います。
            body=user_body
        ).execute()