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
            'variables': ['OS_UUID2', 'OS_UUID_PLAIN', 'OS_UUID_PLAIN2', 'OS_IP', 'OS_NUMBER', 'OS_UUID_PLAIN3', 'OS_UUID', 'OS_NUMBER2', 'OS_NUMBER3', 'OS_NUMBER4', 'OS_NUMBER5']
        },
        {
            'id': 25, 
            #'body': "[-] Lifecycle event OS_NUMBER on VM OS_UUID"
            'body': "\[-\] Lifecycle event (\d+) on VM ([\w\-]+)",
            'variables': ['OS_NUMBER', 'OS_UUID']
        },
        {
            'id': 27, 
            #'body': "[-] image OS_UUID at (/var/lib/nova/instances/_base/OS_UUID_PLAINOS_NUMBERcbfOS_NUMBER): checking"
            'body': "\[-\] image ([\w\-]+) at \(/var/lib/nova/instances/_base/(\w+)(\d+)cbf(\d+)\): checking",
            'variables': ['OS_UUID', 'OS_UUID_PLAIN', 'OS_NUMBER', 'OS_NUMBER2']
        },
        {
            'id': 28, 
            #'body': "[-] image OS_UUID at (/var/lib/nova/instances/_base/OS_UUID_PLAINOS_NUMBERcbfOS_NUMBER): in use: on this node OS_NUMBER local, OS_NUMBER on other nodes sharing this instance storage"
            'body': "\[-\] image ([\w\-]+) at \(/var/lib/nova/instances/_base/(\w+)(\d+)cbf(\d+)\): in use: on this node (\d+) local, (\d+) on other nodes sharing this instance storage",
            'variables': ['OS_UUID', 'OS_UUID_PLAIN', 'OS_NUMBER', 'OS_NUMBER2', 'OS_NUMBER3', 'OS_NUMBER4']
        },
        {
            'id': 29, 
            #'body': "[-] Active base files: /var/lib/nova/instances/_base/OS_UUID_PLAINOS_NUMBERcbfOS_NUMBER"
            'body': "\[-\] Active base files: /var/lib/nova/instances/_base/(\w+)(\d+)cbf(\d+)",
            'variables': ['OS_UUID_PLAIN', 'OS_NUMBER', 'OS_NUMBER2']
        },
        {
            'id': 30, 
            #'body': "Updating bandwidth usage cache"
            'body': "Updating bandwidth usage cache",
            'variables': []
        },
        {
            'id': 33, 
            #'body': "[-] [instance: OS_UUID] During sync_power_state the instance has a pending task. Skip.Updating bandwidth usage cache"
            'body': "\[-\] \[instance: ([\w\-]+)\] During sync_power_state the instance has a pending task. Skip.",
            'variables': ['OS_UUID']
        },
        {
            'id': 34, 
            #'body': "[-] Found OS_NUMBER in the database and OS_NUMBER on the hypervisor."
            'body': "\[-\] Found (\d+) in the database and (\d+) on the hypervisor.",
            'variables': ['OS_NUMBER', 'OS_NUMBER2']
        },
        {
            'id': 38, 
            #'body': "[req-OS_UUID OS_UUID_PLAIN OS_UUID_PLAIN] OS_IP "GET /vOS_NUMBER/OS_UUID_PLAIN/servers HTTP/OS_NUMBER" status: OS_NUMBER len: OS_NUMBER time: OS_NUMBER"
            'body': "\[req-([\w\-]+) (\w+) (\w+)\] (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) \\\"GET /v(\d+)/(\w+)/servers HTTP/(\d+\.\d+)\\\" status: (\d+) len: (\d+) time: (\d+\.\d+)",
            'variables': ['OS_UUID', 'OS_UUID_PLAIN', 'OS_UUID_PLAIN2', 'OS_IP', 'OS_NUMBER', 'OS_UUID_PLAIN3', 'OS_NUMBER2', 'OS_NUMBER3', 'OS_NUMBER4', 'OS_NUMBER5']
        },
        {
            'id': 39, 
            #'body': "[req-OS_UUID OS_UUID_PLAIN OS_UUID_PLAIN] OS_IP "DELETE /vOS_NUMBER/OS_UUID_PLAIN/servers/OS_UUID HTTP/OS_NUMBER" status: OS_NUMBER len: OS_NUMBER time: OS_NUMBER"
            'body': "\[req-([\w\-]+) (\w+) (\w+)\] (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) \\\"DELETE /v(\d+)/(\w+)/servers/([\w\-]+) HTTP/(\d+\.\d+)\\\" status: (\d+) len: (\d+) time: (\d+\.\d+)",
            'variables': ['OS_UUID2', 'OS_UUID_PLAIN', 'OS_UUID_PLAIN2', 'OS_IP', 'OS_NUMBER', 'OS_UUID_PLAIN3', 'OS_UUID', 'OS_NUMBER2', 'OS_NUMBER3', 'OS_NUMBER4', 'OS_NUMBER5']
        },
        {
            'id': 40, 
            #'body': "[req-OS_UUID OS_UUID_PLAIN OS_UUID_PLAIN] [instance: OS_UUID] Terminating instance"
            'body': "\[req-([\w\-]+) (\w+) (\w+)\] \[instance: ([\w\-]+)\] Terminating instance",
            'variables': ['OS_UUID2', 'OS_UUID_PLAIN', 'OS_UUID_PLAIN2', 'OS_UUID']
        },
        {
            'id': 41, 
            #'body': "[-] [instance: OS_UUID] Instance destroyed successfully."
            'body': "\[-\] \[instance: ([\w\-]+)\] Instance destroyed successfully.",
            'variables': ['OS_UUID']
        },
        {
            'id': 42, 
            #'body': "[req-OS_UUID OS_UUID_PLAIN OS_UUID_PLAIN] [instance: OS_UUID] Deleting instance files /var/lib/nova/instances/OS_UUID"
            'body': "\[req-([\w\-]+) (\w+) (\w+)\] \[instance: ([\w\-]+)\] Deleting instance files /var/lib/nova/instances/([\w\-]+)",
            'variables': ['OS_UUID2', 'OS_UUID_PLAIN', 'OS_UUID_PLAIN2', 'OS_UUID', 'OS_UUID3']
        },
        {
            'id': 43, 
            #'body': "[req-OS_UUID OS_UUID_PLAIN OS_UUID_PLAIN] [instance: OS_UUID] Deletion of /var/lib/nova/instances/OS_UUID complete"
            'body': "\[req-([\w\-]+) (\w+) (\w+)\] \[instance: ([\w\-]+)\] Deletion of /var/lib/nova/instances/([\w\-]+) complete",
            'variables': ['OS_UUID2', 'OS_UUID_PLAIN', 'OS_UUID_PLAIN2', 'OS_UUID', 'OS_UUID3']
        }        
]


