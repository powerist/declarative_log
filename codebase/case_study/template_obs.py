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
        # {
        #     'id': 13, 
        #     #'body': "[req-OS_UUID OS_UUID_PLAIN OS_UUID_PLAIN] OS_IP "GET /vOS_NUMBER/OS_UUID_PLAIN/servers/OS_UUID HTTP/OS_NUMBER" status: OS_NUMBER len: OS_NUMBER time: OS_NUMBER"
        #     'body': "\[req-([\w\-]+) (\w+) (\w+)\] (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) \"GET /v(\d+)/(\w+)/servers/([\w\-]+) HTTP/\" status: (\d+) len: (\d+) time: (\d+.\d+)",
        #     'variables': ['OS_UUID', 'OS_UUID_PLAIN', 'OS_UUID_PLAIN', 'OS_IP', 'OS_NUMBER', 'OS_UUID_PLAIN', 'OS_UUID', 'OS_NUMBER', 'OS_NUMBER', 'OS_NUMBER', 'OS_NUMBER']
        # }
]
 
