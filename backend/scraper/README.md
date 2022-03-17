## What is Scraper?
![](Scraper-Logo.png)

Scraper is a web scraper that automatically crawls across search engines, social media for data
Scraper is set to run daily by /webserver

#### How to Use
`cd /backend/scraper`
`scrapy crawl super`
This runs the web scraper to scrape some juicy info from the web

Note: subject to change. Will eventually make use of scrapy pipeline.

To run the api fetching operation directly,
`python scraper/spiders/api.py`

#### Direct Database Insertion
Scrapy will directly insert dynamically fetched data into `mongodb`.
It is up to Machine Learning scripts to interface with `mongodb` to fetch the string data.
You can use GPT-Neo, NLTK to extract the sentiment from this data. Then pass it to `/webserver`.

#### File Structure
`/spiders` contain the web scraping logic that you implement
`spiders/apis.py` contain api keys and links that you can fetch from

#### Notes
To help with web scraping, I will list out some things we should do:

First: go to the [Australian Departments Page](https://www.directory.gov.au/departments-and-agencies)

Next: select the class `"views-content"`.

For each table row `<tr>`, select the corresponding `<a>` tag. Scrape the `href` value and add it to list of department urls.

Make a dictionary -> map each `url` to an empty string `""`.

For each department url, GET the page and and select the `field-items even` class. Scrape the text in between this div. Add this text to `dictionary["url"]`.

Convert dictionary to JSON object and pass it to mongoDB table `Departments`.

*Do something similar with [State](https://www.nsw.gov.au/department-of-premier-and-cabinet) and [Local](https://en.wikipedia.org/wiki/Local_government_in_Australia) departments*. Basically, fetch the main information that summarizes these departments.

## Scrapyd HTTP API
`scrapyd` is an open source scrapy server API. It is useful for actual deployment. We will have to transition to this model later on from our custom FASTAPI server.

#### Twitter
- GET trends/place

#### General
- Items for news, social media and departments.
- Spiders for news, social media and departments.
- Pipelines for news, social media and departments.
- Call all spiders from super_spider.

#### Australian Government
- https://api.gov.au/definitions/api/
