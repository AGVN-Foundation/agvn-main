import scrapy


class SocialSpider(scrapy.Spider):
    '''
    For scraping Social Media

    Facebook -> in div role="feed" take h1, h2, h3 and p tags
    Twitter -> in aria label="Timeline: Explore"
    '''
    name = "social"

    def start_requests(self):
        pass

    def parse(self, response):
        pass
