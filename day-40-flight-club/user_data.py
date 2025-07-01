class UserData:
    """
    UserDataクラス
    このクラスは、ユーザーの氏名とメールアドレスを構造化して保持するために使用されます。
    フライト通知の送信先ユーザー情報を管理する際に利用されます。
    """
    def __init__(self, first_name: str, last_name: str, email: str):
        """
        UserDataクラスのコンストラクタ。
        ユーザーの各属性を初期化します。
        
        Args:
            first_name (str): ユーザーの名。
            last_name (str): ユーザーの姓。
            email (str): ユーザーのメールアドレス。
        """
        self.first_name = first_name
        self.last_name = last_name
        self.email = email

