import numpy as np
import csv

with open("Datasets/Set1Complete.csv", "rb") as csvfile:
    datareader = csv.reader(csvfile)
    next(datareader, None)