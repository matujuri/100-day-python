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

def get_cheapest_flight(origin: str, destination: str):
    """
    指定された出発地と目的地に対して、過去1年間で最も安いフライトを検索します。
    Args:
        origin (str): 出発地の都市コード。
        destination (str): 目的地の都市コード。
    Returns:
        FlightData: 最も安いフライトのデータ、見つからない場合はNone。
    """
    flight_search = FlightSearch(origin=origin, destination=destination)
    cheapest_flight = flight_search.get_cheapest_flight_in_a_year()
    if cheapest_flight == {}:
        return None
    flight_data = FlightData(
        depart_date=cheapest_flight["depart_date"],
        origin=cheapest_flight["origin"],
        destination=cheapest_flight["destination"],
        value=cheapest_flight["value"]
    )
    print(flight_data.__str__())
    return flight_data

def process_flight_data(flight_data: FlightData, current_price: float, is_departure: bool, destination: str, destination_index: int, data_manager: DataManager, notification_manager: NotificationManager):
    """
    フライトデータを処理し、価格更新と通知を行う共通関数。
    新しいフライトの価格が既存の価格より安い場合、DataManagerを更新し、通知を送信します。
    Args:
        flight_data (FlightData): 処理するフライトデータオブジェクト。
        current_price (float): 現在のデータベースに保存されている価格。
        is_departure (bool): 往路フライトの場合はTrue、復路フライトの場合はFalse。
        destination (str): 目的地の空港コード。
        destination_index (int): 目的地のインデックス。
        data_manager (DataManager): DataManagerのインスタンス。
        notification_manager (NotificationManager): NotificationManagerのインスタンス。
    """
    if flight_data is not None and is_price_update_needed(flight_data.value, current_price):
        # 価格を更新し、データベースに保存
        data_manager.update_price(destination_index, flight_data.value, flight_data.depart_date, is_departure)
        flight_type = "departure" if is_departure else "return"
        print(f"Updated {flight_type} price for {destination} from {current_price} to {flight_data.value}")
        
        # 新しい価格が大幅に安い場合、通知を送信
        if flight_data.value < current_price - 1000:
            notification_manager.send_email(flight_data)
            print(f"Sent email for {destination} from {current_price} to {flight_data.value}")

def is_price_update_needed(new_price: float, old_price: float) -> bool:
    """
    新しいフライト価格に基づいて価格更新が必要かどうかを判断する。
    既存の価格が0の場合、または新しい価格が既存の価格より1000安かった場合は更新が必要と判断します。
    Args:
        new_price (float): 新しいフライトの価格。
        old_price (float): 現在データベースに保存されているフライトの価格。
    Returns:
        bool: 価格更新が必要な場合はTrue、それ以外の場合はFalse。
    """
    return old_price == 0 or new_price < old_price - 1000

# DataManagerのインスタンスを作成（データ操作用）
data_manager = DataManager()
# 目的地のデータを取得
destination_data = data_manager.get_destination_data()
# NotificationManagerのインスタンスを作成（メール通知用）
notification_manager = NotificationManager(to_addrs=to_addrs)

# 各目的地についてフライト情報を検索し、価格を更新
for index, destination in enumerate(destination_data):
    # 往路フライトの処理
    departure_flight_data = get_cheapest_flight(origin, destination)
    # 現在の目的地データから最低往路価格を取得
    departure_price = data_manager.get_departure_price(destination)
    # 往路フライトのデータを処理し、必要に応じて価格を更新し通知
    process_flight_data(departure_flight_data, departure_price, True, destination, index, data_manager, notification_manager)
    
    # 復路フライトの処理
    return_flight_data = get_cheapest_flight(destination, origin)
    # 現在の目的地データから最低復路価格を取得
    return_price = data_manager.get_return_price(destination)
    # 復路フライトのデータを処理し、必要に応じて価格を更新し通知
    process_flight_data(return_flight_data, return_price, False, destination, index, data_manager, notification_manager)