from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.pipeline import Pipeline
import string
import re
import gensim

def clean_page_text(page):
    """Clean the returns from Wikipedia api calls.
       This cleaned text is used for creating vectors and vectorizing model. 
       most numbers are eliminated.  """
    temp = page.replace('\n',' ')
    temp = temp.lower()
    temp = re.sub(r'\[[0-9]{1,8}\]',' ', temp) #reference links
    temp = re.sub(r'[0-9]{2,8}|[0-9]{1,8}.[0-9]{1,8}|[0-9]{1,3}\%',' ', temp) #get rid of some numbers.
    temp = re.sub(r"external|references|links",' ', temp) #remove some common wikipedia words 
    temp = re.sub(r"\\xe2\\x80\\x94|\\xe2\\x80\\x99s|\\xc3\\x97|\\xe2\\x80\\x9",' ', temp) #remove some unicode punctuation
    temp = re.sub(r"\\xe2\\x80\\x94|\\xe2\\x80\\x99s|\\xc3\\x97|\\xe2\\x80\\x9",' ', temp) #remove some unicode punctuation

    temp = re.sub(r"\\xe2\\x80\\x99s",' ', temp) #remove some unicode punctuation
    temp = re.sub(r"\\xc3\\x97|\\xe2\\x80\\x9",' ', temp) #remove some unicode punctuation

    punctuation = string.punctuation
    blank_list = ' '*len(punctuation)
    trantab = string.maketrans(punctuation, blank_list)
    temp = temp.translate(trantab)
    lemma_text = " ".join(str(x)[:-3] for x in gensim.utils.lemmatize(temp))
    return lemma_text



def build_vectorizer(clean_pages):
    '''
    this function takes a list of clean pages. 
    It returns a fit svd transformer, and the vectroized pages.
    '''
    vectorizer = TfidfVectorizer(stop_words = 'english',        
                                 use_idf=True,
                                 smooth_idf=True,
                                 #strip_accents = 'ascii', 
                                 max_df = 0.5,
                                 norm = 'l1',)
    svd = TruncatedSVD(n_components=500,algorithm='randomized',n_iter=10)
    svd_trans = Pipeline([('tfidf', vectorizer), 
                            ('svd', svd)])
    vectors = svd_trans.fit_transform(clean_pages)
    return svd_trans, vectors

def get_page_vector(transformer,clean_pages,page_ids):
    '''
    this function takes a trained svd transformer and returns a dictionary with string
    page_id's (input as a list in same order as clean_pages) as keys and page vectors
    as values.
    '''
    page_vecs = {}
    for page_id,page in zip(page_ids,clean_pages):
        page_vecs[page_id] = transformer.transform([page])
        
    return page_vecs

def get_searchterm_vector(transformer,searchterm):
    '''
    this function takes a trained svd transformer and a single string search
    term. It returns the vectorized search term with the searchterm as its key.
    '''
    search_vec = {}
    search_vec[searchterm] = transformer.transform([searchterm])
    return search_vec

def get_cat_vector(transformer,clean_pages_in_cat,cat):
    '''
    this function takes a trained svd transformer, a category, and all the pages in a cateogry(list)(cleaned),
    combines the pages into one "document" and transforms that document into a vector. 
    '''
    category_doc_string = ''
    for doc in clean_pages_in_cat:
        category_doc_string += doc
    return {cat:transformer.transform([category_doc_string])}





