# -*- coding: utf-8 -*-
import scrapy
from newspaper import Article
from nyt.items import NytItem
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor

class NytcrawlerSpider(CrawlSpider):
    name = 'nytcrawler'
    custom_settings = {
        'CLOSESPIDER_ITEMCOUNT': 500,
    }    
    idx = 0
    allowed_domains = ['www.nytimes.com']
    start_urls = ['https://www.nytimes.com/section/world/europe']
    rules = (Rule(LinkExtractor(allow=[r'https://www\.nytimes\.com/\d{4}/\d{2}/\d{2}/world/europe/[a-z-]+\.html$']), callback="parse_item", follow=True),)
    def parse_item(self, response):
        self.log("Scraping: " + response.url)

        article = Article(url=response.url)
        article.download()
        article.parse()

        item = NytItem()
        item['url'] = response.url
        item['authors'] = article.authors
        item['title'] = article.title
        item['text'] = article.text

        f = open('articles/%d-%s'%(self.idx,article.title), 'w', encoding='utf8')
        if len(article.authors) > 0:
            for index in range(len(article.authors)-1):
                f.write(article.authors[index]+', ')
            f.write(article.authors[len(article.authors)-1])
        else:
            f.write('Unknown Author')
        f.write('\n')
        f.write(response.url)
        f.write('\n')
        f.write(article.text)
        f.close()
        self.idx+=1
        return item