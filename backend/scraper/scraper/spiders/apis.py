"""
List of APIs to fetch more urls from.
Also contains some titles which can be directly stored as well.
"""
import requests
from datetime import date
import os.path
import json
from dotenv import load_dotenv

# NOTE: NEWS_API can be queried 100 times/day

# for google news australia
load_dotenv()
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
G_NEWS_URL = f"https://newsapi.org/v2/top-headlines?sources=google-news-au&apiKey={NEWS_API_KEY}"

# for any topic, returns links to articles
def get_topic_news(TOPIC):
    return f"https://newsapi.org/v2/everything?q=f{TOPIC}&apiKey={NEWS_API_KEY}"


def fetch_top_news():
    """
    Current use case: run once daily
    """
    response = requests.get(G_NEWS_URL)
    return response.json()


def fetch_links_topic(TOPIC):
    """
    Run up to 100 times on specific topics
    """
    response = requests.get(get_topic_news())
    return response.json()


if __name__ == "__main__":
    """
    Sample fetch api and write to data
    """
    current_date = date.today().strftime("%d-%m-%Y")
    filename = f'../../data/api-urls-{current_date}.json'

    if not os.path.isfile(filename):
        json_response = fetch_top_news()

        with open(filename, 'w+') as f:
            f.write(json.dumps(json_response))
        print(f'Saved file {filename}')
    else:
        print(f'Already fetched on {current_date}')
    
    rawdata = None

    # algorithm to scrape news media
    # open filename and convert from json to dict
    # for each object in 'articles'
    #   take ['url']
    #   scrape url
