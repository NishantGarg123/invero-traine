import requests
import csv
from lxml import html
import re

url ="https://www.3mindia.in/3M/en_IN/company-in/SDS-search/results/?gsaAction=msdsSRA&msdsLocale=en_IN&co=msds&q=*"
base_add = "https://www.3mindia.in"
headers= {
"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
"referer":"https://www.3mindia.in/",
"accept-language":"en-US,en;q=0.9"
}



response = requests.get(url, headers= headers)
print(response)

#conversion html response to string
html_string = response.text
tree = html.fromstring(html_string)

articles = tree.xpath('//div[@id="MMM--searchResultItem"]')
print(articles)

with open("article_data.csv" , "w" , newline="" , encoding='utf-8') as article:
        writer = csv.writer(article)
        header = ["article-title" , "article-number" , "article-url"]
        writer.writerow(header)

        for i in articles:    
            article_title = i.xpath('.//div[@class="MMM--hdg"]//text()')
            print(article_title)
            
            article_number= i.xpath('.//div[@class="MMM--searchResultItem-info"]//text()')
            print(article_number)

            #Extracton of the digits from the article_number
            pattern = r'\d{2}-\d{4}-\d{1}'
            article_number= re.findall(pattern,article_number[0])
            print(article_number)

            
            article_url= i.xpath('.//div/a/@href')
            print(article_url)
    
            article_row = [article_title[0] , article_number[0] , article_url[0]]
            writer.writerow(article_row)


        # #extraction of data from the next page
        articles_done = 0
        while(articles_done <= 1488):
            print("next page :-")
            next_url = base_add+tree.xpath('//div[@class="MMM--pagination"]/a/@data-url')[0]
            articles_done =re.findall(r'\d{2,}$',next_url) 
            articles_done = int(articles_done[0])
            print("articles_done:-" , articles_done)
            print(next_url)
    
            response = requests.get(next_url, headers= headers)
            print(response)

            #conversion html response to string
            html_string = response.text
            tree = html.fromstring(html_string)

            if "start=96" in next_url:
                continue

            articles = tree.xpath('//div[@id="MMM--searchResultItem"]')
            for j in articles:    
                article_title = j.xpath('.//div[@class="MMM--hdg"]//text()')
                print(article_title)
                
                article_number= j.xpath('.//div[@class="MMM--searchResultItem-info"]//text()')
                print(article_number)

                 #Extracton of the digits from the article_number

                pattern = r'\d{2}-\d{4}-\d{1}'
                article_number= re.findall(pattern,article_number[0])
                print(article_number)


                
                article_url= j.xpath('.//div/a/@href')
                print(article_url)
        
                article_row = [article_title[0] , article_number[0], article_url[0]]
                writer.writerow(article_row)
                  
                






