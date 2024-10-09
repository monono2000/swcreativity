import scrapy
import requests
import re
import time
import json
from scrapy.http import TextResponse
from scrapy.crawler import CrawlerProcess
import csv

class MusinsaItem(scrapy.Item):
    ranking = scrapy.Field()
    brand_name = scrapy.Field()
    product_name = scrapy.Field()
    product_num = scrapy.Field()
    product_spec = scrapy.Field()
    gender = scrapy.Field()
    origin_price = scrapy.Field()
    sale_price = scrapy.Field()
    good_num = scrapy.Field()
    review_count = scrapy.Field()
    target_name = scrapy.Field()
    link = scrapy.Field()

class MusinsaRankingSpider(scrapy.Spider):
    name = "MusinsaRanking"
    allowed_domains = ["store.musinsa.com"]
    
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'COOKIES_ENABLED': True,
        'DOWNLOAD_DELAY': 2,
        'DEFAULT_REQUEST_HEADERS': {
            'Referer': 'https://www.musinsa.com/',
            'Cookie': 'your_cookie_here',  # 여기에 로그인 후 가져온 쿠키 문자열을 삽입
        }
    }
    
    def __init__(self, category='001', last_page=5, *args, **kwargs):
        super(MusinsaRankingSpider, self).__init__(*args, **kwargs)
        self.category = category
        self.last_page = last_page
        self.start_urls = [
            f"https://www.musinsa.com/main/musinsa/ranking={self.category}&range=1w&list_kind=&page={page}&display_cnt=90"
            for page in range(1, self.last_page + 1)
        ]
        # Logging URLs for debugging
        for url in self.start_urls:
            self.log(f"Starting URL: {url}")
        # Slack Webhook Setup
        self.webhook_url = "https://hooks.slack.com/services/~~~"
        self.keyword = "THISISNEVERTHAT"
        # CSV File Setup
        self.csv_file = open('musinsa_data.csv', mode='w', newline='', encoding='utf-8')
        self.csv_writer = csv.writer(self.csv_file)
        self.csv_writer.writerow(["ranking", "brand_name", "product_name", "product_num", "product_spec", "gender", "origin_price", "sale_price", "good_num", "review_count", "target_name", "link"])
    
    def parse(self, response):
        links = response.xpath('//ul[@id=\"goodsRankList\"]/li/div/div[@class=\"box_contents\"]/div[@class=\"list_info\"]/a/@href').extract()
        links = [response.urljoin(link) for link in links]
        for link in links:
            time.sleep(1)  # Avoid getting blocked
            yield scrapy.Request(url=link, callback=self.parse_detail)
    
    def parse_detail(self, response):
        item = MusinsaItem()
        try:
            product_name_1 = response.xpath('//span[@class=\"product_title\"]/span[1]/text()').get()
            product_name_2 = response.xpath('//span[@class=\"product_title\"]/span[2]/text()').get()
            item["product_name"] = f"{product_name_1} {product_name_2}".replace("|", "")
        except:
            item["product_name"] = "-"
        
        item["brand_name"] = response.xpath('//p[@class=\"product_article_contents\"]/strong/a/text()').get(default="-")
        item["product_num"] = response.xpath('//ul[@class=\"product_article\"]/li/p/strong/text()').get(default="-")
        try:
            product_spec_1 = response.xpath('//div[@class=\"product_info\"]/p[@class=\"item_categories\"]/a[1]/text()').get()
            product_spec_2 = response.xpath('//div[@class=\"product_info\"]/p[@class=\"item_categories\"]/a[2]/text()').get()
            item["product_spec"] = f"{product_spec_1} / {product_spec_2}"
        except:
            item["product_spec"] = "-"
        
        gender = response.xpath('//p[@class=\"product_article_contents\"]/span[@class=\"txt_gender\"]/text()').getall()
        item["gender"] = "".join(gender).strip() if gender else "-"
        
        item["good_num"] = response.xpath('//span[@class=\"prd_like_cnt\"]/text()').get(default="-")
        item["review_count"] = response.xpath('//span[@class=\"review_count\"]/a/text()').get(default="-").replace("건", "")
        item["origin_price"] = response.xpath('//del[@class=\"original_price\"]/text()').get(default="기획전")
        item["sale_price"] = response.xpath('//span[@class=\"sale_price\"]/text()').get(default="기획전")
        target_name_1 = response.xpath('//strong[@class=\"age_group\"]/em/text()').get(default="")
        target_name_2 = response.xpath('//span[@class=\"gender\"]/text()').get(default="")
        item["target_name"] = f"{target_name_1} , {target_name_2}"
        item["link"] = response.url
        
        # Save to CSV
        try:
            self.csv_writer.writerow([item["ranking"], item["brand_name"], item["product_name"], item["product_num"], item["product_spec"], item["gender"], item["origin_price"], item["sale_price"], item["good_num"], item["review_count"], item["target_name"], item["link"]])
            self.log(f"Success: {item['product_name']} saved to CSV.")
        except Exception as e:
            self.log(f"Failure: Could not save {item['product_name']} to CSV. Error: {e}")
        
        # Send Slack Message if keyword matches
        if self.keyword in item["brand_name"]:
            self.send_slack_message(item)
        
        yield item
    
    def send_slack_message(self, item):
        message = (
            f"카테고리: {item['product_spec']}, 브랜드명: {item['brand_name']}, 상품명: {item['product_name']}, "
            f"판매가격: {item['origin_price']}, 세일가격: {item['sale_price']}, 좋아요: {item['good_num']}, 링크: {item['link']}"
        )
        payload = {
            "channel": "#musinsa_crawling",
            "username": "musinsa_bot",
            "text": message,
        }
        try:
            requests.post(self.webhook_url, json=payload)
            self.log(f"Success: Slack message sent for {item['product_name']}.")
        except Exception as e:
            self.log(f"Failure: Could not send Slack message for {item['product_name']}. Error: {e}")
        time.sleep(1)  # Avoid Slack rate limits

    def closed(self, reason):
        self.csv_file.close()

# Run the Scrapy Spider
process = CrawlerProcess({
    'FEEDS': {
        'musinsa_data.csv': {
            'format': 'csv',
            'overwrite': True,
        },
    },
    'AUTOTHROTTLE_ENABLED': True,
    'AUTOTHROTTLE_TARGET_CONCURRENCY': 2.0,
})

process.crawl(MusinsaRankingSpider, category='001', last_page=5)
process.start()
