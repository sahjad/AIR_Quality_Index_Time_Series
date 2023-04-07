from datetime import datetime
import base64
import requests
import dataset
import json
import hashlib 
import time

#Making Database connection
db = dataset.connect('sqlite:///../data/db/data.sqlite3')
site_table = db["sites"]
table = db["request_status_data"]
status_code = 1 # 0 for low priority
row_exists = table.find_one(status_code=status_code)
print(row_exists)

while row_exists:     
    print ("#####################################################"+ str(datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')))
    db.begin()
    query_name =row_exists['query_name'] 
    print ("query_name = "+str(query_name))
    encoded_data = row_exists['encoded_data']
    
    print ("encoded_data = "+str(encoded_data))

    headers = {'Origin': 'https://app.cpcbccr.com'}
    headers['Accept-Encoding'] ="gzip, deflate, br"
    headers['Accept-Language'] ="en-US,en;q=0.9"
    headers['User-Agent'] ="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"
    headers['Content-Type'] ="text/plain"
    headers['Accept'] ="application/json, text/plain, */*"
    headers['Referer'] ="https://app.cpcbccr.com/ccr/"
    headers['Connection'] ="keep-alive"
    headers['authority'] ="app.cpcbccr.com"

    r = requests.post("https://app.cpcbccr.com/caaqms/fetch_table_data", headers=headers, data=encoded_data, verify=False)
    print (r.headers)
    if r.status_code == 200:
        print ("Awesome response code 200")
        json_data = json.dumps(r.json())
        print ("I am the json data ===>" + json_data)
        encode_data_bytes = json_data.encode("utf-8")
        encoded_json_data = base64.b64encode(encode_data_bytes)
        json_data_hash = hashlib.md5(encoded_json_data)
        row_exists['json_data'] = json_data
        row_exists['json_data_hash'] = json_data_hash.hexdigest()
        row_exists['status_code'] = r.status_code
    else:
        row_exists['json_data'] = ""
        row_exists['status_code'] = r.status_code

    print ("UPDATING")
    table.update(row_exists,['id'])
    db.commit()

    time.sleep(5)
    row_exists = table.find_one(status_code=status_code)
    if row_exists:
        pass
    else:
        break

    #this is for testing    
    #break

print ("_______________________________________________________________")

#end while
