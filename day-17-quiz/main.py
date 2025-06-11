# Userクラスの定義
# 目的: ユーザーの情報を管理し、フォロー機能を提供する
class User:
    # コンストラクタ
    # 目的: Userオブジェクトを初期化する
    # 引数: user_id (ユーザーID), username (ユーザー名)
    def __init__(self, user_id, username):
        self.id = user_id
        self.username = username
        self.followers = 0
        self.following = 0

    # followメソッド
    # 目的: 別のユーザーをフォローする。フォローする側のfollowing数を増やし、フォローされる側のfollowers数を増やす。
    # 引数: user (フォローするUserオブジェクト)
    def follow(self, user):
        user.followers += 1
        self.following += 1


user_1 = User("001", "Lily")
user_2 = User("002", "Angela")

user_1.follow(user_2)

print(user_1.followers)
print(user_1.following)
print(user_2.followers)
print(user_2.following)