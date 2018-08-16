## Calculating logical conditions in data frame elements
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from django.http import HttpResponse

def fileop():
    Folder='d:/report/'
    R1="Final"
    df1 = pd.read_excel('d:/report/MGM/result/Result2.xls',sheet_name ='Sheet1', na_values=['NA'])

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
    return df1.keys()
