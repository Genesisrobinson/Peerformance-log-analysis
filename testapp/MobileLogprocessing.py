import csv
import pandas as pd
import numpy as np
from csv import DictReader

def processMobileLogs(fileFolder, fileName):

    folder = fileFolder
    fileName = fileName

    summ_keys = ['level', 'reqId', 'time', 'timestamp', 'type', 'endpoint', 'microservice', 'system', 'responseCode']
    dictList = []

    with open(folder+'/'+fileName) as csvfile:
        reader: DictReader = csv.DictReader(csvfile)
        i = 0
        for row in reader:
            if (row['level'] in ['debug', 'error', 'warn']):
                old_url = row['url']
                new_url = ''.join(map(lambda c: '' if c in '0123456789' else c, str(old_url))).replace('//', '/')
                old_handler = row['handler']
                new_handler = ''.join(map(lambda c: '' if c in '0123456789' else c, str(old_handler))).replace('//', '/')
                resTime = 0
                if len(row['time']) > 0:
                    resTime = int(row['time'])
                if len(old_url) > 0:
                    summ_values = [row['level'], row['reqId'], resTime, row['timestamp'], 'url', new_url, row['microservice'], row['system'], row['responseCode']]
                    dictList.append(dict(zip(summ_keys, summ_values)))
                if len(old_handler) > 0:
                    summ_values = [row['level'], row['reqId'], resTime, row['timestamp'], 'handler', new_handler, row['microservice'], row['system'], row['responseCode']]
                    dictList.append(dict(zip(summ_keys, summ_values)))
            i = i + 1
            if i%10000 == 0:
                print('Processed ', i, ' records')
            #if i == 40000:
            #    break

    #print(dictList)

    print('Processing completed; returning Dataframe')

    #with open(folder+'/'+fileName.replace('.csv', '_summ.csv'), 'w') as csvfile:
    #    writer = csv.DictWriter(csvfile, fieldnames=summ_keys)
    #    writer.writeheader()
    #    writer.writerows(dictList)

    df = pd.DataFrame(dictList)
    df = df[summ_keys] # Arrange columns in required order
    writer = pd.ExcelWriter(folder+'/'+fileName.replace('.csv','_summ.xlsx'))  # Writing Dataframe to Excel for specific build
    df.to_excel(writer)
    writer.save()

    return df

def summaryview():
    df1 = pd.read_excel("D:/performance/logs_08092018_summ.xlsx",sheet_name ='Sheet1', na_values=['NA'])
    #print(df1.keys())
    #table = pd.pivot_table(df1, values='time', index="endpoint", columns='level', aggfunc = np.sum)
    table=pd.DataFrame
    table = pd.pivot_table(df1, values='time', index="endpoint", aggfunc=np.average)
    Folder = 'd:/report/MGM'
    R1 = 'Result1'
    writer = pd.ExcelWriter(str(Folder) + "/" + str(R1) + ".xls", engine=None)
    table.to_excel(writer, sheet_name='Sheet1')
    writer.save()
    read = pd.read_excel(str(Folder) + "/" + str(R1) + ".xls", engine=None)
    print(read.keys())

    return read

    #df1pivot=df1.pivot(index='endpoint',columns="type", values='timestamp')
    #print(df1pivot)
    #xlist = list(df1['endpoint'].unique().tolist())
    #print(xlist)

#fileFolder = 'D:/New folder'
#fileName = 'logs_08092018.csv'

#df1 = processMobileLogs(fileFolder, fileName)
#print('Rows and Columns in the Dataframe returned : ', df1.shape)


#pivot=summaryview()
#print(pivot["endpoint"])
#print(pivot["time"])