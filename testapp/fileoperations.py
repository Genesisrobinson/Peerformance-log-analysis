## Calculating logical conditions in data frame elements
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from django.http import HttpResponse
#Folder='/Users/genesisrobinson/Documents/Excel'
#R1='Final'
def fileop(a,b):
    print("From File----")
    print(a)
    print(b)
    Folder=a
    R1=b
    print(Folder)
    print(R1)
    df1 = pd.read_excel(str(Folder) + "/" + "Result.xls",sheet_name ='Sheet1', na_values=['NA'])

    #print(df1.keys())

    a = []
    index = []
    for x, y in enumerate(df1.columns):
        if "fail" in y:
            a.append(y)
            index.append(x)

    print(df1.keys())
    print(index)

    df1['final'] = np.where((df1.loc[:, df1.columns[index]] == "None").all(axis=1), "passed", "failed")



    writer = pd.ExcelWriter(str(Folder) + "/" + str(R1) + ".xls", engine=None)
    df1.to_excel(writer, sheet_name='Sheet1')
    writer.save()
    return df1
