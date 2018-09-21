import csv
import pandas as pd
from csv import DictReader
import numpy as np
import matplotlib.pyplot as plt
import xlrd


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
                new_handler = ''.join(map(lambda c: '' if c in '0123456789' else c, str(old_handler))).replace('//',
                                                                                                               '/')
                resTime = 0.00
                if len(row['time']) > 0:
                    resTime = float(row['time'])/1000
                if len(old_url) > 0:
                    summ_values = [row['level'], row['reqId'], resTime, row['timestamp'], 'url', new_url,
                                   row['microservice'], row['system'], row['responseCode']]
                    dictList.append(dict(zip(summ_keys, summ_values)))
                if len(old_handler) > 0:
                    summ_values = [row['level'], row['reqId'], resTime, row['timestamp'], 'handler', new_handler,
                                   row['microservice'], row['system'], row['responseCode']]
                    dictList.append(dict(zip(summ_keys, summ_values)))
            i = i + 1
            # if i%10000 == 0:
            #    print('Processed ', i, ' records')
            # if i == 40000:
            #    break

    # print(dictList)

    print('Processing completed; returning Dataframe')

    # with open(folder+'/'+fileName.replace('.csv', '_summ.csv'), 'w') as csvfile:
    #    writer = csv.DictWriter(csvfile, fieldnames=summ_keys)
    #    writer.writeheader()
    #    writer.writerows(dictList)

    df = pd.DataFrame(dictList)
    df = df[summ_keys]  # Arrange columns in required order
    # writer = pd.ExcelWriter(folder+'/'+fileName.replace('.csv','_summ.xlsx'))  # Writing Dataframe to Excel for specific build
    # df.to_excel(writer)
    # writer.save()

    df_pivot_endpoint_mean_time = df.groupby(by=['endpoint']).mean().reset_index()
    df_pivot_endpoint_mean_time.time = round(df_pivot_endpoint_mean_time.time, 2)
    df_pivot_endpoint_mean_time.rename(columns={'time': 'averageResponseTime'}, inplace=True)

    df_pivot_level_endpoint_mean_time = df.groupby(by=['level', 'endpoint']).mean().reset_index()
    df_pivot_level_endpoint_mean_time.time = round(df_pivot_level_endpoint_mean_time.time, 2)
    df_pivot_level_endpoint_mean_time.rename(columns={'time': 'averageResponseTime'}, inplace=True)

    df_pivot_success_endpoint_mean_time = df_pivot_level_endpoint_mean_time[
                                              df_pivot_level_endpoint_mean_time['level'] == 'debug'].loc[:,
                                          ['endpoint', 'averageResponseTime']]
    df_pivot_error_endpoint_mean_time = df_pivot_level_endpoint_mean_time[
                                            df_pivot_level_endpoint_mean_time['level'] == 'error'].loc[:,
                                        ['endpoint', 'averageResponseTime']]

    df_pivot_type_endpoint_mean_time = df.groupby(by=['type', 'endpoint']).mean().reset_index()
    df_pivot_type_endpoint_mean_time.time = round(df_pivot_type_endpoint_mean_time.time, 2)
    df_pivot_type_endpoint_mean_time.rename(columns={'time': 'averageResponseTime'}, inplace=True)

    df_pivot_handler_endpoint_mean_time = df_pivot_type_endpoint_mean_time[
                                              df_pivot_type_endpoint_mean_time['type'] == 'handler'].loc[:,
                                          ['endpoint', 'averageResponseTime']]
    df_pivot_url_endpoint_mean_time = df_pivot_type_endpoint_mean_time[
                                          df_pivot_type_endpoint_mean_time['type'] == 'url'].loc[:,
                                      ['endpoint', 'averageResponseTime']]

    df_pivot_level_count = df.groupby(by=['level']).count().reset_index()
    df_pivot_level_count = df_pivot_level_count.loc[:, ['level', 'endpoint']]
    df_pivot_level_count.rename(columns={'endpoint': 'transactionCount'}, inplace=True)

    df_pivot_endpoint_count = df.groupby(by=['level', 'endpoint']).count().reset_index()
    df_pivot_success_endpoint_count = df_pivot_endpoint_count[df_pivot_endpoint_count['level'] == 'debug'].loc[:,
                                      ['endpoint', 'time']]
    df_pivot_success_endpoint_count.rename(columns={'time': 'transactionCount'}, inplace=True)
    df_pivot_error_endpoint_count = df_pivot_endpoint_count[df_pivot_endpoint_count['level'] == 'error'].loc[:,
                                    ['endpoint', 'time']]
    df_pivot_error_endpoint_count.rename(columns={'time': 'transactionCount'}, inplace=True)

    print("processed")
    return [df_pivot_endpoint_mean_time,
            df_pivot_success_endpoint_mean_time,
            df_pivot_error_endpoint_mean_time,
            df_pivot_handler_endpoint_mean_time,
            df_pivot_url_endpoint_mean_time,
            df_pivot_level_count,
            df_pivot_success_endpoint_count,
            df_pivot_error_endpoint_count]


#fileName = 'D:/report/Mobile/logs_08092018/logs_08092018.csv'

#[df1, df2, df3, df4, df5, df6, df7, df8] = processMobileLogs(fileName)

