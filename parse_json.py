import json
from pprint import pprint
import csv


def genCleanCSV():
    global cleanData
    with open("Datasets/raw/API_EN.ATM.CO2E.PC_DS2_en_csv_v2/API_EN.ATM.CO2E.PC_DS2_en_csv_v2.csv", "rb") as csvfile:
        datareader = csv.reader(csvfile)
        for i in range(5):
            next(datareader, None)
        for line in datareader:
            newline = line
            del newline[1]
            del newline[1]
            del newline[1]
            # print newline
            if newline[1] != '':
                cleanData.append(newline[0:55])
    ofile = open('Datasets/.csv', "wb")
    writer = csv.writer(ofile, delimiter='', quotechar='"', quoting=csv.QUOTE_ALL)

    for row in reader:
        writer.writerow(row)


with open('Datasets/countries.json') as data_file:
    data = json.load(data_file)

print len(data)

for country in data:
    if country["cca3"]
