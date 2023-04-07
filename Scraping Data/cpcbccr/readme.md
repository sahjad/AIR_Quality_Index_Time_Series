# Details
[Scraping National Air Quality Data

# Code
All the code exists in the code folder. There are three python scripts, they all use data.sqlite3 databse inside data/db/data.sqlite3.  Check sites table to see all the sites are setup before you start

1. setup_pull.py # you need to setup the dates for which you need to get data. After that run this script. This sets up all the requests that needs to be called to pull the data.It will make an entry to request_status_data.

2. pull.py # call this to actually pull the data setup in the previous script. Data received is JSON and stored in request_status_data.The status code should be 200 which indicates success while 404 in case of failure.

3. parse.py # this actually parses the data got in step 2 and fills the data table.Also, this will mark parsed =1 in in request_status_data.

# Data
1. The main db is in data/db/data.sqlite3
2. some reports are in reports tab along with the sqls I generally use
3. test - some test data, ignore it

#Sites Which can be helpful
1. Sites code can be pulled from https://app.cpcbccr.com/AQI_India and doing an inspect element.Or it can be pulled from https://app.cpcbccr.com/aqi_dashboard/aqi_station_all_india API call by checking the response parameters.

2. https://app.cpcbccr.com/caaqms/fetch_table_data is the API to pull the tabular data and in this we need to send all the request parameters. 

Pollutants Unique ID :
{
  "criteria": "24 Hours",
  "reportFormat": "Tabular",
  "fromDate": "22-09-2020 T00:00:00Z",
  "toDate": "23-09-2020 T14:50:59Z",
  "state": "Delhi",
  "city": "Delhi",
  "station": "site_5024",
  "parameter": [
    "parameter_215",
    "parameter_193",
    "parameter_204",
    "parameter_238",
    "parameter_237",
    "parameter_235",
    "parameter_234",
    "parameter_236",
    "parameter_226",
    "parameter_225",
    "parameter_194",
    "parameter_311",
    "parameter_312",
    "parameter_203",
    "parameter_222",
    "parameter_202",
    "parameter_232",
    "parameter_223",
    "parameter_240",
    "parameter_216"
  ],
  "parameterNames": [
    "PM10",
    "PM2.5",
    "AT",
    "BP",
    "SR",
    "RH",
    "WD",
    "RF",
    "NO",
    "NOx",
    "NO2",
    "NH3",
    "SO2",
    "CO",
    "Ozone",
    "Benzene",
    "Toluene",
    "Xylene",
    "MP-Xylene",
    "Eth-Benzene"
  ]
}

https://www.base64decode.org/ In order to decode the parameters and form prompt_all in setup_pull.py


