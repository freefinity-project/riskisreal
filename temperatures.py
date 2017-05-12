import csv, json
import pandas as pd
import codecs
import os


def getTimeSeries(filename):
    print filename
    contents = codecs.open(filename, encoding='utf-8').read()
    contents = contents.replace('   ', ',')
    with open(filename, 'w') as csvfile:
        csvfile.write(contents)

    country_name = ""
    val_list = []
    with open(filename, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        cnt = 0
        for row in spamreader:
            cnt+=1
            if(row[0].split(" = ")[0] == "Country"):
                country_name = row[0].split(" = ")[1]
            if(cnt >=64):
                try:
                    val_list.append(float(row[17]))
                except IndexError:
                    val_list.append(float(row[16]))
    return country_name, val_list


temp_series = {}
for filename in os.listdir('Datasets/temperatures'):
    if filename.endswith(".csv"):
        country_name, val_list = getTimeSeries('Datasets/temperatures/' + filename)
        temp_series[country_name] = val_list
    else:
        continue




with open("Datasets/temp_top30.csv", "w") as f:
    for i in temp_series:
        f.write(i)
        f.write(",")
        f.write(str(temp_series[i])[1:-1].replace(" ",""))
        f.write("\n")