# Import packages
import requests,sys
import csv

teleconnection = "https://www.cpc.ncep.noaa.gov/products/precip/CWlink/pna/norm.daily.ao.nao.pna.aao.gdas.120days.csv"

# Grab the CPC teleconnection archive CSV file
with requests.Session() as s:
    download = s.get(teleconnection)
    teleconnection = download.content.decode('utf-8')
    cr = csv.reader(teleconnection.splitlines(), delimiter=',', skipinitialspace=True)
    teleconnection = list(cr)
    
rows = []

#with open(teleconnection, newline='') as csvFile:
#    csvRead = csv.reader(csvFile, delimiter = ',', skipinitialspace=True)
for row in teleconnection:
    rows.append(row)

# Extract the last two weeks of values, then write them into the good ol'
# NavCSV format
with open('cpcTeleconnection.csv', 'w', newline='') as csvFileTwo:
    csvWrite = csv.writer(csvFileTwo, delimiter=',')
    for i in range(0, 16):
        if i == 0:
            navCSVstuff = ["LOCATIONID", "LOCATIONNAME", "LATITUDE", "LONGITUDE"]
        else:
            rowName = str(i - 1) + "_DaysAgo"
            navCSVstuff = [rowName,rowName,"",""]
        rowQueuedUp = navCSVstuff + rows[0 - i]
        print(rowQueuedUp)
        csvWrite.writerow(rowQueuedUp)
