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


temptop30 = {}

with open("Datasets/temp_top30.csv", "rb") as csvfile:
    datareader = csv.reader(csvfile)
    for line in datareader:
        tmps = line[2:]
        actual_row = []
        i = 0
        for i in range(len(tmps)):
            if (i <= 48):
                try:
                    actual_row.append([i+1960, float(tmps[i])])
                except ValueError:
                    pass
        temptop30[line[0]] = actual_row


print temptop30

maxn = 0
for i in temptop30:
    for j in temptop30[i]:
        if(j[1] > maxn):
            maxn = j[1]
print maxn

minn = 1000000000
for i in temptop30:
    for j in temptop30[i]:
        if(j[1] < minn):
            minn = j[1]
print minn


print cdo_emissions

with open("timegraph/tempdata_time.json", 'w') as f:
    f.write("[")
    f.write("\n")
    for country in temptop30:
        try:
            testr = cdo_emissions[country]
            testr = regions[country]
            f.write("\t{\n")
            f.write("\t\t\"name\": ")
            f.write("\"" + country + "\"")
            f.write(",")
            f.write("\n")

            f.write("\t\t\"region\": ")
            try:
                f.write("\"" + regions[country] + "\"")
            except KeyError:
                f.write("\"Asia\"")
            f.write(",")
            f.write("\n")

            f.write("\t\t\"income\": ")
            f.write("[")
            f.write("\n")
            for i in cdo_emissions[country]:
                f.write("\t\t\t[")
                f.write("\n")
                f.write("\t\t\t\t" + str(i[0]))
                f.write(",\n")
                f.write("\t\t\t\t" + str(i[1]))
                f.write("\n")
                f.write("\t\t\t]")
                if (cdo_emissions[country].index(i) != len(cdo_emissions[country]) - 1):
                    f.write(",")
                f.write("\n")
            f.write("\t\t],\n")

            f.write("\t\t\"population\": ")
            f.write("[")
            f.write("\n")
            for i in populations[country]:
                f.write("\t\t\t[")
                f.write("\n")
                f.write("\t\t\t\t" + str(i[0]))
                f.write(",\n")
                f.write("\t\t\t\t" + str(i[1]))
                f.write("\n")
                f.write("\t\t\t]")
                if (populations[country].index(i) != len(populations[country]) - 1):
                    f.write(",")
                f.write("\n")
            f.write("\t\t],\n")

            f.write("\t\t\"lifeExpectancy\": ")
            f.write("[")
            f.write("\n")
            for i in temptop30[country]:
                f.write("\t\t\t[")
                f.write("\n")
                f.write("\t\t\t\t" + str(i[0]))
                f.write(",\n")
                f.write("\t\t\t\t" + str(i[1]))
                f.write("\n")
                f.write("\t\t\t]")
                if (temptop30[country].index(i) != len(temptop30[country]) - 1):
                    f.write(",")
                f.write("\n")
            f.write("\t\t]\n")

            f.write("\t},\n")

        except KeyError:
            pass

    f.write("]")