import os
import smtplib
from dotenv import load_dotenv
from email.mime.text import MIMEText

load_dotenv()

class NotificationManager:
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
    
    def __init__(self):
        """
        NotificationManagerクラスのコンストラクタ。
        
        Args:
            to_addrs (str): 通知メールの送信先アドレス。
        """
        self.server = self.SMTP_SERVER
        self.port = self.SMTP_PORT
        self.username = self.SMTP_USERNAME
        self.password = self.SMTP_PASSWORD
        self.from_addr = self.SMTP_FROM
        
    def send_email(self, to_addrs: str, subject: str, message: str):
        # HTMLメールを作成
        msg = MIMEText(message, 'html', 'utf-8')
        msg['Subject'] = subject
        msg['From'] = self.from_addr
        msg['To'] = to_addrs

        # SMTP接続を確立し、TLS暗号化を開始します。
        with smtplib.SMTP(self.server, self.port) as connection:
            connection.starttls() # 接続を暗号化
            connection.login(user=self.username, password=self.password)
            # メールメッセージを作成し、送信します。
            # Subjectと本文は改行(\n)で区切ります。
            connection.sendmail(
                from_addr=self.from_addr,
                to_addrs=to_addrs,
                msg=msg.as_string()
            )
            print("Email sent successfully")

        