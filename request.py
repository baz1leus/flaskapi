import requests

HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKCYAN = '\033[96m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

def process_responce(resp):
    if resp.ok:
        print(OKGREEN, resp.json(), ENDC)
    else:
        print(WARNING, resp.text, ENDC)
    print('---')


process_responce(requests.get('http://127.0.0.1:5000'))
process_responce(requests.get('http://127.0.0.1:5000/store'))
process_responce(requests.get('http://127.0.0.1:5000/store/My Store'))
process_responce(requests.post('http://127.0.0.1:5000/store', json={'name': 'MSTORE'}))
process_responce(requests.post('http://127.0.0.1:5000/store/My Store', json={'name': 'MITEM', 'price': 1412}))
