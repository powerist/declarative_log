# -*- coding: utf-8 -*-

import sys
import dateutil.parser as dparser
import datetime
import pytz
import re

import json
import sqlite3

from template import log_templates

# Openstack log patterns
log_templates = [
        {
            'id': 0,
            #'body': "(OS_NUMBER) accepted ('OS_IP', OS_NUMBER)"
            'body': "\[-\] \((\d+)\) accepted \('(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', (\d+)\)",
            'variables': ['OS_NUMBER', 'OS_IP', 'OS_NUMBER2']
        },
        {
            'id': 1,
            #'body': "[-] Starting new HTTP connection (OS_NUMBER): OS_IP"
            'body': "\[-\] Starting new HTTP connection \((\d+)\): (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})",
            'variables': ['OS_NUMBER', 'OS_IP']
        },
        {
            'id': 3, 
            #'body': "[-] Auditing locally available compute resources"
            'body': "\[-\] Auditing locally available compute resources",
            'variables': []
        },
        {
            'id': 4, 
            #'body': "[-] Free ram (MB): OS_NUMBER"
            'body': "\[-\] Free ram \(MB\): (\d+)",
            'variables': ['OS_NUMBER']
        },
        {
            'id': 5, 
            #'body': "[-] Free disk (GB): OS_NUMBER"
            'body': "\[-\] Free disk \(GB\): (\d+)",
            'variables': ['OS_NUMBER']
        },
        {
            'id': 6, 
            #'body': "[-] Free VCPUS: OS_NUMBER"
            'body': "\[-\] Free VCPUS: (\d+)",
            'variables': ['OS_NUMBER']
        },
        {
            'id': 8, 
            #'body': "[-] Compute_service record updated for OS_IP:OS_IP"
            'body': "\[-\] Compute_service record updated for OS_IP: (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})",
            'variables': ['OS_IP']
        },
        {
            'id': 13, 
            #'body': "[req-OS_UUID OS_UUID_PLAIN OS_UUID_PLAIN] OS_IP "GET /vOS_NUMBER/OS_UUID_PLAIN/servers/OS_UUID HTTP/OS_NUMBER" status: OS_NUMBER len: OS_NUMBER time: OS_NUMBER"
            'body': "\[req-([\w\-]+) (\w+) (\w+)\] (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) \\\"GET /v(\d+)/(\w+)/servers/([\w\-]+) HTTP/(\d+\.\d+)\\\" status: (\d+) len: (\d+) time: (\d+\.\d+)",
            'variables': ['OS_UUID', 'OS_UUID_PLAIN', 'OS_UUID_PLAIN', 'OS_IP', 'OS_NUMBER', 'OS_UUID_PLAIN', 'OS_UUID', 'OS_NUMBER', 'OS_NUMBER', 'OS_NUMBER', 'OS_NUMBER']
        }
]


# Create regular expression for log_templates
for t in log_templates:
    t['regex'] = re.compile(t['body'])


json_file = "delete-0.log"
sqlite_file = "delete.db"

traffic = json.load(open(json_file))
db_conn = sqlite3.connect(sqlite_file)

# Get database schema
# Log key list
sample_entry = traffic[0]
key_list = sample_entry.keys()
datatype = "text"
# Pre-process schemas of the log
for n,key in enumerate(key_list):
    # Get rid of '@' in the key
    if key.startswith('@'):
        new_key = key.replace('@', 'aT')
        key_list[n] = new_key
    
    column_name = key_list[n]
    column_prefix = "ops_"
    key_list[n] = column_prefix + column_name + " " + datatype

# SAF key list
saf_key_list = ["eventno integer", 
                "eventtype text", 
                "timestamp integer", 
                "timestampusec integer", 
                "origin text"]

# # TEST: Add an extra column
# test_key_list = ["test integer"]

# SQL key list
sql_key_list = saf_key_list + key_list
# sql_key_list = saf_key_list + key_list + test_key_list
sql_key_count = len(sql_key_list)
sql_key_string = ', '.join(sql_key_list)

# print key_count
# print key_string
# print sql_key_count
# print sql_key_string
# sys.exit()

# Create the database table
# TODO: avoid hardcoding table schemas
cursor = db_conn.cursor()
table_name = 'network_log'
deletion_query = 'drop table if exists ' + table_name
cursor.execute(deletion_query)
creation_query = 'create table ' + table_name + ' (' + sql_key_string + ')'
#print creation_query
cursor.execute(creation_query)

# Data insertion template
placeholders = ['?'] * sql_key_count
placeholder_string = ', '.join(placeholders)
data_insertion = 'insert into ' + table_name + ' values(' + placeholder_string + ')'

# Process log data and insert the data into the database
saf_event_type = "OpenStackDelete"
saf_origin = ""
for cnt, log_entry in enumerate(traffic):
    #print log_entry
    #print '\n'

    # Process SAF event attributes
    saf_data_list = []
    saf_data_list.append(cnt)
    saf_data_list.append(saf_event_type)

    # Parse timestamp in logs
    utc_time = log_entry["@timestamp"]
    parsed_time = dparser.parse(utc_time)
    epoch_naive = datetime.datetime.fromtimestamp(0)
    epoch_aware = epoch_naive.replace(tzinfo=pytz.UTC)
    delta_time = parsed_time - epoch_aware
    timestamp_delta = delta_time.total_seconds()
    timestamp_seconds = int(timestamp_delta)
    timestamp_micro_seconds = timestamp_delta * 1000000
    saf_data_list.append(timestamp_seconds)
    saf_data_list.append(timestamp_micro_seconds)
    
    saf_data_list.append(saf_origin)

    # Process Openstack data
    ops_data_list = []
    for key, data in log_entry.items():
        # TEST: Identify message template
        if key == "message_body":
            print "message_body"
            print data
            for t in log_templates:
                matched = t['regex'].match(data)
                if matched:
                    print "Matched!ID: ", t['id']
                    break
        # ops_data_list.append(data)

    # # TEST: data list
    # test_data = cnt % 4 - 2
    # test_data_list = [test_data]

    data_list = saf_data_list + ops_data_list
    # data_list = saf_data_list + ops_data_list + test_data_list

    # Execute the SQL statement
    # cursor.execute(data_insertion, data_list)

db_conn.commit()
db_conn.close()
        
