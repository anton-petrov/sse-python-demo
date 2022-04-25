import json
from rich import print
import sseclient


def get_response(url, headers):
    import urllib3
    http = urllib3.PoolManager()
    return http.request('GET', url, preload_content=False, headers=headers)


url = 'http://localhost:8000/stream-data'
headers = {'Accept': 'text/event-stream'}
response = get_response(url, headers) 
client = sseclient.SSEClient(response)

for event in client.events():
    try:
        print(json.loads(event.data))
    except:
        pass
        # print(type(event.data), event.data)