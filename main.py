#!/usr/bin/env python3
import pandas as pd
from pandas import DataFrame, Series
import os

from ftfy import fix_text

output = './output.csv'
inputFile = './postBaldronContacts-withMamut.csv'#'./sample.csv'

def processCell(value)-> str:
    if not isinstance(value, str):
        return value
    value = fix_text(value)
    
    print(value)

    return value

def processCity(city: str)-> str:
    if not isinstance(city, str):
        return city
    
    return city.capitalize()

def processRow(frame: DataFrame)-> DataFrame:
    for colName in frame.columns:
        frame[colName] = frame[colName].map(processCell)
        
        if 'city' in colName or 'City' in colName:
            frame[colName] = frame[colName].map(processCity)
        

        
    return frame    

def removeFileIfExists(output)-> None:
    if os.path.exists(output):
        os.remove(output)

todoRemoveStop = 0
chunksize = 10 ** 100
for chunk in pd.read_csv(inputFile, chunksize=chunksize, encoding='iso-8859-1'):
    removeFileIfExists(output)
    processRow(chunk).to_csv('./output.csv', index=False)

    # todoRemoveStop+=1
    # if todoRemoveStop > 4:
    #     break

# print(''.join(list(notValidatedYet)))