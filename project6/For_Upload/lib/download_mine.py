import lib.database_module as db
from requests import get
from  bs4 import BeautifulSoup
import re

base_url = "https://en.wikipedia.org/w/api.php"

def create_query_param_string(params):
    param_list = [key+'='+value for key, value in params.items()]
    return '?'+'&'.join(param_list)
def wikipedia_page_format(page):
    return page.replace(' ','_')
def parse_pages_from_json(response_json):
    return response_json['query']['pages']
def parse_headings_from_json(response_json):
    return response_json['mobileview']['sections']


def wikipedia_get_page(title, category=False):
    """ Get the text of a wikipedia page"""
    
    params = { 'action' : 'query',
               'format' : 'json',
               'prop' : 'extracts',
               'exlimit' : 'maxl'
             }
    
    if category:
        title = "Category:"+title
        
    params['titles'] = wikipedia_page_format(title)
    query_param_string = create_query_param_string(params)
    response = get(base_url+query_param_string)
    
    return response.json()['query']['pages']

def wikipedia_by_pageid(pageid):
    """ Get the text of a wikipedia page"""
    
    params = { 'action' : 'query',
               'format' : 'json',
               'prop' : 'extracts',
               'exlimit' : 'maxl'
             }
    

    params['pageids'] = str(pageid)
    query_param_string = create_query_param_string(params)
    response = get(base_url+query_param_string)
    
    return response.json()['query']['pages']

def wikipedia_get_pages_for_category(category, continue_string=None):
    response_list = []
    
    params = { 'action' : 'query',
               'format' : 'json',
               'list' : 'categorymembers',
               'cmlimit' : 'max',
                
             }
    params['cmtitle'] = 'Category:'+wikipedia_page_format(category)
    if continue_string:
        params['cmcontinue'] = continue_string
        
    query_param_string = create_query_param_string(params)
    response = get(base_url+query_param_string)
    response_list = response.json()['query']['categorymembers']    
    if 'continue' in response.json().keys():
        response_list.extend(wikipedia_get_pages_for_category
                             (category,response.json()['continue']['cmcontinue'] ))
    return response_list
    
def fetch_and_store_page(title, page_id,category_number,db_location, transformer):
    if re.search('Category:',title):
            return None
    print "Storing", title, page_id
    text = get_text(page_id)
    title = title.replace('"','').replace("'","").replace(';','')
    text = text.replace('"','').replace("'","").replace(';','')
    if text == '':
        pass
    db.create_or_update_page_in_database(page_id,category_number,title,text,db_location)
    page_vector = list(transformer.transform([text])[0])
    db.create_or_update_page_vector(page_id, page_vector,db_location)

def get_text(page_id):
    wiki_page = wikipedia_by_pageid(str(page_id))
    soup = BeautifulSoup(wiki_page[wiki_page.keys()[0]]['extract'], "html.parser")
    return soup.get_text()

def fetch_and_store_category(category_name):
    if re.search('Category:',category_name):
            pass
    text = get_text(title)
    db.create_or_update_page_in_database(page_id,category_number,title,text,db_location)
