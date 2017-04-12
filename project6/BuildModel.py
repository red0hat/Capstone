#!/Users/chris/anaconda/bin/python

import sys
import os 
import re
import lib.database_module as db
import lib.download_mine as down
import lib.encoding_module as en
from sklearn.externals import joblib
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.pipeline import Pipeline
import tqdm

def get_args():
    """Read the arguments, Use the string as a file name for the model.
    If there is an argument 'location = <databse>', use that database location."""
    db_location = 'local'
    file_name = [ ]
    for arg in sys.argv[1:]:
        if re.findall('location=', arg):
            db_location=  re.findall('location=(\w*)', arg)[0]
        else:
            file_name.append(arg)
    if file_name == []:
        file_name = 'data/vectorizer.pkl'
    else:
        file_name = file_name.replace(' ','_')
    return file_name, db_location            



def main():
    # print command line arguments
    file_name, db_location = get_args()

    fetch_pages_sql = """
    SELECT page_id, page 
    FROM page
"""
    pages_text_temp = db.execute_sql_statement(fetch_pages_sql, db_location)
    
    pages_text_list = ([en.clean_page_text(p[1]) for p in 
                        tqdm.tqdm(pages_text_temp, desc = "Cleaning Pages")])
    
    vectorizer, vectors = en.build_vectorizer(pages_text_list)
    joblib.dump(vectorizer, 'data/vectorizer.pkl')
    y=[p[0] for p in pages_text_temp]
    vectors = zip(y,vectors)
    connection, cursor,_ = db.connect_to_postgres(db_location)
    sql_page_vector_delete = """
        DELETE from page_vec"""
    cursor.execute(sql_page_vector_delete)
    connection.commit()


    sql_page_vector = """INSERT INTO page_vec (page_id, page_vector)
            VALUES ({}, ARRAY{});""" 

    for v in tqdm.tqdm(vectors,desc = "Building Vectors"):
        cursor.execute(sql_page_vector.format(v[0], list(v[1])))
        connection.commit()
    cursor.close()
    connection.close()

    print "Created model at {}".format(file_name)


if __name__ == "__main__":
    main()

