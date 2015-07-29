import sys
import ast
import re
import pprint
pp = pprint.PrettyPrinter()
templates = [
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
        }
        ]


for t in templates: 
    t['regex'] = re.compile(t['body'])

messages = ast.literal_eval(''.join([l for l in sys.stdin]))

for mi, m in enumerate(messages): 
    m['id'] = -1
    for t in templates:
        matched = t['regex'].match(m['message_body'])
        if matched: 
            m['message_body_template_id'] = t['id']
            for vi, v in enumerate(t['variables']): 
                m['message_body' + '_' + v] = matched.group(vi + 1)
            #if t['id'] in [1]: 
            pp.pprint(m) 
            break
         

