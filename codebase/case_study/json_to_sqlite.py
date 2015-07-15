# -*- coding: utf-8 -*-

import json
import sqlite3

json_file = "delete-0.log"
sqlite_file = "delete.db"

traffic = json.load(open(json_file))
db_conn = sqlite3.connect(sqlite_file)

# Get database schema
sample_entry = traffic[0]
key_list = sample_entry.keys()
# Get rid of '@' in the key
for n,key in enumerate(key_list):
    if key.startswith('@'):
        new_key = key.replace('@', 'aT')
        key_list[n] = new_key
key_count = len(key_list)
key_string = ', '.join(key_list)

#print key_count
#print key_string

# Create the database table
# TODO: avoid hardcoding table schemas
cursor = db_conn.cursor()
table_name = 'network_log'
deletion_query = 'drop table if exists ' + table_name
cursor.execute(deletion_query)
creation_query = 'create table ' + table_name + ' (' + key_string + ')'
#print creation_query
cursor.execute(creation_query)

# Data insertion template
placeholders = ['?'] * key_count
placeholder_string = ', '.join(placeholders)
data_insertion = 'insert into ' + table_name + ' values(' + placeholder_string + ')'
# Insert the data into the database
for log_entry in traffic:
    #print log_entry
    #print '\n'
    data_list = []
    for key, data in log_entry.items():
        data_list.append(data)
    cursor.execute(data_insertion, data_list)

#selection_query = 'select * from ' + table_name
#cursor.execute(selection_query)

db_conn.commit()
db_conn.close()
        
