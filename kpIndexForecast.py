# Import packages
import requests,sys
import csv
import re

forecast = "https://services.swpc.noaa.gov/text/3-day-forecast.txt"

# Grab the CPC teleconnection archive CSV file
with requests.Session() as s:
    download = s.get(forecast)
    forecast = download.content.decode('utf-8').splitlines()

rows = []

morningForecast = False
eveningForecast = False

for i in range(0, len(forecast)):
    if forecast[i][21:23] == "12":
        morningForecast = True
    if forecast[i][21:23] == "00":
        eveningForecast = True

for i in range(0, len(forecast)):
    if forecast[i][0:7] == "00-03UT":
        # Remove consecutive whitespace without deleting actual spaces
        daylist = ((re.sub('\s{2,}', ',', forecast[i - 1])).split(","))[1:]
        
        for j in range(i, i + 8):
            # Remove consecutive whitespace without deleting actual spaces
            addToData = ((re.sub('\s{2,}', ',', forecast[j])).split(","))[:-1]
            rows.append(addToData)
       
print(rows)

# For 12z forecast
# tonight           = 21z day 1 --> 15z day 2
# tomorrow night    = 21z day 2 --> 15z day 3
# day 3             = 18z day 3 --> end of forecast

# For 00z forecast
# tonight           = 00z day 1 --> 15z day 1
# tomorrow night    = 21z day 1 --> 15z day 2
# day 3             = 21z day 2 --> 15z day 3

day1 = []
day2 = []
day3 = []

if morningForecast == True:
    day1.append(rows[7][1]) # 21z day 1
    day1.append(rows[0][2]) # 00z day 2
    day1.append(rows[1][2]) # 03z day 2
    day1.append(rows[2][2]) # 06z day 2
    day1.append(rows[3][2]) # 09z day 2
    day1.append(rows[4][2]) # 12z day 2
    
    day2.append(rows[7][2]) # 21z day 2
    day2.append(rows[0][3]) # 00z day 3
    day2.append(rows[1][3]) # 03z day 3
    day2.append(rows[2][3]) # 06z day 3
    day2.append(rows[3][3]) # 09z day 3
    day2.append(rows[4][3]) # 12z day 3
    
    day3.append(rows[6][3]) # 09z day 3
    day3.append(rows[7][3]) # 12z day 3
    
    day1_max = int(round(float(max(day1)), 0))
    day2_max = int(round(float(max(day2)), 0))
    day3_max = int(round(float(max(day3)), 0))

if eveningForecast == True:
    day1.append(rows[0][1]) # 00z day 1
    day1.append(rows[1][1]) # 03z day 1
    day1.append(rows[2][1]) # 06z day 1
    day1.append(rows[3][1]) # 09z day 1
    day1.append(rows[4][1]) # 12z day 1
    
    day2.append(rows[7][1]) # 21z day 1
    day2.append(rows[0][2]) # 00z day 2
    day2.append(rows[1][2]) # 03z day 2
    day2.append(rows[2][2]) # 06z day 2
    day2.append(rows[3][2]) # 09z day 2
    day2.append(rows[4][2]) # 12z day 2
   
    day2.append(rows[7][2]) # 21z day 2
    day2.append(rows[0][3]) # 00z day 3
    day2.append(rows[1][3]) # 03z day 3
    day2.append(rows[2][3]) # 06z day 3
    day2.append(rows[3][3]) # 09z day 3
    day2.append(rows[4][3]) # 12z day 3
    
    day1_max = int(round(float(max(day1)), 0))
    day2_max = int(round(float(max(day2)), 0))
    day3_max = int(round(float(max(day3)), 0))

print(str(day1_max) + ", " + str(day2_max) + ", " + str(day3_max))

with open('kpIndex.csv', 'w', newline='') as csvFileTwo:
    csvWrite = csv.writer(csvFileTwo, delimiter=',')
    for i in range(0, len(rows) + 1):
        if i == 0:
            navCSVstuff = ["LOCATIONID","LOCATIONNAME","LATITUDE","LONGITUDE","TIME","DAY1","DAY2","DAY3"]
            navCSVstuff = navCSVstuff
            csvWrite.writerow(navCSVstuff)
        else:
            rowName = "ForecastTime" + str(i)
            navCSVstuff = [rowName,rowName,"",""]
            rowQueuedUp = navCSVstuff + rows[i - 1]
            print(rowQueuedUp)
            csvWrite.writerow(rowQueuedUp)

    navCSVstuff = ["Date","Date","","",""]
    csvWrite.writerow(navCSVstuff + daylist)
    
    navCSVstuff = ["MaxValue","MaxValue","","",""]
    csvWrite.writerow(navCSVstuff + [str(day1_max), str(day2_max), str(day3_max)])
    
