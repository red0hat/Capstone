#!/Users/chris/anaconda/bin/python

import sys
import os 
import re
import lib.database_module as db
import lib.download_mine as down
import lib.encoding_module as en
from sklearn.externals import joblib
from sklearn.metrics.pairwise import cosine_similarity

def get_args():
    """Read the arguments, and if there is a file in the arugments list, 
    assume it is a text file and make it a string, and try to add it's contents
    Otherwise, add the words to a string to be searched.  If there is an argument 
    'location = <databse>', use that database location."""
    db_location = 'local'
    search_list = [ ]
    for arg in sys.argv[1:]:
        if os.path.isfile(arg):
            with open(arg, 'r') as f:
                search_list.append(f.read())
        elif re.findall('location=', arg):
            db_location=  re.findall('location=(\w*)', arg)[0]
        else:
            search_list.append(arg)
    return search_list, db_location            



def main():
    # print command line arguments
    search_list, db_location = get_args()

    pickled_transformer = joblib.load('data/vectorizer.pkl')
    search_vector = en.get_searchterm_vector(pickled_transformer,search_list[0])
    pages_vectors = db.select_all_page_vectors(location=db_location)
    vectors = [x[1] for x in pages_vectors]
    page_ids = [x[0] for x in pages_vectors]
    cos = cosine_similarity(vectors,search_vector[search_vector.keys()[0]])
    indices = cos.argsort(axis = 0)[-5:].ravel().tolist()
    indices.reverse()
    page_match_list = [(page_ids[i], cos[i]) for i in indices]
    temp_list =[]

    connection, cur, _ = db.connect_to_postgres(db_location)
    for page,score in page_match_list:
        sql = """SELECT title, page
                 FROM page
                 WHERE page_id = {};""".format(page)
        cur.execute(sql)
        temp = cur.fetchone()
        connection.commit()
        #print "Page title: {}\n{}\n\n".format(temp[0], temp[1][:250])
        temp_list.append( (temp[0], temp[1][:280], score))
        
    cur.close()
    connection.close()
        
    for result in temp_list:
        print "Page title: {}  Match Score: {:.2f}\n{}\n\n".format(result[0],(result[2][0])*100,result[1][:280].replace("\n"," "))



if __name__ == "__main__":
    main()

