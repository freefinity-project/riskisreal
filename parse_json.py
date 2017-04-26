import json
from pprint import pprint
import csv

cleanData = []

def genCleanCSV():
    global cleanData
    rawData = []
    with open("Datasets/raw/API_EN.ATM.CO2E.PC_DS2_en_csv_v2/API_EN.ATM.CO2E.PC_DS2_en_csv_v2.csv", "rb") as csvfile:
        datareader = csv.reader(csvfile)
        for i in range(5):
            next(datareader, None)
        for line in datareader:
            # print newline
            if line[4] != '':
                rawData.append(line)
    for row in rawData:
        newrow = row
        del newrow[2]
        del newrow[2]
        cleanData.append(newrow)
    ofile = open('Datasets/clean/cdo_emissions.csv', "wb")
    writer = csv.writer(ofile)

    for row in cleanData:
        writer.writerow(row)

genCleanCSV()

with open('Datasets/raw/countries.json') as data_file:
    data = json.load(data_file)

print len(data)
#
# for country in data:
#     if country["cca3"]
