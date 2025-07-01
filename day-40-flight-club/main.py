# main.py
# このファイルは、航空券の最安値検索とユーザーへの通知を管理するメインプログラムです。
# DataManager, FlightSearch, FlightData, NotificationManager クラスを使用して、
# プログラムの要件を達成します。

#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
from flight_search import FlightSearch
from flight_data import FlightData
from data_manager import DataManager
from notification_manager import NotificationManager
import os
import dotenv
dotenv.load_dotenv()

# 出発地の空港コード (東京)
origin = "TYO"
# 通知メールの送信先アドレスを環境変数から取得
to_addrs = os.getenv("TO_ADDRS")

def get_latest_cheapest_flight(origin: str, destination: str):
    """
    指定された出発地と目的地に対して、過去1年間で最も安いフライトを検索します。
    Args:
        origin (str): 出発地の都市コード。
        destination (str): 目的地の都市コード。
    Returns:
        FlightData: 最も安いフライトのデータ、見つからない場合はNone。
    """
    flight_search = FlightSearch(origin=origin, destination=destination)
    latest_cheapest_flight = flight_search.get_latest_cheapest_flight_in_a_year()
    if latest_cheapest_flight == {}:
        return None
    flight_data = FlightData(
        depart_date=latest_cheapest_flight["depart_date"],
        origin=latest_cheapest_flight["origin"],
        destination=latest_cheapest_flight["destination"],
        value=latest_cheapest_flight["value"]
    )
    print(flight_data.__str__())
    return flight_data

def get_saved_flight_data(data_manager: DataManager, origin: str) -> list[FlightData]:
    """
    DataManagerから保存されたフライトデータを取得し、FlightDataオブジェクトのリストに変換します。
    Google Sheetsから読み込んだ生データを、プログラム内で扱いやすい形式に整形します。
    
    Args:
        data_manager (DataManager): DataManagerのインスタンス。Google Sheetsからデータを取得するために使用されます。
        origin (str): 出発地の都市コード。これはすべてのフライトデータの出発地として設定されます。
        
    Returns:
        list[FlightData]: 整形されたFlightDataオブジェクトのリスト。
                         各要素は往路または復路のフライト情報を表します。
    """
    # DataManagerを使用してGoogle Sheetsから全ての保存済みフライトデータを取得します。
    saved_flight_data = data_manager.fetch_all_saved_flight_data()
    
    # 取得したデータから往路フライトのFlightDataオブジェクトを作成します。
    # Google Sheetsの行は1から始まるため、インデックスに2を加えることで正確な行番号（sheet_row_number）を_FlightData.indexに設定します。
    flight_data = [FlightData(
        depart_date=data["departure_date"],
        origin=origin,
        destination=data["destination"],
        value=data["departure_price"],
        is_departure=True,
        index=index+2 # Google Sheetsの行番号（1始まり、ヘッダー行が1行目なのでデータは2行目から）
    ) for index, data in enumerate(saved_flight_data)]
    
    # 復路フライトのFlightDataオブジェクトを作成し、既存のリストに追加します。
    # 復路の場合、出発地と目的地が往路と逆になります。
    flight_data.extend(FlightData(
        depart_date=data["return_date"],
        origin=data["destination"],
        destination=origin,
        value=data["return_price"],
        is_departure=False,
        index=index+2 # Google Sheetsの行番号（1始まり）
    ) for index, data in enumerate(saved_flight_data))
    
    return flight_data

def need_notification(new_price: float, old_price: float) -> bool:
    """
    新しいフライト価格に基づいてメール通知が必要かどうかを判断する。
    新しい価格が既存の価格より1000円安かった場合は通知が必要と判断します。
    Args:
        new_price (float): 新しいフライトの価格。
        old_price (float): 現在データベースに保存されているフライトの価格。
    Returns:
        bool: メール通知が必要な場合はTrue、それ以外の場合はFalse。
    """
    return new_price < old_price - 1000

def run_flight_check_and_notify():
    """
    フライトデータの確認と通知を行うメイン処理。
    DataManagerから保存されたフライトデータを取得し、最新の最安フライトを検索、
    価格の更新が必要な場合はデータベースを更新し、ユーザーに通知します。
    """
    # DataManagerのインスタンスを作成（データ操作用）
    data_manager = DataManager()
    # NotificationManagerのインスタンスを作成（メール通知用）
    notification_manager = NotificationManager(to_addrs=to_addrs)

    # 各目的地についてフライト情報を検索し、価格を更新。メール通知が必要な場合は通知を送信する
    for index, flight_data in enumerate(get_saved_flight_data(data_manager, origin)):
        latest_flight_data = get_latest_cheapest_flight(flight_data.origin, flight_data.destination)
        saved_price = flight_data.value
        if latest_flight_data is not None:
            data_manager.update_saved_flight_data(flight_data.index, latest_flight_data.value, latest_flight_data.depart_date, flight_data.is_departure)
            print(f"Updated departure price for {flight_data.destination} from {saved_price} to {latest_flight_data.value}")
            if need_notification(latest_flight_data.value, saved_price):
                notification_manager.send_email(latest_flight_data)
                print(f"Sent email for {flight_data.destination} from {saved_price} to {latest_flight_data.value}")

if __name__ == "__main__":
    run_flight_check_and_notify()
    