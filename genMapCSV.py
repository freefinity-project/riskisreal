import csv
import numpy as np


country_rates = {}
country_rate_vector = {}
with open("Datasets/clean/cdo_emissions.csv", "rb") as csvfile:
    datareader = csv.reader(csvfile)
    for line in datareader:
        # print line
        country_name = line[0]
        country_code = line[1]
        country_vector = line[2:]
        country_rate = []
        prev_val = None
        curr_val = None
        for cdoval in country_vector:
            try:
                curr_val = float(cdoval)
                if(prev_val != None):
                    country_rate.append(curr_val - prev_val)
                prev_val = curr_val
            except ValueError:
                pass
        country_rate_vector[country_code] = np.array(country_rate)


for country in country_rate_vector:
    country_rates[country] = np.mean(country_rate_vector[country])


print country_rates

max = 0
argmax = 0
meanv = 0
for i in country_rates:
    meanv += country_rates[i]
    if(country_rates[i] > max):
        max = country_rates[i]
        argmax = i
print meanv/len(country_rates)
print argmax, max

# with open('Datasets/clean/cdo_map.csv', 'w') as f:  # Just use 'w' mode in 3.x
#     f.write("country,rate_value")
#     f.write("\n")
#     for country in country_rates:
#         f.write(str(country) + ",")
#         f.write(str(country_rates[country]))
#         f.write("\n")