from bs4 import BeautifulSoup, ResultSet, Tag
import requests

def webScrapper(url: str) -> ResultSet[Tag]:
    print("\nStart WebScrapper")

    page_to_scrape = requests.get(url)
    soup = BeautifulSoup(page_to_scrape.text, "html.parser")

    body = soup.find('tbody')
    body_list = body.findAll('tr')

    return body_list

if __name__ == "__main__":
    url = "https://docs.google.com/spreadsheets/d/1VZv4gzrwjshWxZLtmjD1xzSL9sTPjliNeu17SJ0DEuA/edit?pli=1&gid=814253745#gid=814253745"
    url3 = "https://docs.google.com/spreadsheets/u/0/d/1RBZOdt2100S9NBBeA81unABfkBxa_2TEZh4brfXyBQE/htmlview#"
    body_list = webScrapper(url3)
    for rand in body_list:
        print(rand)