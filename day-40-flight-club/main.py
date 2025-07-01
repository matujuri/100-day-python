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
    saved_flight_data = data_manager.fetch_all_saved_flight_data()
    flight_data = [FlightData(
        depart_date=data["departure_date"],
        origin=origin,
        destination=data["destination"],
        value=data["departure_price"],
        is_departure=True,
        index=index+2
    ) for index, data in enumerate(saved_flight_data)]
    flight_data.extend(FlightData(
        depart_date=data["return_date"],
        origin=data["destination"],
        destination=origin,
        value=data["return_price"],
        is_departure=False,
        index=index+2
    ) for index, data in enumerate(saved_flight_data))
    return flight_data

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
# NotificationManagerのインスタンスを作成（メール通知用）
notification_manager = NotificationManager(to_addrs=to_addrs)

# 各目的地についてフライト情報を検索し、価格を更新
for index, flight_data in enumerate(get_saved_flight_data(data_manager, origin)):
    latest_flight_data = get_latest_cheapest_flight(flight_data.origin, flight_data.destination)
    saved_price = flight_data.value
    if latest_flight_data is not None and is_price_update_needed(latest_flight_data.value, saved_price):
        data_manager.update_saved_flight_data(flight_data.index, latest_flight_data.value, latest_flight_data.depart_date, flight_data.is_departure)
        print(f"Updated departure price for {flight_data.destination} from {saved_price} to {latest_flight_data.value}")
        if latest_flight_data.value < saved_price - 1000:
            notification_manager.send_email(latest_flight_data)
            print(f"Sent email for {flight_data.destination} from {saved_price} to {latest_flight_data.value}")
    