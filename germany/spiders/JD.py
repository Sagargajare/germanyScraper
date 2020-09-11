import json
import os
import urllib

import scrapy
# from scrapy_splash import SplashRequest
import subprocess
import re
import random
global h
import time
global h , data
import requests
from bs4 import BeautifulSoup
# with open("1.json","r") as file:
#     data = json.load(file)
# # data = json.loads(data)
# h =3550
# from items import SprojectItem
class GermanyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    No = scrapy.Field()
    url = scrapy.Field()
    Adresse = scrapy.Field()
    Wohnfläche = scrapy.Field()
    Grundstück = scrapy.Field()
    Typ = scrapy.Field()
    Zimmer =scrapy.Field()
    Baujahr = scrapy.Field()
    Modernisierung =scrapy.Field()
    Wesentliche = scrapy.Field()
    Heizungsart = scrapy.Field()
    Energiebedarf = scrapy.Field()
    Energieeffizienzklasse = scrapy.Field()
    Objektbeschreibung = scrapy.Field()
    Ausstattung = scrapy.Field()
    Lage = scrapy.Field()

def proxy_generator():
    response = requests.get("https://sslproxies.org/")
    soup = BeautifulSoup(response.content, 'html.parser')
    proxy = {'https': random.choice(list(map(lambda x: x[0] + ':' + x[1], list(zip(map(lambda x:x.text,
	   soup.findAll('td')[::8]), map(lambda x:x.text, soup.findAll('td')[1::8]))))))}


