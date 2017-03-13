
#Created 2/1/2017 by Chris Peterson and Suketu Kothari
#modified 2/5/2017
#Version : 1.1 release candidate 1

import psycopg2
import yaml
import re

### TO DO: abstract the error handling to function. The Return from a select or insert will be the sticky wicket.

def create_or_update_category_in_database ( category_id,category_name, location = 'remote'):
	"""
	This function will insert the values passed into the categories table in the wikipedia database.  
	If the category number matches a value in the table, the category title will be updated.
	"""

	update_sql = u"""
        INSERT INTO category
        (category_id, category_name) VALUES ({}, '{}')
        on conflict (category_id) do 
        UPDATE set category_name =excluded.category_name;
        """.format(category_id, category_name)
	try:
		connection, cursor, _ = connect_to_postgres(location)
		cursor.execute(update_sql)
		connection.commit()
		cursor.close()
		connection.close()
		return "OK"
	except psycopg2.Error as e:
		connection.rollback()
		cursor.close()
		connection.close()
		return e.pgerror


def create_or_update_page_in_database ( page_id, category_id, page_title, page_text,location = 'remote'):
	"""
	This function will insert the values passed into the page table in the wikipedia database.  
	If the page_id matches a value in the table, the page title and page text will be updated.
	"""
   	insert_page = u"""
        INSERT INTO page (page_id, title, page)
        VALUES ({}, '{}', '{}')
        on conflict (page_id) do 
            UPDATE set title ='{}', page = '{}';
    """.format(page_id, page_title, page_text, page_title, page_text)

    	insert_page_cate = u"""
		INSERT INTO page_cate (page_id, category_id)
		VALUES ({}, {})
		on conflict do nothing;
    """.format(page_id, category_id)
	try:
	    connection, cursor, _ = connect_to_postgres(location)
	    cursor.execute(insert_page)
	    cursor.execute(insert_page_cate)
	    connection.commit()
	    cursor.close()
	    connection.close()
	    return "OK"
	except psycopg2.Error as e:
	    connection.rollback()
	    cursor.close()
	    connection.close()
    	return e.pgerror

def select_pages ( page_ids, location = 'remote'):
	"""
	This function will return pages the have a pagid in the list 'page_ids'.  
	Set the location string to select the database to be used.
	"""
	if len(page_ids) ==1:
		page_ids = page_ids *2
	page_ids = tuple(page_ids)  #converts the list 'page_ids' into a format the SQL likes.
	
	select_pages_sql = u"""
	    SELECT DISTINCT page_id, title, page
	    FROM page
	    WHERE page_id IN {};
	    """.format(page_ids)
	try:
	    connection, cursor, _ = connect_to_postgres(location)
	    cursor.execute(select_pages_sql)
	    returned_pages = cursor.fetchall()
	    connection.commit()
	    cursor.close()
	    connection.close()
	    return returned_pages
	except psycopg2.Error as e:
	    connection.rollback()
	    cursor.close()
	    connection.close()
    	return e.pgerror

def select_categories_for_page ( page_id , location = 'remote'):
	"""
	This function will return categories for a page_id.  
	Set the location string to select the database to be used.
	"""

	select_category_sql = u"""
    	SELECT category.category_name, category.category_id 
    	FROM category
    	join page_cate
    	on page_cate.category_id = category.category_id
    	WHERE page_cate.page_id = {};
    	""".format(page_id)

	try:
	    connection, cursor, _ = connect_to_postgres(location)
	    cursor.execute(select_category_sql)
	    returned_cate = cursor.fetchall()
	    connection.commit()
	    cursor.close()
	    connection.close()
	    return returned_cate	
	except psycopg2.Error as e:
	    connection.rollback()
	    cursor.close()
	    connection.close()
	    return e.pgerror

def connect_to_postgres (location = 'remote'):
    """ v 1.2 Open a psycopg2 connection and create a cursor based on a yaml credential file.
        The current expected name of the yaml file is "Database_credentials"; please customize this to your taste.
        The credentials file will look for a entry in the dictionary called 'remote' by default.  If the remote
        databse is unavailalbe, it will attempt to connect with the settings the 'local' key.  
        Please remember to close the cursor and connection when you are done using them.        
    """
#TO DO: make  'location' to a list and iterate through the list, rather than default to local db.
#TO DO: add credential file support as a param for the function call.


    with open('data/credentials.yml', 'r') as f:
        credentials =  yaml.load(f) 
    
    try:
        connection = psycopg2.connect(**credentials[location])
        return connection, connection.cursor(), "Connected to server {}.".format(credentials[location]['host'])
    except:
        print 'FAILED to connect to server {}.  Trying local server.'.format(credentials[location]['host'])
        try:
            connection = psycopg2.connect(**credentials['local'])
            return connection, connection.cursor(), "Connected to server {}.".format(credentials[location]['local']) 
        except:
            print "No Database is available"
            pass 

def execute_sql_statement ( sql_select, location = 'remote'):
	"""
	This function will return run an arbitrary SQL select command.
	"""
#	if  re.search('^[select]', sql_select.lower()) and not re.search(';(?!$)',sql_select):
#	    print "OK"
#	else:
#	    raise ValueError('The SELECT statment is not valid: {}'.format(sql_select))
#
	try:
	    connection, cursor, _ = connect_to_postgres(location)
	    cursor.execute(sql_select)
	    returned_cate = cursor.fetchall()
	    connection.commit()
	    cursor.close()
	    connection.close()
	    return returned_cate	
	except psycopg2.Error as e:
	    connection.rollback()
	    cursor.close()
	    connection.close()
	    return e.pgerror

