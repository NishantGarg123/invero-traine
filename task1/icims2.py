from dexi_io_scrappers import extract_url
import re
import scrapy
import json
import math
import requests
from lxml import html
from scrapy.selector import Selector
from lxml import etree
from dexi_io_scrappers.items import DexiIoScrappersItem
from datetime import datetime
from dexi_io_scrappers.DexiBaseSpider import DexiBaseSpider

class careerjobs2(DexiBaseSpider):
    name = 'icims2' 

    def get_articles(self, company_url):
        if company_url.strip()[-1] != "/":
            company_url = company_url.strip() + "/"
        final_urls = []
        base_url = "/".join(company_url.split("/")[:3])
        domain = company_url.split("/")[2].split(".")[1]
        search_key_list = extract_url.job_board_search_keywords(self.job_board)
        print("-----------------------------------------------")
        print("company url " , company_url)
        print(" search key  = " , search_key_list)
        print("-----------------------------------------------")
        for search_key in search_key_list:
            # main_url = f"{base_url}/api/jobs?keywords={search_key}&sortBy=relevance&page=1&internal=false&deviceId=undefined&
            # domain={domain}.jibeapply.com"        
            main_url = f"https://jobs.intuit.com/search-jobs/results?ActiveFacetID=0&CurrentPage=1&RecordsPerPage=15&TotalContentResults=&Distance=50&RadiusUnitType=0&Keywords=&Location=&ShowRadius=False&IsPagination=False&CustomFacetName=&FacetTerm=&FacetType=0&SearchResultsModuleName=Search+Results&SearchFiltersModuleName=Search+Filters&SortCriteria=0&SortDirection=0&SearchType=5&RefinedKeywords%5B0%5D={search_key}&PostalCode=&ResultsType=0&fc=&fl=&fcf=&afc=&afl=&afcf=&TotalContentPages=NaN"
            print("-----------------------------------------------")
            print(" Outer main_url = " , main_url)  
            print("-----------------------------------------------")
            res = requests.get(main_url)
            try:
                print("-----------------------------------------------\n")
                print("We are with in the try case")
                print("-----------------------------------------------\n")
                json_part = json.loads(res.text)
            except:
                print("-----------------------------------------------\n")
                print("We are with in the try case")
                print("-----------------------------------------------\n")
                json_part = None
            
            print("-----------------------------------------------\n")
            # print("Json_part_value = " , json_part)
            print("-----------------------------------------------\n")
            if json_part is None:
                # https://jobs.intuit.com/search-jobs/
                main_url = f"{company_url}search?ss=1&in_iframe=1&searchKeyword={search_key}"
                res = requests.get(main_url)
                print("-----------------------------------------------")
                print("response"  , res , "\n")
                print(" Inner main_url = " , main_url , "\n")
                print("res.text =" , res.url)
                print("-----------------------------------------------\n")
                res = html.fromstring(res.text)
                title_list = res.xpath('//div[@class="col-xs-12 title"]//h3//text()')
                url_list = res.xpath('//div[@class="col-xs-12 title"]//a//@href')
                if title_list:
                    pass
                else:
                    title_list = res.xpath('//section[@id="search-results-list"]//ul//li//a//h2//text()')
                if url_list:
                    pass
                else:
                    url_list = res.xpath('//section[@id="search-results-list"]//ul//li//a/@href')

                print("-----------------------------------------------\n")
                print("title_list ->" , title_list)
                print("-----------------------------------------------\n")
                print("url_list ->" , url_list)
                print("-----------------------------------------------\n")
                count = 0
                for title in title_list:
                    if extract_url.validate_title(title, job_board=self.job_board):
                        job_url = url_list[count]
                        final_urls.append(job_url)
                    count += 1
            else:

              

                print("-----------------------------------------------\n")
                print("We are with in the else case")
                print("-----------------------------------------------\n")

                # print("Json result data", json_part['results'])
                # resultant_data =  json_part['results']
                html_data = json_part.get("results", "")
                # parser = etree.HTMLParser()
                # tree = etree.fromstring(html_data, parser)

                # formatted_html = etree.tostring(tree, pretty_print=True, encoding="unicode")
                # print(formatted_html)
                # print("-----------------------------------------------\n")
                # print("Json result data",html_data)
                # print("-----------------------------------------------\n")

                
                html_selector = Selector(text=html_data)
                filtered_by_text = html_selector.xpath("//section[@id='search-results-list']//ul//li").getall()
                title = filtered_by_text.xpath("//h2//text()")
                print("-----------------------------------------------\n")
                print("filtered data" , filtered_by_text)
                print("-----------------------------------------------\n")
                

                # for job in json_part['results']:
                #     print("jobs = " , job['attorney'])
                # for job in json_part["jobs"]:
                #     title = job["data"]["title"]
                #     job_id = job["data"]["req_id"]
                #     if extract_url.validate_title(title, job_board=self.job_board):
                #         job_url = company_url + job_id + "?lang=en-us"
                #         final_urls.append(job_url)
                # total_count = json_part["totalCount"]
                # if total_count >10:
                #     no_of_page = math.ceil(total_count/10)
                #     for i in range(2, no_of_page+1):
                #         main_url = f"{base_url}/api/jobs?keywords={search_key}&sortBy=relevance&page={i}&internal=false&deviceId=undefined&domain={domain}.jibeapply.com"
                #         res = requests.get(main_url)
                #         json_part = json.loads(res.text)
                #         for job in json_part["jobs"]:
                #             title = job["data"]["title"]
                #             job_id = job["data"]["req_id"]
                #             if extract_url.validate_title(title, job_board=self.job_board):
                #                 job_url = company_url + job_id + "?lang=en-us"
                #                 final_urls.append(job_url)                
        
        print(final_urls,"------------final_urls")
        return final_urls

    def get_articles_callback(self, response):
        print("**************************")
        url_list = self.get_articles(response.meta["search_url"])
        
        for url in url_list:
            yield scrapy.Request(url=url, callback=self.parse, meta=response.meta)

    def parse(self, response):
        company_name = response.meta['company_name']
        industry = response.meta['job_category']
        search_url = response.meta['search_url']

        response_dict = re.findall(
            r'<script> window.jobDescriptionConfig = (.*?); </script>',
            response.text
        )
        if len(response_dict) == 0:
            response_dict = re.findall(
            r'application\/ld\+json\">(.*?)<\/script>',
            response.text
        )
            if len(response_dict) == 0:
                return
            data = json.loads(response_dict[0])
            title = data['title']

            reference =  response.url.split('/')[4]
            
            job_url = data['url']
            description = data['description']

            country = ""
            try:
                country = data['jobLocation'][0]['address']['addressCountry']
                if 'UNAVAILABLE' in country:
                    country = ""
            except:
                country = ""


            if 'jobLocation' not in data:
                location = "CHECK LOCATION" 
            elif len(data['jobLocation']) > 1:
                count = 1
                reference_append = ""
                for locations in data['jobLocation']:
                    if count == 1:
                        reference_append = ""
                    else:
                        reference_append = "-"+str(count)

                    location = '{}, {}'.format(
                        locations['address']['addressLocality'],
                        locations['address']['addressRegion'],
                    )
                    if 'UNAVAILABLE' not in location:
                        data = {
                            "title": title.strip(),
                            "companyName": company_name.strip(),
                            "location": location,
                            "country" : country,
                            "reference": re.sub('[^A-Za-z0-9]+', '', company_name.replace(' ', '') + reference.strip()) + reference_append ,
                            "description": description,
                            "category": industry,
                            "company": "",
                            "url": job_url.strip(),
                            "searchUrl": search_url,
                            "expiration_date": "",
                            "expiry": "",
                            "scrapyd_job_id": self.scrapyd_job_id
                        }
                        yield data
                        count += 1
            else:
                location = '{}, {}'.format(
                    data['jobLocation'][0]['address']['addressLocality'],
                    data['jobLocation'][0]['address']['addressRegion'],
                )
                if 'UNAVAILABLE' in location and 'Remote' not in location:
                    try:
                        location_dict = re.findall(r'var icimsSD = (.*?);', response.text)
                        location_data = json.loads(location_dict[0])
                        location = location_data['job']['location']
                    except:
                        location = 'NO LOCATION'

                if location == '(All)':
                    try:
                        location = '{}-{}-{}'.format(
                            data['jobLocation'][1]['address']['addressCountry'],
                            data['jobLocation'][1]['address']['addressRegion'],
                            data['jobLocation'][1]['address']['addressLocality'],
                        )
                    except:
                        location = 'NO LOCATION'
                    
                
                
                data = {
                    "title": title.strip(),
                    "companyName": company_name.strip(),
                    "location": location,
                    "country" : country,
                    "reference": re.sub('[^A-Za-z0-9]+', '', company_name.replace(' ', '') + reference.strip()),
                    "description":  description,
                    "category": industry,
                    "company": "",
                    "url": job_url.strip(),
                    "searchUrl": search_url,
                    "expiration_date": "",
                    "expiry": "",
                    "scrapyd_job_id": self.scrapyd_job_id
                }
                yield data
        else:
            data = json.loads(response_dict[0])

            title = data["job"]['title']
            
            reference =  data["job"]['req_id']

            job_url = response.url
            description = data["job"]['description']

            location_list = []
            if "full_location" in data["job"]:
                location_list = data["job"]['full_location'].split(";")
            elif "location_name" in data["job"]:
                location_list.append(data["job"]['location_name'])
            else:
                location_list.append(data["job"]['short_location'])
            country = data["job"]['country']

            count = 1
            reference_append = ""
            for loc in location_list:
                if count == 1:
                    reference_append = ""
                else:
                    reference_append = "-"+str(count)
                data = {
                    "title": title.strip(),
                    "companyName": company_name.strip(),
                    "location": loc,
                    "country" : country,
                    "reference": company_name.replace(' ', '') + reference.strip() + reference_append,
                    "description":  description,
                    "category": industry,
                    "company": "",
                    "url": job_url,
                    "searchUrl": search_url,
                    "expiration_date": "",
                    "expiry": "",
                    "scrapyd_job_id": self.scrapyd_job_id
                }
                yield data
                count += 1