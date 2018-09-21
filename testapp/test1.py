import pandas as pd

def convertDFtoOptions(df):
    lstOptions = str(df.values.tolist())
    strOptions = (str(lstOptions).replace('[','(')).replace(']',')')
    return strOptions

df = pd.DataFrame({'a':['AUT','DEU','NLD','IND','JPN','CHN'],
                   'b':['Austria','Germany','Netherland','India','Japan','China']})
strOptions = convertDFtoOptions(df)
print(strOptions)
