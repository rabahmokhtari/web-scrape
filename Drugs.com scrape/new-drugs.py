from datetime import date

import requests
from bs4 import BeautifulSoup
import re
import json


f = open("drugs-{}.json".format(str(date.today())), "w+")
f.write('{ "druges" : [')


def process_page(url):
    print(url)
    request = requests.get(url)
    soup = BeautifulSoup(request.text, 'lxml')
    drugs_list = soup.find_all("div", class_="ddc-media-content")
    for drug in drugs_list:
        date_of_approval = re.findall("<b>Date of Approval: </b>(.*?)<br/>", str(drug).replace("\n", " "))
        if len(date_of_approval) == 1:
            date_of_approval = date_of_approval[0]
        else:
            date_of_approval = "NONE"
        treatment = re.findall("<b>Treatment for:</b>(.*?)<br/>", str(drug).replace("\n", " "))
        if len(treatment) == 1:
            treatment = treatment[0]
            soup = BeautifulSoup(treatment, 'html.parser')
            link_list = soup.findAll('a')
            if len(link_list) > 0:  # if treatments are present as href link
                treatment = link_list[0].text
                for el in link_list[1:]:
                    treatment = treatment + ',' + el.text
        else:
            treatment = "NONE"
        company = re.findall("<b>Company:</b>(.*?)<br/>", str(drug).replace("\n", " "))
        if len(company) == 1:
            company = company[0]
        else:
            company = "NONE"
        drug_title_h3 = drug.find("h3", class_="ddc-media-title").text
        drug_subtitle_p = drug.find("p", class_="drug-subtitle")
        # list_b = drug_subtitle_p.find_all('b')
        # print(drug_subtitle_p.text)
        if len(drug.find_all("p")) == 2:
            drug_description = drug.find_all("p")[1].text.replace('"', '\\"')
        else:
            drug_description = ''
        soup = BeautifulSoup(str(drug), 'lxml')
        previous_application_ul = soup.find_all("ul", class_="previous_application")
        if len(previous_application_ul) == 1:
            previous_application = previous_application_ul[0].text.replace('"', '\\"')
        else:
            previous_application = ''
        drug_json_data = '{' + '"title" : "{_title}",'.format(
            _title=drug_title_h3) + '"date_of_approval" :  "{_date_approv}",'.format(
            _date_approv=date_of_approval) + '"company": "{_company}",'.format(
            _company=company) + '"treatment": "{_treatment}",'.format(
            _treatment=treatment) + '"drug_description": "{_description}",'.format(
            _description=drug_description) + '"previous application": "{_previous_application}"'.format(
            _previous_application=previous_application) + '}'
        # print(drug_json_data)
        json_object = json.loads(drug_json_data.replace('\n', ' '), strict=False)
        json_formatted_str = json.dumps(json_object, indent=2)
        f.write(json_formatted_str + ",")


def process_all_url(first_year, last_year):
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october',
              'november', 'december']
    for year in range(first_year, last_year):
        for m in months:
            urlink = 'https://www.drugs.com/newdrugs-archive/{_month}-{_year}.html'.format(_month=m, _year=year)
            process_page(urlink)
    f.write(']}')
    f.close()



url = 'https://www.drugs.com/newdrugs-archive/april-2007.html'
url_list = []
# process_page(url)

process_all_url(2002, 2022)
