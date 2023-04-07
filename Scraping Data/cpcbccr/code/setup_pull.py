from datetime import datetime
from datetime import timedelta
import base64
import dataset

#Making Database connection
db = dataset.connect('sqlite:///../data/db/data.sqlite3')
#TODO : edit data/db/data.sqlite3 and add the sites you want to scrape into sites table.
site_table = db["sites"]
#check if sites is connecting and able to fetch a station
print(site_table.find_one(site_name='Anand Vihar, Delhi - DPCC'))
run_name = "run2_"  #leave this as it is


for site_row in site_table:
    state = site_row['state']
    city = site_row['city']
    site = site_row['site']
    site_name = site_row['site_name']
    print("state "+state+"city "+city+"site "+ site)
    label = state.lower().replace(" ","") +"_"+city.lower().replace(" ","-")+"_"+site+"_"
    print("label " + label)
    table = db["request_status_data"]
    fromDate = "30-12-2020"  #TODO 2: starting date
    endDate = "31-12-2020"   #TODO 3: ending date, will be next day after that day
    how_many_days = 161  

    toDate = ""
    objFromDate = datetime.strptime(fromDate, "%d-%m-%Y" )
    time_part = " T00:00:00Z"
    time_part_end = " T23:59:00Z"
    status_code = 1

    while (objFromDate < datetime.strptime(endDate, "%d-%m-%Y" )):
        print ("####################################################")

        objToDate = objFromDate +timedelta(days=how_many_days)

        fromDate=objFromDate.strftime("%d-%m-%Y")+time_part
        toDate=objToDate.strftime("%d-%m-%Y")+time_part

        print (fromDate)
        print (toDate)


        query_name = run_name + label + objFromDate.strftime("%Y%m%d")

        print ("I am the query" + query_name)

        prompt_all='{"draw":1,"columns":[{"data":0,"name":"","searchable":true,"orderable":false,"search":{"value":"","regex":false}}],"order":[],"start":0,"length":2000,"search":{"value":"","regex":false},"filtersToApply":{"parameter_list":[{"id":0,"itemName":"PM2.5","itemValue":"parameter_193"},{"id":1,"itemName":"PM10","itemValue":"parameter_215"},{"id":4,"itemName":"NOx","itemValue":"parameter_225"},{"id":6,"itemName":"SO2","itemValue":"parameter_312"},{"id":7,"itemName":"CO","itemValue":"parameter_203"}],"criteria":"24 Hours","reportFormat":"Tabular","fromDate":"'+fromDate+'","toDate":"'+toDate+'","state":"'+state+'","city":"'+city+'","station":"'+site+'","parameter":["parameter_193","parameter_215","parameter_225","parameter_312","parameter_203"],"parameterNames":["PM2.5","PM10","NOx","SO2","CO"]},"pagination":1}'
        #prompt_both='{"draw":2,"columns":[{"data":0,"name":"","searchable":true,"orderable":false,"search":{"value":"","regex":false}}],"order":[],"start":10,"length":10,"search":{"value":"","regex":false},"filtersToApply":{"parameter_list":[{"id":0,"itemName":"PM2.5","itemValue":"parameter_193"},"criteria":"4 Hours","reportFormat":"Tabular","fromDate":"'+fromDate+'","toDate":"'+toDate+'","state":"'+state+'","city":"'+city+'","station":"'+site+'","parameter":["parameter_193"],"parameterNames":["PM2.5"]},"pagination":1}'


        data_to_encode = prompt_all
        data_bytes = data_to_encode.encode("utf-8")
        encoded_data = base64.b64encode(data_bytes)
        print (encoded_data)

        row_exists = table.find_one(query_name=query_name)
        if row_exists:
            print ("EXISTS SO GO TO NEXT")
        else:
            row = {}
            row['query_name'] = query_name 
            row['fromDate'] = fromDate
            row['toDate'] = toDate
            row['state'] = state
            row['city'] = city
            row['site'] = site
            row['site_name'] = site_name
            row['data_to_encode'] = data_to_encode
            row['encoded_data'] = encoded_data
            row['status_code'] = status_code        
            row['parsed'] = 0
            table.insert(row)

        #forward in date for next
        objFromDate = objToDate    
        print ("_______________________________________________________________")
        #end while