# Create regular expression for log_templates
for t in log_templates:
    # print "template id"
    # print t['id']
    t['regex'] = re.compile(t['body'])

# Open the json file and the database file
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

# Extra columns
template_col = 'template_id integer'
uuid_col = 'uuid text'
osip_col = 'ip text'
extra_list = [template_col, uuid_col, osip_col]

# SAF key list
saf_key_list = ["eventno integer", 
                "eventtype text", 
                "timestamp integer", 
                "timestampusec integer", 
                "origin text"]

# # TEST: Add an extra column
# test_key_list = ["test integer"]

# SQL key list
sql_key_list = saf_key_list + key_list + extra_list
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
    temp_id = 0
    uuid = ''
    osip = ''
    ops_data_list = []
    for key, data in log_entry.items():
        # TEST: Identify message template
        if key == "message_body":
            # print "message_body"
            # print data
            for t in log_templates:
                matched = t['regex'].match(data)
                if matched:
                    # print "matched"
                    # print t['id']
                    temp_id = t['id']
                    for idx, obj in enumerate(t['variables']):
                        if obj == 'OS_UUID':
                            uuid = matched.group(idx + 1)
                        if obj == 'OS_IP':
                            osip = matched.group(idx + 1)
                    break
        ops_data_list.append(data)
    ops_data_list.append(temp_id)
    ops_data_list.append(uuid)
    ops_data_list.append(osip)    

    # # TEST: data list
    # test_data = cnt % 4 - 2
    # test_data_list = [test_data]

    data_list = saf_data_list + ops_data_list
    # data_list = saf_data_list + ops_data_list + test_data_list

    # Execute the SQL statement
    cursor.execute(data_insertion, data_list)

db_conn.commit()
db_conn.close()
        
