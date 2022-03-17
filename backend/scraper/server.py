'''
Microservice API to engage the spider
NOTE: should be calling less than 100 times per day
'''
from fastapi import FastAPI, Form
import uvicorn
import requests
from bs4 import BeautifulSoup
import re
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import random
import base64

app = FastAPI()


origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/maps/search/')
def search_maps(search: str):
    '''
    Extension: use abstractive summarizing for req['search']
    '''
    # search = req['search']
    if ' ' in search:
        search = search.split(' ')
        search = '+'.join(search)
    maps_url = f'https://www.google.com.au/maps/place/{search}'
    # call maps scraper
    html_text = requests.get(maps_url).text

    match = r'^(<iframe src).*(</iframe>)$'

    return {"iframe_src": re.match(html_text, match)}


@app.get('/scrape')
def do_scrape(spider):
    '''
    Calls a specific scraper and returns data when available
    '''
    if spider == 'main':
        # call the main spider
        exec('scrapy super_spider')
        # return all the data in /data
        # Algorithm
        # call data = data_to_json('scraper/data/*')
        # return data
    elif spider == 'news':
        exec('scrapy news')
        # return data from 'scraper/data/news.txt'
    elif spider == 'social_media':
        exec('scrapy social_media')
        # return data from 'scraper/data/social_media.txt'
    elif spider == 'departments':
        exec('scrapy departments')
        # return data from 'scraper/data/departments.txt'
        # NOTE: this includes all federal, state and local departments
    else:
        return {"Error": "Invalid Spider"}


class Image(BaseModel):
    image: str


@app.post('/behavioral/')
def test(image: Image):
    # print(image)
    img_dict = re.match(
        "data:(?P<type>.*?);(?P<encoding>.*?),(?P<data>.*)", image.image).groupdict()
    with open("imagetosave.jpeg", "wb") as fh:
        fh.write(base64.b64decode(img_dict['data'].encode()))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7200)
