###############################################################
# Script  
#	NOVADELETE
#
# Domain  
#	USERMODELS
#
# Description       
# 	Test logs of OpenStack
#
# Constraints Specified
#	 None
#
# Output    
#	Outputs event sequences that represent novadelete actions
#
# Output Event Name
#	 OpenStack
#
#Output Attributes     

############################################################### 
[header]
NAMESPACE = USERMODELS
NAME = NOVADELETE
QUALIFIER = {}

[states]
event_1 = {template_id = 0, ip = $1}
event_2 = {template_id = 38, ip = $event_1.ip}
event_3 = {template_id = 13, ip = $event_2.ip}
event_4 = {template_id = 39, ip = $event_3.ip}
event_5 = {template_id = 40, ip = $event_4.uuid}
event_6 = {template_id = 25, ip = $event_5.uuid}
event_7 = {template_id = 41, ip = $event_6.uuid}
event_8 = {template_id = 42, ip = $event_7.uuid}
event_9 = {template_id = 43, ip = $event_8.uuid}

[behavior]
b = (event_1 ~> event_2 ~> event_3 ~> event_4 ~> event_5 ~> event_6 ~> event_7 ~> event_8 ~> event_9)

[model]
NOVADELETE(eventno, eventtype, timestamp, timestampusec, template_id, uuid, ip) =  b
