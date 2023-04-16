import pandas as pd

data = pd.read_excel('data.xlsx')

dictionaryOfData = {}

for num in data['teamNumber']:
    if num not in dictionaryOfData:
        dictionaryOfData[num] = [data[data['teamNumber'] == num]]
    else:
        dictionaryOfData[num].append(data[data['teamNumber'] == num])

for key in dictionaryOfData:
