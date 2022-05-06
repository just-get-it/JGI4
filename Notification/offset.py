




import requests,time,json


URL="http://127.0.0.1:8000/api/getOffset"

Offset=None

while True:
    r=requests.get(url=URL)
    Offset=json.loads(r.content)['offset']
    print("skjs",Offset)
    time.sleep(5000)