import requests

class Post:
    def __init__(self, id, title, subtitle, body):
        self.id = id
        self.title = title
        self.subtitle = subtitle
        self.body = body

class Posts:
    def __init__(self):
        self.all_posts = []
        self.get_posts()
    
    def get_posts(self):
        response = requests.get("https://api.npoint.io/707b3421446e5ca81b90")
        response.raise_for_status()
        self.all_posts = response.json()

    def get_post(self, id):
        for post in self.all_posts:
            if post["id"] == id:
                return post
