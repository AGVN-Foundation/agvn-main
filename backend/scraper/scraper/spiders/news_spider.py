import scrapy


class NewsSpider(scrapy.Spider):
    '''
    Extension: For scraping Social Media

    Facebook -> in div role="feed" take h1, h2, h3 and p tags
    Twitter -> in aria label="Timeline: Explore"
    '''
    name = "news"

    def start_requests(self):
        pass

    def parse(self, response):
        pass
        # if class or id 'content' exists, create an item called ContentItem
        # basically text = response.css('content *::text')

        # Algorithm
        # store all the text into ContentItem['content']
        # store the title as ContentItem['title']
        # if id or class 'author' or 'date' exists, store to ContentItem['author'|'date']
        # hook to it in pipelines and add to database as
