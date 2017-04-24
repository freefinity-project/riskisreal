import numpy as np
import csv
import matplotlib.pyplot as plt
import numpy
import matplotlib.pyplot as plt
import pandas
import math
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error

cleanData = []
numpy.random.seed(7)

def cleanCSV():
    global cleanData
    with open("Datasets/API_EN.ATM.CO2E.PC_DS2_en_csv_v2/API_EN.ATM.CO2E.PC_DS2_en_csv_v2.csv", "rb") as csvfile:
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
                cleanData.append(newline)

    for i in cleanData:
        print i


# plt.plot(cleanData)
# plt.show()

for country_row in cleanData:
    country_name = country_row[0]
    ts_vals = numpy.array(country_row[1:len(country_row)])
    scaler = MinMaxScaler(feature_range=(0, 1))
    dataset = scaler.fit_transform(dataset)