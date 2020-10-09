import datetime
import re

import requests

def get_lost_found_text():
    url = 'http://advisory.mtanyct.info/LPUWebServices/CurrentLostProperty.aspx'
    response = requests.get(url)
    
    return response.text

def parse_category(category_text):
    category_name = re.search(r'Category="(.*?)"',
                              category_text).group(1)
    
    subcategories = re.findall(r'<SubCategory SubCategory="(.*?)" count="(\d+)"/>',
                               category_text)
    
    parsed = [(subcategory, category_name, count) for subcategory, count in subcategories]
    
    return parsed


def parse_lost_claimed(text):
    lost_regex = re.compile(r'<NumberOfLostArticles>(\d+)</NumberOfLostArticles>')
    claimed_regex = re.compile(r'<NumberOfItemsclaimed>(\d+)</NumberOfItemsclaimed>')
    
    lost = lost_regex.search(text).group(1)
    claimed = claimed_regex.search(text).group(1)
    
    return lost, claimed

def parse_categories(text):
    category_regex = re.compile(r'(<Category.*?</Category>)')
    categories = category_regex.findall(text)
    
    subcategory_info = [parse_category(category) for category in categories]
    subcategory_flat = [x for subcategory in subcategory_info for x in subcategory]
    
    return subcategory_flat

def parse_lost_found(text):
    
    lost, claimed = parse_lost_claimed(text)
    
    subcategory_flat = parse_categories(text)
    
    return {'now': datetime.datetime.now(), 'lost': lost, 'claimed': claimed, 'subcategories': subcategory_flat}


def query_lost_found_api():
  
    text = get_lost_found_text()
    return parse_lost_found(text)