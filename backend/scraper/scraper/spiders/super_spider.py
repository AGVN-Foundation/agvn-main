import scrapy
from .apis import G_NEWS_URL, get_topic_news, fetch_top_news
import json
from datetime import date
import os.path
import os


class SuperSpider(scrapy.Spider):
    '''
    Used as a complete spider that calls sub spiders:
        main_crawler = CrawlerProcess()
        main_crawler.crawl(Spider1)
        main_crawler.crawl(Spider2)
        main_crawler.start()
    '''
    # name for this spider
    name = "super"

    def start_requests(self):
        '''
        Read today's api urls, then go to each url and scrape everything on there
        Extension: go to twitter and search for all the hash tags and scrape everything
        '''
        current_date = date.today().strftime("%d-%m-%Y")

        # check if scraped data already exists for today
        scraped_filename = f'data/scraped-data-{current_date}.json'
        if os.path.isfile(scraped_filename):
            exit("Already scraped today... Exiting")

        api_filename = f'data/api-urls-{current_date}.json'

        if not os.path.isfile(api_filename):
            print(f'Have not fetched on {current_date}')
            json_response = fetch_top_news()

            with open(api_filename, 'r') as f:
                f.write(json.dumps(json_response))
            print(f'Saved file {api_filename}')
        else:
            print(f'Already fetched on {current_date}')

        # read and parse data as dict
        print('Reading from:', api_filename)
        with open(api_filename, 'r') as f:
            api_data = f.read()
            data = json.loads(api_data)
        
        os.mkdir('data/'+current_date)

        # fetch articles and each url
        urls = [a['url'] for a in data['articles']]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        '''
        Parse everything. Take everything in between tags.
        '''
        current_date = date.today().strftime("%d-%m-%Y")
        page = response.url.split('/')
        page = page[3] + page[4] + page[5] + '.txt'

        # write data
        filename = f'data/{current_date}/{page}'
        with open(filename, 'w+') as f:
            out = response.css('content *::text').extract()
            # response.body.decode("utf-8")
            f.write(out)
        self.log(f'Saved file {filename}')
