from xml.etree.ElementTree import ElementTree
import requests
import pandas as pd
import requests
from bs4 import BeautifulSoup
from lxml import etree # To help parse through the soup with XPaths.

class Webscraper:
    def __init__(self, template, placeholder = None, values = []): # values is a two_dimensional list.
        self.template = template
        self.values = values
        if placeholder:
            self.template = self.template.replace(placeholder, "{}")
        self.dataframe = pd.DataFrame()

    def scrape(self, content = {}):
        all_added_observations = []
        print("Self.values: ", self.values)
        for value_list in self.values:
            URL = self.template.format(*value_list)
            page = requests.get(URL)
            print(URL)

            soup = BeautifulSoup(page.content, "html.parser")

            # Use of CSS Selector
            results = soup.select('#mw-content-text > div > table:nth-child(2) > tbody > tr:nth-child(1) > td > table > tbody > tr:nth-child(1) > td > table > tbody > tr > td:nth-child(2) > i')
            print(len(results))
            for r in results:
                print(r.text)
            dom = etree.HTML(str(soup))

        print(all_added_observations)
        
            # content in the format of
            # {columnHeader: {xpath: full_xPath,
            #                 multiples: True/False}} If multiples is true, there are multiple points of interest with the same xpath (scrape all).

# Webscraper("mywebsite.{}/{}", "[]", [["gov", "confidential"], ["com", "nonconfidential"]]) 

# Example Link https://bulbapedia.bulbagarden.net/wiki/Bulbasaur_(Pok%C3%A9mon)
# Say I want to scrape Japanese name and catch rate.
'''
My template would be https://bulbapedia.bulbagarden.net/wiki/{}_(Pok%C3%A9mon), where placeholder is {}.

I want the Japanese name and catch rate, so the content will be

content = {
        "jap_name" : {
            "xpath": r"/html/body/div[2]/div[1]/div[3]/div[5]/div[4]/div/table[2]/tbody/tr[1]/td/table/tbody/tr[1]/td/table/tbody/tr/td[2]/span/b"
            "multiples": False
        },
        "catch_rate": {
            "xpath": r"//*[@id="mw-content-text"]/div/table[2]/tbody/tr[1]/td/table/tbody/tr[1]/td/table/tbody/tr/td[2]/span/b/span"
            "multiples": False
        }

    }

So if I give it the values "Bulbasaur" and "Beedril", what do I expect to get?

I expect a data frame with

[search] | [jap_name] | [catch_rate]
Bulbasaur| xxxxx      | xxxxx
Beedril  | xxxxx      | xxxxx

'''
# TEST RUN
wb = Webscraper("https://bulbapedia.bulbagarden.net/wiki/[]_(Pok%C3%A9mon)", "[]", [["Bulbasaur"], ["Beedrill"], ["Charizard"], ["Lopunny"], ["Pikachu"]])

content = {
    "jap_name" : {"xpath": r'''//*[@id="mw-content-text"]/div/table[2]/tbody/tr[1]/td/table/tbody/tr[1]/td/table/tbody/tr/td[2]/span/b/span''',
            "multiples": False
        },
    "catch_rate": {
            "xpath": r"/html/body/div[2]/div[1]/div[3]/div[5]/div[4]/div/table[2]/tbody/tr[4]/td[2]/table/tbody/tr/td/small/span",
            "multiples": False
        }}

wb.scrape(content)