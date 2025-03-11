import scrapy
from lxml import html

class FlipkartMonitorsSpider(scrapy.Spider):
    name = "flipkart_monitors"
    allowed_domains = ["flipkart.com"]
    start_urls = ["https://www.flipkart.com/search?q=monitor&sid=6bo%2Cg0i%2C9no&as=on&as-show=on&otracker=AS_QueryStore_OrganicAutoSuggest_1_4_na_na_na&otracker1=AS_QueryStore_OrganicAutoSuggest_1_4_na_na_na&as-pos=1&as-type=RECENT&suggestionId=monitor%7CMonitors&requestId=6e496f8c-2acb-412c-a374-2cd146e28db0&as-searchtext=moni"]
    j=0
    def start_requests(self):
        # url="https://www.flipkart.com/search?q=monitor&sid=6bo%2Cg0i%2C9no&as=on&as-show=on&otracker=AS_QueryStore_OrganicAutoSuggest_1_4_na_na_na&otracker1=AS_QueryStore_OrganicAutoSuggest_1_4_na_na_na&as-pos=1&as-type=RECENT&suggestionId=monitor%7CMonitors&requestId=6e496f8c-2acb-412c-a374-2cd146e28db0&as-searchtext=moni"
        url ="https://www.flipkart.com/search?q=monitor&sid=6bo%2Cg0i%2C9no&as=on&as-show=on&otracker=AS_QueryStore_OrganicAutoSuggest_1_4_na_na_na&otracker1=AS_QueryStore_OrganicAutoSuggest_1_4_na_na_na&as-pos=1&as-type=RECENT&suggestionId=monitor%7CMonitors&requestId=6e496f8c-2acb-412c-a374-2cd146e28db0&as-searchtext=moni&page=15"

        yield scrapy.Request(url=url, callback=self.parse)
     
    flag =0
    def parse(self, response):
        print(response.status)
        if(self.flag ==0 ):
            all_urls_list = response.xpath('//a[@class="CGtC98"]/@href').getall()
            # print(all_urls_list)
            self.flag =1
            for i in range( len(all_urls_list)):
                new_url = response.urljoin(all_urls_list[i])
                yield scrapy.Request(url=new_url, callback=self.parse)
        else:
            specification_title = response.xpath('((//table[@class="_0ZhAN9"]//tr[@class="WJdYP6 row"]//td[@class="+fFi1w col col-3-12"])[position() <= 12])//text()').getall()
            specification_title_value = response.xpath('((//table[@class="_0ZhAN9"]//tr[@class="WJdYP6 row"]//li[@class="HPETK2"])[position() <=12])//text()').getall()
            print("------------------------------------------------------------------------------------------------------")
            print("specification_title",specification_title)
            print("specification_title_value",specification_title_value)
            for i in range(len(specification_title)):
                yield{
                        "system":response.url,
                        "specification_title":specification_title[i],
                        "specification_title_value": specification_title_value[i]
                    }

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
            