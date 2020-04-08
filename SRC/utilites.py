import json
import random

from pip._vendor import requests

gif_api_key = "47GQTCO6W90R"

def get_gif(name):
    pos = "6"
    r = requests.get("https://api.tenor.com/v1/search?q=%s&key=%s&pos=%s&limit=%s" % (name, gif_api_key, pos, 1))
    if r.status_code == 200:
        return json.loads(r.content)


def get_random_gif():
    pos = str(random.randint(0, 100))
    good_pos = False
    while not good_pos:
        if pos == 99 or pos == 100 or pos == 50:
            pos = str(random.randint(0, 100))
        else:
            good_pos = True
    r = requests.get("https://api.tenor.com/v1/search?q=%s&key=%s&pos=%s&limit=%s" % ("kanye", gif_api_key, pos, 1))
    if r.status_code == 200:
        return json.loads(r.content)


def output_random_quote():
    with open("HELPERS/Quotes.txt", "r") as file:
        list = []
        for line in file:
            list.append(line)
        return list
