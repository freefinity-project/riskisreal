import json
from pprint import pprint
import csv
import unicodedata

cleanData = []
valDict = {}

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
        valDict[newrow[1].encode('ascii','ignore')] = newrow[2:]
        cleanData.append(newrow)
    ofile = open('Datasets/clean/cdo_emissions.csv', "wb")
    writer = csv.writer(ofile)

    for row in cleanData:
        writer.writerow(row)


def genJSON():
    global cleanData
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
            print "\n"
        except KeyError:
            print "Not found", country_code


genCleanCSV()
genJSON()