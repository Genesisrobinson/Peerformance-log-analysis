import csv
import pandas as pd
import numpy as np
from csv import DictReader

def processMobileLogs(fileName):

    fileName = fileName

    summ_keys = ['level', 'reqId', 'time', 'timestamp', 'type', 'endpoint', 'microservice', 'system', 'responseCode']
    dictList = []

    with open(fileName) as csvfile:
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
            #if i%10000 == 0:
                #print('Processed ', i, ' records')
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
    return df

def summaryview(fileFolder="D:/report/Mobile/logs_08092018/logs_08092018.csv"):
    df1=processMobileLogs(fileFolder)
    pivot = pd.pivot_table(df1, values='time', index="endpoint", aggfunc=np.average)
    df2 = pivot.reset_index()
    return df2



#fileName = 'D:/report/Mobile/logs_08092018/logs_08092018.csv'

#pivot=summaryview()
#print(pivot)
