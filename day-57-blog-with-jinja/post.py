import requests

class Post:
    def __init__(self, id, title, subtitle, body):
        self.id = id
        self.title = title
        self.subtitle = subtitle
        self.body = body

class Posts:
    def __init__(self):
        self.all_posts = self.get_all_posts()
        
    def get_all_posts(self) -> list[Post]:
        response = requests.get("https://api.npoint.io/c790b4d5cab58020d391")
        all_posts = response.json()
        posts = []
        for post in all_posts:
            posts.append(Post(post["id"], post["title"], post["subtitle"], post["body"]))
        return posts
    
    def get_post(self, id: int) -> Post | None:
        for post in self.all_posts:
            if post.id == id:
                return post

