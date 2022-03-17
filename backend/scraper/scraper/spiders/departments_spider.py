import scrapy


class DepartmentSpider(scrapy.Spider):
    '''
    For scraping Department information (h1, p tags)
    Extension: search google for each state's departments, and scrape first page's links
    '''
    name = "department"

    def start_requests(self):
        # scrape federal department links

        urls = {
            # Federal
            'fed': 'https://www.directory.gov.au/departments-and-agencies',

            # ACT
            'act': 'https://www.act.gov.au/',

            # NSW
            'nsw': 'https://www.service.nsw.gov.au/nswgovdirectory/departments',

            # VIC
            'vic': 'https://w.www.vic.gov.au/contactsandservices/directory/',

            # SA
            'sa': 'https://www.sa.gov.au/topics/about-sa/government',

            # TAS
            'tas': 'https://www.lgat.tas.gov.au/',

            # WA
            'wa': 'https://www.wa.gov.au/service',

            # QLD
            'qld': 'https://www.qld.gov.au/about/how-government-works/government-structure',

            # NT
            'nt': 'https://nt.gov.au/',
        }

    def parse(self, response):

        # types of links found across the pages
        link_types = ['.row[role=list]', '.tile-grid__item', '']
        link_types = list(map(lambda x: x+' a::attr(href)', link_types))

        # write data
        filename = f'data/departments/raw'
        with open(filename, 'a') as f:
            out = response.css('content *::text').extract()
            # response.body.decode("utf-8")
            f.write(out)
        self.log(f'Saved file {filename}')

        for link_type in link_types:
            can_crawl = response.css(link_type)
            if can_crawl:
                yield response.follow(can_crawl, callback=self.parse)
