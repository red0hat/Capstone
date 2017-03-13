#!/Users/chris/anaconda/bin/python

import sys
import yaml
import os 
import re
import lib.database_module as db
import lib.download_mine as down
import tqdm
from sklearn.externals import joblib

def get_text(title):
    wiki_page = wikipedia_get_page(title)
    soup = BeautifulSoup(wiki_page[wiki_page.keys()[0]]['extract'], "html.parser")
    return soup.get_text()


def get_categories():
    """Read the arguments, and if there is a file in the arugments list, 
    assume it is a yaml file, and try to add it's contents"""
    db_location = None
    category_list = [ ]
    for arg in sys.argv[1:]:
        if os.path.isfile(arg):
            with open(arg, 'r') as f:
                category_list.extend(yaml.load(f)['category'])
        elif re.findall('location=', arg):
            db_location=  re.findall('location=(\w*)', arg)[0]
        else:
            category_list.append(arg)
    return category_list, db_location            



def main():
    # print command line arguments
    category_list, db_location = get_categories()
    pickled_transformer = joblib.load('data/vectorizer.pkl')
    for cate in tqdm.tqdm(category_list, desc="Downloading Categories"):
#    for cat in category_list.items():
        category = down.wikipedia_get_page(cate, category=True)
        cate_id = category.keys()[0]
        cate_name = cate
#        print cate_id, cate_name
        db.create_or_update_category_in_database(cate_id,cate_name,db_location)
        pages = down.wikipedia_get_pages_for_category(cate_name)
        for page in tqdm.tqdm(pages,desc='Downloading {}'.format(cate_name)):
            down.fetch_and_store_page(page[u'title'],
                                      page['pageid'],
                                      cate_id,db_location,
                                      pickled_transformer)
    db.delete_blank_page_text(db_location)



if __name__ == "__main__":
    main()

