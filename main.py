#!/usr/bin/env python3
import pandas as pd
from pandas import DataFrame, Series
import os
import unicodedata

from ftfy import fix_text

import sys

# Version 1.0.1 fix csv encoding, columns with city or City in title capitalized
# used as terminal command
# output files in directory with input file
version='1.0.1'

# Output prefix
outputPrefix = 'kubaScriptV' + version.replace('.','') + '_'
ENCODING = 'Windows-1252'
INPUT_ENCODING = ENCODING

def fixString(value)-> str:
    if not isinstance(value, str):
        return value
    value = fix_text(value)
    
    return value

def capitalizeString(city: str)-> str:
    if not isinstance(city, str):
        return city
    
    return city.capitalize()


def printString(cell):
    if isinstance(cell, str):
        print(cell)

    return cell


def processRow(frame: DataFrame)-> DataFrame:
    for colName in frame.columns:
        frame[colName] = frame[colName].map(fixString)
        
        if 'city' in colName or 'City' in colName:
            frame[colName] = frame[colName].map(capitalizeString)
        
        frame[colName].map(printString)
        frame[colName].map(lambda x: x.replace('(Ingen)','') if isinstance(x, str) else x)

    return frame    

def removeFileIfExists(output)-> None:
    if os.path.exists(output):
        os.remove(output)

def parseCsv(inputFile: str)-> None:
    chunksize = 10 ** 4
    output = createOutputFileName(inputFile)
    for chunk in pd.read_csv(inputFile, chunksize=chunksize, encoding=INPUT_ENCODING):
        removeFileIfExists(output)
        saveFile(chunk, inputFile)

def parseXlsFile(inputFile: str)-> None:
    frame = pd.read_excel(inputFile)
    frame = processRow(frame)
    saveFile(frame, inputFile)

def isXlsx(inputFile: str)-> bool:
    return 'xlsx' == inputFile.split('.').pop()

def createOutputFileName(inputPath: str)-> str:        
    (path, extension) = os.path.splitext(inputPath)
    basename = os.path.basename(path)
    
    return path.replace(basename, outputPrefix + basename + '.csv')

def saveFile(frame: DataFrame, inputFile: str):
    frame.to_csv(createOutputFileName(inputFile), encoding=ENCODING, index=False, errors='replace')

def main(argv):
    if len(sys.argv) < 2:
        raise ValueError('Input file 1st arg output file ' + outputPrefix + '[filename], 2nd arg encoding default' + ENCODING)
    
    if 3 <= len(sys.argv):
        ENCODING = sys.argv[2]

    inputPath = sys.argv[1]
    parseXlsFile(inputPath) if isXlsx(inputPath) else parseCsv(inputPath)

if __name__ == "__main__":
   main(sys.argv[1:])