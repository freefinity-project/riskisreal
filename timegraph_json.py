import json,csv

populations = {}
cdo_emissions = {}
regions = {}
with open('timegraph/sampledata.json') as data_file:
    data = json.load(data_file)

for i in range(len(data)):
    actual_row = []
    for prow in data[i]["population"]:
        if(prow[0] >= 1960):
            actual_row.append(prow)

    populations[data[i]["name"]] = actual_row
    regions[data[i]["name"]] = data[i]["region"]




with open("Datasets/clean/cdo_emissions.csv", "rb") as csvfile:
    datareader = csv.reader(csvfile)
    for line in datareader:
        cdv = line[2:]
        actual_row = []
        i = 0
        for i in range(len(cdv)):
            if (i <= 48):
                try:
                    actual_row.append([i+1960, float(cdv[i])])
                except ValueError:
                    pass
        cdo_emissions[line[0]] = actual_row

# print cdo_emissions["India"]
# print populations["India"]






urbanpop = {}
with open("Datasets/raw/urbanpop.csv", "rb") as csvfile:
    datareader = csv.reader(csvfile)
    for line in datareader:
        if(line[4] != ""):
            if(line[3] == "SP.URB.TOTL.IN.ZS"):
                actual_row = []
                for i in line[4:60]:
                    try:
                        actual_row.append(float(i))
                    except ValueError:
                        actual_row.append(i)
                urbanpop[line[0]] = actual_row

# print urbanpop["Aruba"]

urbanpop_dict = {}
for country in urbanpop:
    actual_row = []
    for i in range(len(urbanpop[country])):
        if(i<=48):
            try:
                actual_row.append([i + 1960, float(urbanpop[country][i])])
            except ValueError:
                actual_row.append([i + 1960, urbanpop[country][i]])
    urbanpop_dict[country] = actual_row

# print urbanpop_dict

maxn = 0
argmax = 0
meanv = 0
for i in cdo_emissions:
    for j in cdo_emissions[i]:
        if(j[1] > maxn):
            maxn = j[1]
print maxn
#
#
# with open("timegraph/mydata.json", 'w') as f:
#     f.write("[")
#     f.write("\n")
#     for country in cdo_emissions:
#         try:
#             testr = regions[country]
#             f.write("\t{\n")
#             f.write("\t\t\"name\": ")
#             f.write("\"" + country + "\"")
#             f.write(",")
#             f.write("\n")
#
#             f.write("\t\t\"region\": ")
#             try:
#                 f.write("\"" + regions[country] + "\"")
#             except KeyError:
#                 f.write("\"Asia\"")
#             f.write(",")
#             f.write("\n")
#
#             f.write("\t\t\"income\": ")
#             f.write("[")
#             f.write("\n")
#             for i in cdo_emissions[country]:
#                 f.write("\t\t\t[")
#                 f.write("\n")
#                 f.write("\t\t\t\t" + str(i[0]))
#                 f.write(",\n")
#                 f.write("\t\t\t\t" + str(i[1]))
#                 f.write("\n")
#                 f.write("\t\t\t]")
#                 if (cdo_emissions[country].index(i) != len(cdo_emissions[country]) - 1):
#                     f.write(",")
#                 f.write("\n")
#             f.write("\t\t],\n")
#
#             f.write("\t\t\"population\": ")
#             f.write("[")
#             f.write("\n")
#             for i in populations[country]:
#                 f.write("\t\t\t[")
#                 f.write("\n")
#                 f.write("\t\t\t\t" + str(i[0]))
#                 f.write(",\n")
#                 f.write("\t\t\t\t" + str(i[1]))
#                 f.write("\n")
#                 f.write("\t\t\t]")
#                 if (populations[country].index(i) != len(populations[country]) - 1):
#                     f.write(",")
#                 f.write("\n")
#             f.write("\t\t],\n")
#
#             f.write("\t\t\"lifeExpectancy\": ")
#             f.write("[")
#             f.write("\n")
#             for i in urbanpop_dict[country]:
#                 f.write("\t\t\t[")
#                 f.write("\n")
#                 f.write("\t\t\t\t" + str(i[0]))
#                 f.write(",\n")
#                 f.write("\t\t\t\t" + str(i[1]))
#                 f.write("\n")
#                 f.write("\t\t\t]")
#                 if (urbanpop_dict[country].index(i) != len(urbanpop_dict[country]) - 1):
#                     f.write(",")
#                 f.write("\n")
#             f.write("\t\t]\n")
#
#             f.write("\t},\n")
#
#         except KeyError:
#             pass
#
#     f.write("]")