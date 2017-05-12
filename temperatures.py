import csv, json
import pandas as pd
import codecs

temp_series = {}

contents = codecs.open('Datasets/raw/tempfile.csv', encoding='utf-8').read()
contents = contents.replace('    ', ',')
with open('Datasets/raw/tempfile.csv', 'w') as csvfile:
    csvfile.write(contents)

country_name = ""
val_list = []
with open('Datasets/raw/tempfile.csv', 'rb') as csvfile:
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
    temp_series[country_name] = val_list

for i in temp_series:
    print i, temp_series[i]
