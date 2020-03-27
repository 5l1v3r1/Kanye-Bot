from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
from urllib.request import Request

url = "https://www.reddit.com/r/Kanye/"
upvotes = []
titles = []
pictures = []
links = []
loop = 0

def gather_post_info():
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html = uReq(req).read()
    page_soup = soup(html, "html.parser")
    global loop
    for container in page_soup.find_all("div", {"class": "scrollerItem"}):
        if loop == 5:
            break

        if container.find("span", attrs={"class": "_2oEYZXchPfHwcf9mTMGMg8"}):
            continue

        upvotes_div = container.find("div", attrs={"class": "_1rZYMD_4xY3gRcSS3p8ODO"})
        if upvotes_div is not None:
            upvotes.append(upvotes_div.text.strip())

        titles_div = container.find("h3", attrs={"class": "_eYtD2XCVieq6emjKBH3m"})
        if titles_div is not None:
            titles.append(titles_div.text.strip())

        possible_video_div = container.find("video", attrs={"class": "_1EQJpXY7ExS04odI1YBBlj"})
        if possible_video_div is not None:
            pictures.append(possible_video_div['poster'])

        titles_div = container.find("img", attrs={"class": "ImageBox-image"})
        if titles_div is not None:
            pictures.append(titles_div['src'])

        link_div = container.find("a", attrs={"class": "SQnoC3ObvgnGjWt90zD9Z _2INHSNB8V5eaWp4P0rY_mE"})
        if link_div is not None:
            links.append("https://reddit.com"+link_div['href'])

        loop += 1