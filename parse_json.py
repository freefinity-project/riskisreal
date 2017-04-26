import json
from pprint import pprint
import csv
import unicodedata

cleanData = []
valDict = {}
jsonData = {}
# We need data in this format:
# var data = [
#     [
#     '1995', [ latitude, longitude, magnitude, latitude, longitude, magnitude, ... ]
#     ],
#     [
#     '1996', [ latitude, longitude, magnitude, latitude, longitude, magnitude, ... ]
#     ]
# ];

def genCleanCSV():
    global cleanData, valDict
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
        valDict[newrow[1].encode('ascii','ignore')] = newrow[2:56]
        cleanData.append(newrow[0:56])
    ofile = open('Datasets/clean/cdo_emissions.csv', "wb")
    writer = csv.writer(ofile)

    for row in cleanData:
        writer.writerow(row)


def genJSON():
    global cleanData, jsonData
    with open('Datasets/raw/countries.json') as data_file:
        data = json.load(data_file)
    print "Loaded", len(data), "countries."

    for country in data:
        country_code = country["cca3"].encode('ascii','ignore')
        country_latlng = country["latlng"]
        try:
            country_val = valDict[country_code]
            print "For", country_code, "at", country_latlng, ":"
            print "\t", country_val
            for i in range(len(country_val)):
                year_val = country_val[i]
                toAppend = [country_latlng[0], country_latlng[1], year_val]
                jsonData[str(i)] = jsonData[str(i)].append(toAppend)
        except KeyError:
            print "Not found", country_code
    print jsonData
    with open('Datasets/clean/cdo_emissions.json', 'w') as outfile:
        json.dump(jsonData, outfile)


genCleanCSV()
genJSON()