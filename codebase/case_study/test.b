###############################################################
# Script  
#	OPENSTACKTEST
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
#	Outputs two events whose "test" fields match
#
# Output Event Name
#	 OpenStack
#
#Output Attributes     

############################################################### 
[header]
NAMESPACE = USERMODELS
NAME = OPENSTACKTEST
QUALIFIER = {}

[states]
test_s = {test = $1}
test_d = {test = $test_s.test}

[behavior]
b = test_s ~> test_d

[model]
OPENSTACKTEST(eventno, eventtype, timestamp, timestampusec, test) =  b