def proxy_find():
    proxies = []
    res = requests.get('https://free-proxy-list.net/', headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(res.text, "lxml")

    for items in soup.select("#proxylisttable tbody tr")[:15]:
        proxy_list = ':'.join([item.text for item in items.select("td")[:2]])
        proxies.append(f"{proxy_list}")
    proxies = list(filter(is_bad_proxy,proxies))
    print(proxies)
    # proxies = ['46.158.200.233:53281', '59.120.117.244:80', '142.44.221.126:8080', '162.243.175.14:80', '92.247.168.74:8080',
    #  '37.139.125.110:8080', '162.144.44.140:3838', '162.144.81.84:3838']

    return proxies
def is_bad_proxy(pip):
    try:
        proxy_handler = urllib.request.ProxyHandler({'http': pip})
        opener = urllib.request.build_opener(proxy_handler)
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        urllib.request.install_opener(opener)
        sock = urllib.request.urlopen('http://www.google.com')  # change the url address here
        # sock=urllib.urlopen(req)
    except urllib.error.HTTPError as e:
        print('Error code: ', e.code)
        return e.code
    except Exception as detail:

        print("ERROR:", detail)
        return 1
    return 0


class JdSpider(scrapy.Spider):
    name = 'JD'

    # start_urls = ['https://www.immobilienscout24.de/expose/121423633#/', 'https://www.immobilienscout24.de/expose/121389152#/',]

    def __init__(self,  n = 0 ,url_and_no={}, **kwargs):

        self.n = n
        # print(load())
        self.url_and_no = url_and_no
        self.start_urls = []
        # self.proxies = proxy_find()

        super().__init__(**kwargs)

    # https://www.immobilienscout24.de/Suche/de/haus-kaufen?pagenumber=2

    def start_requests(self):
        self.start_urls =[self.url_and_no[f"{self.n}"]]
        for url in self.start_urls:
            # res = requests.get("https://gimmeproxy.com/api/getProxy")
            # data = res.json()
            # print(pprint.pprint((res.json())))
            # print(data["ipPort"])
            # proxy = data["ipPort"]

                # print(proxy_list)
            # if self.proxy_pool:
                # req.meta['proxy'] = random.choice(self.proxy_pool)
            proxy = "confettihunter99@gmail.com:Persona99@au473.nordvpn.com"
            yield scrapy.Request(url=url, callback=self.parse,meta={'dont_merge_cookies': True, 'dont_filter': False})

    custom_settings = {
        'DUPEFILTER_CLASS': 'scrapy.dupefilters.BaseDupeFilter',
        'FEED_URI': 'output.csv', 'FEED_FORMAT': 'csv',
        'HTTPERROR_ALLOW_ALL': True,
    }

    def parse(self, response):
        # .is24qa-wohnflaeche


        url = response.url
        # global h
        # print(h)
        # print(url)
        #address-block
        address = response.css("div.address-block")
        address = [x.css("span::text").extract() for x in address]
        qualify = True
        x = 0
        try:
            address = "".join(address[0])
            print(address)

        except:


            url = self.url_and_no[f"{self.n}"]
            qualify = False
            print(url)
            print("------------------Proxy Change-----------____________")

            city = random.choice(["berlin", "paris", "london", "tokyo", "Istanbul", "mumbai", ])
            print(f"-------{self.n}----------------ERROR-----{self.n}--------------")
            process = subprocess.Popen(['nordvpn', 'connect', f'{city}'],
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
            print(stdout, stderr)
            x = x + 1
            if x>6:
                return

            yield scrapy.Request(url=url, callback=self.parse,meta={'dont_merge_cookies': True, 'dont_filter': True,})


            # return scrapy.Request(url=url, callback=self.parse, meta={'dont_merge_cookies': True, 'dont_filter': False})
        if qualify or x>5:
            x=0

            items = GermanyItem()
            try:
                Wohnfläche = response.css("div.is24qa-wohnflaeche::text").extract()[0]
                # print(Wohnfläche)
            except:
                Wohnfläche = " "
            try:
                Grundstück = response.css('div.is24qa-grundstueck::text').extract()[0]
                # print(Grundstück)
            except:
                Grundstück = " "
            try:
                Typ = response.css("dd.is24qa-typ::text").extract()[0]
                # print(Typ)
            except:
                Typ=""

            try:
                Zimmer = response.css("dd.is24qa-zimmer::text").extract()[0]
                # print(Zimmer)
            except:
                Zimmer=""

            # .is24qa-baujahr
            try:
                Baujahr = response.css("dd.is24qa-baujahr::text").extract()[0]
                # print(Baujahr)
            except:
                Baujahr =""

            try:
                renovation = response.css("dd.is24qa-objektzustand::text").extract()[0]
                # print(renovation)
            except:
                renovation = ""
            try:
                Wesentliche = response.css("dd.is24qa-wesentliche-energietraeger::text").extract()[0]
                # print(Wesentliche)
            except:
                Wesentliche = " "

            # .is24qa-heizungsart
            try:
                Heizungsart = response.css("dd.is24qa-heizungsart::text").extract()[0]
                # print(Heizungsart)
            except:
                Heizungsart = " "


            try:
                Energy_Demand = response.css("dd.is24qa-endenergiebedarf::text").extract()[0]
            except:
                Energy_Demand = " "


            try:
                Energy_class = response.css("dd.is24qa-energieeffizienzklasse::text").extract()[0]
                # print(Energy_class)
            except:
                Energy_class = " "


            try:
                End_energie_verbrauch = response.css("dd.is24qa-endenergieverbrauch::text").extract()[0]
                # print(End_energie_verbrauch)
            except:
                End_energie_verbrauch = " "


            try:
                renovation = response.css("dd.is24qa-objektzustand::text").extract()[0]
                # print(renovation)
            except:
                renovation = " "

            try:
                Objektbeschreibung = response.css("pre.is24qa-objektbeschreibung::text").extract()[0]
                # print(Objektbeschreibung)
            except:
                Objektbeschreibung = " "

            try:
                Ausstattung = response.css("pre.is24qa-ausstattung::text").extract()[0]
                # print(Ausstattung)
            except:
                Ausstattung = " "
            # .is24qa-lage
            try:
                 lage = response.css("pre.is24qa-lage::text").extract()[0]
                 # print(lage)
            except:
                lage =" "

            items["No"] = self.n
            items["url"] = url
            items["Adresse"] = address
            items["Wohnfläche"] = Wohnfläche
            items["Grundstück"] = Grundstück
            items["Typ"] = Typ
            items["Zimmer"] = Zimmer
            items["Baujahr"] = Baujahr
            items["Modernisierung"] = renovation
            items["Wesentliche"] = Wesentliche
            items["Heizungsart"] = Heizungsart
            items["Energiebedarf"] = Energy_Demand
            items["Energieeffizienzklasse"] = Energy_class
            items["Objektbeschreibung"] = Objektbeschreibung
            items["Ausstattung"] = Ausstattung
            items["Lage"] = lage

            # yield items
            yield {"No.": self.n,
                    "url":url,
                   "Adresse": address,
                   "Wohnfläche":Wohnfläche,
                   "Grundstück":Grundstück,
                   "Typ":Typ,
                   "Zimmer":Zimmer,
                   "Baujahr":Baujahr,
                   "Modernisierung":renovation,
                   "Wesentliche":Wesentliche,
                   "Heizungsart":Heizungsart,
                    "Energiebedarf":Energy_Demand,
                   "Energieeffizienzklasse":Energy_class,
                   "Objektbeschreibung":Objektbeschreibung,
                   "Ausstattung":Ausstattung,
                   "Lage":lage,}
            self.n = self.n + 1
            # url = data[f"{h}"]
            # h = h + 1
            url = self.url_and_no[f"{self.n}"]
            yield scrapy.Request(url=url, callback=self.parse,meta={'dont_merge_cookies': True, 'dont_filter': True})
        # if not qualify:


