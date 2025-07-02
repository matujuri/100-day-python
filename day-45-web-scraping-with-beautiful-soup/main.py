from bs4 import BeautifulSoup
import lxml

with open("day-45-web-scraping-with-beautiful-soup/website.html", "r") as file:
    contents = file.read()

soup = BeautifulSoup(contents, "lxml")

all_anchor_tags = soup.find_all(name="a")
print(all_anchor_tags)

for tag in all_anchor_tags:
    print(tag.getText())
    print(tag.get("href"))
    
company_url = soup.select_one("p a")
print(company_url)

heading = soup.select(".heading")
print(heading)

second_heading = soup.find(name="h3", class_="heading")
print(second_heading.get("class")[0])
