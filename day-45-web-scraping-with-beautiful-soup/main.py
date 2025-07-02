from bs4 import BeautifulSoup
from requests import get
from notification_manager import NotificationManager

response = get("https://news.ycombinator.com/news")

soup = BeautifulSoup(response.text, "html.parser")

articles = soup.select(".titleline")
titles = [article.a.getText() for article in articles]
links = [article.a.get("href") for article in articles]
scores = [int(score.getText().split()[0]) for score in soup.select(".score")]

items = [
    {
        "title": title,
        "link": link,
        "score": score
    }
    for title, link, score in zip(titles, links, scores)
]

items.sort(key=lambda x: x["score"], reverse=True)

mail_html_body = ""
for item in items:
    mail_html_body += f"""
    <h3><a href="{item["link"]}">{item["title"]}</a></h3>
    <p>{item["score"]}</p>
    <hr />
    """

print(mail_html_body)

notification_manager = NotificationManager()
notification_manager.send_email(to_addrs="xiaobaka59@gmail.com", subject="Hacker News", message=mail_html_body)
