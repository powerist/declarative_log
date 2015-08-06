###############################################################
# Script  
#	NOVABOOT
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
#	Outputs event sequences that represent novaboot actions
#
# Output Event Name
#	 OpenStack
#
#Output Attributes     

############################################################### 
[header]
NAMESPACE = USERMODELS
NAME = NOVABOOT
QUALIFIER = {}

[states]
event_1 = {template_id = 0, ip = $1}
event_2 = {template_id = 2, ip = $event_1.ip}
event_3 = {template_id = 7, ip = $event_2.ip}
event_4 = {template_id = 9, ip = $event_3.ip}
event_5 = {template_id = 10, ip = $event_4.ip}
event_6 = {template_id = 11, uuid = $event_5.uuid}
event_7 = {template_id = 12, uuid = $event_6.uuid1}
event_8 = {template_id = 13, ip = $event_7.ip}
event_9 = {template_id = 9, ip = $event_8.ip}
event_10 = {template_id = 7, ip = $event_9.ip}
event_11 = {template_id = 14, uuid_plain = $event_10.uuid_plain}
event_12 = {template_id = 17, uuid = $event_11.uuid}
event_13 = {template_id = 15, uuid = $event_12.uuid}
event_14 = {template_id = 16, uuid = $event_13.uuid}
event_15 = {template_id = 18, uuid = $event_14.uuid}
event_16 = {template_id = 21, uuid = $event_15.uuid}
event_17 = {template_id = 19, uuid = $event_16.uuid}
event_18 = {template_id = 20, uuid = $event_17.uuid}
event_19 = {template_id = 22, uuid = $event_18.uuid}
event_20 = {template_id = 23, uuid = $event_19.uuid}
event_21 = {template_id = 24, uuid = $event_20.uuid}
event_22 = {template_id = 25, uuid = $event_21.uuid1}
event_23 = {template_id = 26, uuid = $event_22.uuid}


[behavior]
b = (event_1 ~> event_2 ~> event_3 ~> event_4 ~> event_5 ~> event_6 ~> event_7 ~> event_8 ~> event_9 ~> event_10 ~> event_11 ~> event_12 ~> event_13 ~> event_14 ~> event_15 ~> event_16 ~> event_17 ~> event_18 ~> event_19 ~> event_20 ~> event_21 ~> event_22 ~> event_23)

[model]
NOVABOOT(eventno, eventtype, timestamp, timestampusec, template_id, uuid, ip, uuid_plain) =  b
