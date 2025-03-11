import scrapy
from lxml import html

class FlipkartMonitorsSpider(scrapy.Spider):
    name = "flipkart_monitors"
    allowed_domains = ["flipkart.com"]
    start_urls = ["https://www.flipkart.com/search?q=monitor&sid=6bo%2Cg0i%2C9no&as=on&as-show=on&otracker=AS_QueryStore_OrganicAutoSuggest_1_4_na_na_na&otracker1=AS_QueryStore_OrganicAutoSuggest_1_4_na_na_na&as-pos=1&as-type=RECENT&suggestionId=monitor%7CMonitors&requestId=6e496f8c-2acb-412c-a374-2cd146e28db0&as-searchtext=moni"]
    def start_requests(self):
        # url="https://www.flipkart.com/search?q=monitor&sid=6bo%2Cg0i%2C9no&as=on&as-show=on&otracker=AS_QueryStore_OrganicAutoSuggest_1_4_na_na_na&otracker1=AS_QueryStore_OrganicAutoSuggest_1_4_na_na_na&as-pos=1&as-type=RECENT&suggestionId=monitor%7CMonitors&requestId=6e496f8c-2acb-412c-a374-2cd146e28db0&as-searchtext=moni"
        url ="https://www.flipkart.com/search?q=monitor&sid=6bo%2Cg0i%2C9no&as=on&as-show=on&otracker=AS_QueryStore_OrganicAutoSuggest_1_4_na_na_na&otracker1=AS_QueryStore_OrganicAutoSuggest_1_4_na_na_na&as-pos=1&as-type=RECENT&suggestionId=monitor%7CMonitors&requestId=6e496f8c-2acb-412c-a374-2cd146e28db0&as-searchtext=moni&page=15"

        yield scrapy.Request(url=url, callback=self.parse)
     
  
    def parse(self, response):
        print(response.status)


        all_urls_list = response.xpath('//a[@class="CGtC98"]/@href').getall()
        print(all_urls_list)

        # headings = response.css("div[class*='KzDlHZ']::text").getall()
        # ratings = response.css("div.XQDdHH::text").getall()
        # price = response.css("div[class*='Nx9bqj _4b5DiR']::text").getall()
        # image = response.css("img[class*='DByuf4']::attr(src)").getall()
        # print(len(headings))
        # print(ratings)
        # print(price)
        # print(image)
        # for i in range(len(headings)):
        #     yield{
        #         "title":headings[i],
        #         "ratings":ratings[i],
        #         "price":price[i],
        #         "image":image[i]
        #     }
        #  # Find the "Next Page" button and follow it

        # # base_url = "https://www.flipkart.com/"

        # next_page = response.xpath('//nav[@class="WSL9JP"]//a[@class="_9QVEpD"][last()]/@href').get()
        # print("---------------")
        # print(next_page)

        # if next_page:
        #     new_url = response.urljoin(next_page)
        #     print("----------------------------------------" , new_url , "---------------------------------")
        #     print(new_url)
        #     yield scrapy.Request(url=new_url, callback=self.parse)
            