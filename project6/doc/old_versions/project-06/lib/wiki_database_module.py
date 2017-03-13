#Created 2/1/2017 by Chris Peterson

import psycopg2
from database_connections import connect_to_postgres

def create_or_update_category_in_database ( category_id,category_name, location = 'remote'):
	"""
	This function will insert the values passed into the categories table in the wikipedia database.  
	If the category number matches a value in the table, the category title will be updated.
	"""

	connection, cursor = connect_to_postgres(location)
	update_sql = u"""
   	 	INSERT INTO category
    	(category_id, category_name) VALUES ({}, '{}')
    	on conflict (category_id) do 
    		UPDATE set category_name =excluded.category_name;
    	""".format(category_id, category_name)
	cursor.execute(update_sql)
	connection.commit()
	connection.close()


def create_or_update_page_in_database ( page_id, category_id, page_title, page_text,location = 'remote'):
	"""
	This function will insert the values passed into the page table in the wikipedia database.  
	If the page_id matches a value in the table, the page title and page text will be updated.
	"""

	connection, cursor = connect_to_postgres(location)
	insert_page = u"""
		INSERT INTO page (page_id, title, page)
		VALUES ({}, '{}', '{}')
		on conflict (page_id) do 
    		UPDATE set title ='{}', page = '{}';
	""".format(page_id, page_title, page_text,page_title,page_text)
	insert_page_cate = u"""
		INSERT INTO page_cate (page_id, category_id)
		VALUES ({}, {})
		on conflict do nothing;
	""".format(page_id, category_id)
	
	insert_page_status = cursor.execute(insert_page)
	insert_page_cate_status = cursor.execute(insert_page_cate)
	connection.commit()

	cursor.close()
	connection.close()
	#print "Insert page status: {}".format(insert_page_status)
	#print "Link page to category status: {}".format(insert_page_cate_status)

def select_pages ( page_ids = [], location = 'remote'):
	"""
	This function will return pages the have a pagid in the list 'page_ids'.  
	Set the location string to select the database to be used.
	"""
	page_ids = tuple(page_ids)  #converts the list 'page_ids' into a format the SQL likes.
	connection, cursor = connect_to_postgres(location)
	select_pages = u"""
	    SELECT page_id, title, page
	    FROM page
	    WHERE page_id IN {};
	    """.format(page_ids)

	returned_pages = cursor.fetchall()
	connection.commit()

	cursor.close()
	connection.close()
	return returned_pages

def select_categories_for_page ( page_id , location = 'remote'):
	"""
	This function will return categories for a page_id.  
	Set the location string to select the database to be used.
	"""
	connection, cursor = connect_to_postgres(location)
	select_category = u"""
    	SELECT category.category_name
    	FROM category
    	join page_cate
    	on page_cate.category_id = category.category_id
    	WHERE page_cate.page_id = {};
    	""".format(page_id)

	cursor.execute(select_category)
	returned_cate = cursor.fetchall()
	connection.commit()

	cursor.close()
	connection.close()
	return returned_cate	