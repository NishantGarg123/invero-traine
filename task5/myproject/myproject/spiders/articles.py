import scrapy
import re


class ArticlesSpider(scrapy.Spider):
    name = "articles"
    # allowed_domains = ["3mindia.in"]
    # start_urls = ["https://3mindia.in"]
    header= {
               "accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/          signed-exchange;v=b3;q=0.7",
                "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
                }
    def start_requests(self):
        urls = [
           "https://www.3mindia.in/3M/en_IN/company-in/SDS-search/results/?gsaAction=msdsSRA&msdsLocale=en_IN&co=msds&q=*"
        ]
        
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse , headers=self.header)

    def parse(self, response):
        print(response.status)
        articles = response.xpath('//div[@id="MMM--searchResultItem"]')
        print(articles)
        
        for i in articles:    
            article_title = i.xpath('.//div[@class="MMM--hdg"]//text()').get()
            article_number= i.xpath('.//div[@class="MMM--searchResultItem-info"]//text()').get()
            #Extracton of the digits from the article_number
            pattern = r'\d{2}-\d{4}-\d{1}'
            article_number= re.findall(pattern,article_number)
            article_url= i.xpath('.//div/a/@href').get()
            yield{
               "article_title" :article_title,
               "article_number":article_number,
                "article_url": article_url
            }
            
        next_page = response.xpath('//div[@class="MMM--pagination"]//a//@data-url').get()
      
        if next_page:
            new_url = response.urljoin(next_page)
            print(new_url)
            yield scrapy.Request(url=new_url, callback=self.parse , headers=self.header)
            

