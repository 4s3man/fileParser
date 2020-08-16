#!/usr/bin/env python3
import pandas as pd
from pandas import DataFrame, Series
import os

from ftfy import fix_text

import sys

# Version 1.0.0 fix csv encoding, columns with city or City in title capitalized
version='1.0.0'

# Output prefix
outputPrefix = 'kubaScriptV' + version.replace('.','') + '_'


def processCell(value)-> str:
    if not isinstance(value, str):
        return value
    value = fix_text(value)
    
    return value

def processCity(city: str)-> str:
    if not isinstance(city, str):
        return city
    
    return city.capitalize()


def showCell(cell):
    if isinstance(cell, str):
        print(cell)

    return cell


def processRow(frame: DataFrame)-> DataFrame:
    for colName in frame.columns:
        frame[colName] = frame[colName].map(processCell)
        
        if 'city' in colName or 'City' in colName:
            frame[colName] = frame[colName].map(processCity)
        
        frame[colName].map(showCell)

    return frame    

def removeFileIfExists(output)-> None:
    if os.path.exists(output):
        os.remove(output)

def parseCsv(inputFile: str)-> None:
    chunksize = 10 ** 4
    output = createOutputFileName(inputFile)
    for chunk in pd.read_csv(inputFile, chunksize=chunksize, encoding='iso-8859-1'):
        removeFileIfExists(output)
        processRow(chunk).to_csv(output, index=False)

def parseXlsFile(inputFile: str)-> None:
    frame = pd.read_excel(inputFile)
    processRow(frame).to_csv(createOutputFileName(inputFile), index=False)    

def isXlsx(inputFile: str)-> bool:
    return 'xlsx' == inputFile.split('.').pop()

def createOutputFileName(inputPath: str)-> str:    
    (path, extension) = os.path.splitext(inputPath)
    basename = os.path.basename(path)

    return outputPrefix + basename + '.csv'

def main(argv):
    if len(sys.argv) != 2:
        raise ValueError('Input file 1st arg output file ' + outputPrefix + '[filename]')
    
    inputPath = sys.argv[1]
    parseXlsFile(inputPath) if isXlsx(inputPath) else parseCsv(inputPath)

if __name__ == "__main__":
   main(sys.argv[1:])