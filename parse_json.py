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
            cnt = 0
            for year_val in country_val:
                try:
                    toAppend = [country_latlng[0], country_latlng[1], float(year_val)/10]
                except ValueError:
                    toAppend = [country_latlng[0], country_latlng[1], float("0.")]
                jsondictkey = str(cnt+1960)
                # print "At key ", str(jsondictkey), "toAppend : ", toAppend
                try:
                    current_json_list_val = jsonData[jsondictkey]
                    for val in toAppend:
                        current_json_list_val.append(val)
                    jsonData[jsondictkey] = current_json_list_val
                except KeyError:
                    jsonData[jsondictkey] = toAppend
                cnt+=1
        except KeyError:
            print "Not found", country_code
    print jsonData
    with open('Datasets/clean/cdo_emissions_2.json', 'w') as outfile:
        json.dump(jsonData, outfile)

# /riskisreal/webgl-globe/globe/population909500.json
# /riskisreal/Datasets/clean/cdo_emissions.json
# /riskisreal/Datasets/clean/cdo_emissions.json

# Replace <, "> with <],[">
# Replace <{> in begining with <[[> and <}> in end with <]]>
# Replace <: > with <,>
genCleanCSV()
genJSON()