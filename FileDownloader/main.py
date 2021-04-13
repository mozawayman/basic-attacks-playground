#!/usr/bin/env python
import requests

def download(url):
    down_file = requests.get(url)
    print(down_file)
    filename = url.split("/")
    #binary mode open
    with open(filename.pop(), "wb") as out_file:
        out_file.write(down_file.content)

download("https://shifter.sapo.pt/wp-content/uploads/2020/04/GitHub-Gratuito-Shifter_01.jpg")
