from datetime import date
import re
import os

try:
    import requests
    from bs4 import BeautifulSoup
    import json
except Exception as e:
    os.system("pip install bs4")
    os.system("pip install requests")
    import requests
    from bs4 import BeautifulSoup
    import json
    
f = open("direcrtory-{}.json".format(str(date.today())), encoding='utf-8', mode= "w+")


class Dcciinfo:
    def __init__(self):
        self.directory = '{ "directory" : ['
        self.all_category_urls = self.get_category_urls()

    def get_category_urls(self):
        urls = []
        c = 'A'
        for i in range(1, 27):
            urls.append("https://dcciinfo.ae/categories/" + c)
            c = chr(ord(c) + 1)
        return urls

    def process_company(self, url):
        print(url)
        request = requests.get(url)
        soup = BeautifulSoup(request.text, 'lxml')
        branches = soup.find_all("div", class_="col-lg-6")
        company_title = soup.find_all("div", class_="top-title")[0].text
        company_json = '{' + f'"title" : "{company_title}", "branches": ['

        for br in branches:
            br_title = br.find_all("div", class_="comp-box-header")[0].text
            infos = br.find_all("div", class_="col-9")
            if len(infos) != 0:
                phone = infos[0].text
                fax = infos[1].text
                box = infos[2].text
                city = infos[3].text
                area = infos[4].text
                website = re.findall('href="(.*?)"', str(infos[5]))
                address = infos[6].text
            else:
                phone = fax = box = city = area = website = address = ""
            if len(website) == 0:
                website = ""
            company_json = company_json + '{' \
                                          f'"title": "{br_title}",' \
                                          f'"phone": "{phone}",' \
                                          f'"fax": "{fax}",' \
                                          f'"box": "{box}",' \
                                          f'"city": "{city}",' \
                                          f'"area": "{area}",' \
                                          f'"website": "{website}",' \
                                          f'"address": "{address}"' \
                                          '},'
        company_json = company_json + ']}'
        company_json = company_json.replace('\n', '').replace(',]', ']')
        self.directory = self.directory + company_json + ','

    def process_category(self, cateory_url):
        request = requests.get(cateory_url)
        soup = BeautifulSoup(request.text, 'lxml')
        companies = soup.find_all("div", class_="col-xs-12 col-sm-12")[0]
        companies_url_refs = companies.find_all("div", class_="col-12 col-md-6 col-xl-4")
        for url_ref in companies_url_refs:
            url = re.findall('<a href="(.*?)"', str(url_ref))
            if len(url) != 0:
                self.process_company(url[0])

    def process_all_category(self):
        for cateory_url in self.all_category_urls:
            self.process_category(cateory_url)
        self.directory = self.directory + ']'
        self.directory = self.directory.replace(',]', ']')
        f.write(str(self.directory))


Dcciinfo().process_all_category()