def select_all_page_vectors ( location = 'remote'):
	"""
	This function will return all page vectors, and page_ids.
	"""
	select_page_vectors_sql = u"""
    	SELECT * FROM page_vec
    	"""

	try:
	    connection, cursor, _ = connect_to_postgres(location)
	    cursor.execute(select_page_vectors_sql)
	    page_vectors = cursor.fetchall()
	    connection.commit()
	    cursor.close()
	    connection.close()
	    return page_vectors	
	except psycopg2.Error as e:
	    connection.rollback()
	    cursor.close()
	    connection.close()
	    return e.pgerror

def select_page_vectors ( page_ids, location = 'remote'):
	"""
	This function will return page vectors that have a pagid in the list 'page_ids'.  
	Set the location string to select the database to be used.
	"""
	if len(page_ids) ==1:
		page_ids = page_ids *2
	page_ids = tuple(page_ids)  #converts the list 'page_ids' into a format the SQL likes.
	
	select_page_vectors_sql = u"""
	    SELECT DISTINCT page_id, page_vec
	    FROM page_vec
	    WHERE page_id IN {};
	    """.format(page_ids)
	try:
	    connection, cursor, _ = connect_to_postgres(location)
	    cursor.execute(select_page_vectors_sql)
	    returned_pages = cursor.fetchall()
	    connection.commit()
	    cursor.close()
	    connection.close()
	    return returned_pages
	except psycopg2.Error as e:
	    connection.rollback()
	    cursor.close()
	    connection.close()
    	return e.pgerror


def select_all_category_vectors ( location = 'remote'):
	"""
	This function will return all category vectors, and category_ids.
	"""
	select_category_vectors_sql = u"""
    	SELECT * FROM cate_vec
    	"""

	try:
	    connection, cursor, _ = connect_to_postgres(location)
	    cursor.execute(select_category_vectors_sql)
	    category_vectors = cursor.fetchall()
	    connection.commit()
	    cursor.close()
	    connection.close()
	    return category_vectors	
	except psycopg2.Error as e:
	    connection.rollback()
	    cursor.close()
	    connection.close()
	    return e.pgerror

def select_category_vectors ( cagetgory_ids , location = 'remote'):
	"""
	This function will return category vectors that have a category id in the list 'categoru_ids'.  
	Set the location string to select the database to be used.
	"""
	if len(cagetgory_ids) ==1:
		cagetgory_ids = cagetgory_ids *2
	cagetgory_ids = tuple(cagetgory_ids)  #converts the list 'categoru_ids' into a format the SQL likes.
	
	select_category_vectors_sql = u"""
	    SELECT DISTINCT category_id, cate_vec
	    FROM cate_vec
	    WHERE category_id IN {};
	    """.format(cagetgory_ids)
	try:
	    connection, cursor, _ = connect_to_postgres(location)
	    cursor.execute(select_category_vectors_sql)
	    returned_vectors = cursor.fetchall()
	    connection.commit()
	    cursor.close()
	    connection.close()
	    return returned_vectors
	except psycopg2.Error as e:
	    connection.rollback()
	    cursor.close()
	    connection.close()
    	return e.pgerror

def delete_blank_page_text (location = 'remote'):
	"""
	This function will delete page records where there is no page text.
	"""
   	drop_pages = u"""DELETE FROM page_cate WHERE page_id IN
  					(SELECT page_id FROM page WHERE page = '' OR page is NULL);
					DELETE FROM page_vec WHERE page_id IN
  					(SELECT page_id FROM page WHERE page = '' OR page is NULL);                    
					DELETE FROM page WHERE page = '' OR page is NULL;"""

	try:
	    connection, cursor, _ = connect_to_postgres(location)
	    cursor.execute(drop_pages)
	    connection.commit()
	    cursor.close()
	    connection.close()
	    return "OK"
	except psycopg2.Error as e:
	    connection.rollback()
	    cursor.close()
	    connection.close()
    	return e.pgerror

def create_or_update_page_vector ( page_id, page_vector,location = 'remote'):
	"""
	This function will insert the values passed into the page table in the wikipedia database.  
	If the page_id matches a value in the table, the page title and page text will be updated.
	"""
	sql_page_vector = """INSERT INTO page_vec (page_id, page_vector)
           VALUES ({}, ARRAY{})
           on conflict do nothing;""".format(page_id, page_vector)
	try:
	    connection, cursor, _ = connect_to_postgres(location)
	    cursor.execute(sql_page_vector)
	    connection.commit()
	    cursor.close()
	    connection.close()
	    return "OK"
	except psycopg2.Error as e:
	    connection.rollback()
	    cursor.close()
	    connection.close()
    	return e.pgerror

def fetch_all_category_vectors(location = 'remote'):
	sql_category_vectors = """select t2.category_id, t1.page_vector 
							from page_vec as t1
							join page_cate as t2
							on t1.page_id = t2.page_id;"""
	try:
	    connection, cursor, _ = connect_to_postgres(location)
	    cursor.execute(sql_category_vectors)
	    returned_vectors = cursor.fetchall()
	    connection.commit()
	    cursor.close()
	    connection.close()
	    return returned_vectors
	except psycopg2.Error as e:
	    connection.rollback()
	    cursor.close()
	    connection.close()
    	return e.pgerror

def fetch_all_category_pages(location = 'remote'):
	sql_category_pages = """select t2.category_id, t1.page
							from page as t1
							join page_cate as t2
							on t1.page_id = t2.page_id;"""
	try:
	    connection, cursor, _ = connect_to_postgres(location)
	    cursor.execute(sql_category_pages)
	    returned_vectors = cursor.fetchall()
	    connection.commit()
	    cursor.close()
	    connection.close()
	    return returned_vectors
	except psycopg2.Error as e:
	    connection.rollback()
	    cursor.close()
	    connection.close()
    	return e.pgerror
