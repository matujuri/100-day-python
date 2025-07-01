import os
import smtplib
from flight_data import FlightData

class NotificationManager:
    """
    NotificationManagerクラス
    このクラスは、フライトの最安値情報に関する通知（メール）を送信する責任を負います。
    SMTPプロトコルを使用してGmailサーバー経由でメールを送信します。
    """
    # SMTPサーバーのアドレス（Gmailの場合）
    SMTP_SERVER = "smtp.gmail.com"
    # SMTPサーバーのポート番号（TLS/STARTTLSを使用する場合）
    SMTP_PORT = 587
    # Gmailアカウントのユーザー名（環境変数から取得）
    SMTP_USERNAME = os.getenv("GMAIL_USERNAME")
    # Gmailのアプリパスワード（環境変数から取得。通常のパスワードではない点に注意）
    SMTP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")
    # 送信元メールアドレス（通常はSMTP_USERNAMEと同じ）
    SMTP_FROM = os.getenv("GMAIL_USERNAME")
    
    def __init__(self, to_addrs: str):
        """
        NotificationManagerクラスのコンストラクタ。
        
        Args:
            to_addrs (str): 通知メールの送信先アドレス。
        """
        self.to_addrs = to_addrs
        
    def send_email(self, flight_data: FlightData):
        """
        指定されたフライトデータに基づいて、フライト最安値アラートメールを送信します。
        
        Args:
            flight_data (FlightData): 送信するフライトの詳細情報を含むFlightDataオブジェクト。
        """
        # SMTP接続を確立し、TLS暗号化を開始します。
        with smtplib.SMTP(self.SMTP_SERVER, self.SMTP_PORT) as connection:
            connection.starttls() # 接続を暗号化
            connection.login(user=self.SMTP_USERNAME, password=self.SMTP_PASSWORD)
            # メールメッセージを作成し、送信します。
            # Subjectと本文は改行(\n)で区切ります。
            message = "Subject: Flight Lowest Price Alert!\n\n"
            message += f"Only {flight_data.value} JPY to fly from {flight_data.origin} to {flight_data.destination} on {flight_data.depart_date}"
            connection.sendmail(
                from_addr=self.SMTP_FROM,
                to_addrs=self.to_addrs,
                msg=message.encode('utf-8') # 日本語対応のためutf-8でエンコード
            )

        