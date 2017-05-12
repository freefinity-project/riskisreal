import json
from pprint import pprint
import csv
import unicodedata
import fileinput



urbanpop = {}
with open("Datasets/raw/urbanpop.csv", "rb") as csvfile:
    datareader = csv.reader(csvfile)
    for line in datareader:
        if(line[4] != ""):
            if(line[3] == "SP.URB.TOTL.IN.ZS"):
                urbanpop[line[0]] = line[4:60]

print urbanpop["Aruba"]