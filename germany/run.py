from scrapy.crawler import CrawlerProcess
# from JD import JdSpider
import json


from scrapy.utils.project import get_project_settings

from spiders.JD import JdSpider

urls = []
start = int(input("Starting Point :- "))
with open("spiders/total.json") as file:
    data = json.load(file)
for i in range(start,100):
    url = data[f"{i}"]
    urls.append(url)


if __name__ == "__main__":



    process = CrawlerProcess(get_project_settings())
    process.crawl(JdSpider, n = start,url_and_no = data)
    process.start()

