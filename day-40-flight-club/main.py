# main.py
# このファイルは、航空券の最安値検索とユーザーへの通知を管理するメインプログラムです。
# DataManager, FlightSearch, FlightData, NotificationManager クラスを使用して、
# プログラムの要件を達成します。

#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
from flight_search import FlightSearch
from data_manager import DataManager
from notification_manager import NotificationManager
from flight_data import FlightData
from user_data import UserData  
import os
import dotenv
dotenv.load_dotenv()

# 出発地の空港コード (東京)
origin = "TYO"
# 通知メールの送信先アドレスを環境変数から取得
to_addrs = os.getenv("TO_ADDRS")
# DataManagerのインスタンスを作成（データ操作用）
data_manager = DataManager()
# NotificationManagerのインスタンスを作成（メール通知用）
notification_manager = NotificationManager()

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
    return latest_cheapest_flight

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
    # 各目的地についてフライト情報を検索し、価格を更新。メール通知が必要な場合は通知を送信する
    saved_flight_data = data_manager.fetch_all_saved_flight_data(origin)
    for flight_data in saved_flight_data:
        latest_flight_data = get_latest_cheapest_flight(flight_data.origin, flight_data.destination)
        saved_price = flight_data.value
        if latest_flight_data is not None and latest_flight_data.value != saved_price:
            data_manager.update_saved_flight_data(flight_data.index, latest_flight_data.value, latest_flight_data.depart_date, flight_data.is_departure)
            print(f"Updated departure price for departure from {flight_data.origin} to {flight_data.destination} from {saved_price} to {latest_flight_data.value}")
            if need_notification(latest_flight_data.value, saved_price):
                notify_users(latest_flight_data, saved_price)

def notify_users(latest_flight_data: FlightData, saved_price: int):
    """
    すべてのユーザーにメールを送信する
    """
    user_data = data_manager.fetch_all_user_data()
    for user in user_data:
        notification_manager.send_email(user.email, latest_flight_data, saved_price)
        print(f"Sent email to {user.email} for departure from {latest_flight_data.origin} to {latest_flight_data.destination} from {saved_price} to {latest_flight_data.value}")

def add_user_data():
    """
    ユーザーを追加する
    """
    print("Welcome to Flight Club.\nWe find the best flight deals and email you.")
    first_name = input("What is your first name?\n")
    last_name = input("What is your last name?\n")
    email = input("What is your email?\n")
    validate_email = input("Please enter your email again.\n")
    if email != validate_email:
        print("Emails do not match. Please try again.")
        return
    print(f"Welcome to the Flight Club, {first_name} {last_name}!")
    print(f"You're in the club {email}!")
    user_data = UserData(first_name=first_name, last_name=last_name, email=email)
    data_manager.add_user_data(user_data)


if __name__ == "__main__":
    add_user_data()
    # run_flight_check_and_notify()
    