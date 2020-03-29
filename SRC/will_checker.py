from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
from urllib.request import Request


url = "https://steamcommunity.com/profiles/76561198149063421"

def gather_will_info():
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html = uReq(req).read()
    page_soup = soup(html, "html.parser")
    for container in page_soup.find_all("div", {"class": "_1rZYMD_4xY3gRcSS3p8ODO"}):
        if container.text.strip() == "Currently Offline":
            return True
        else:
            return False


