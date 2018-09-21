# import spur
#
# shell = spur.SshShell(hostname="s2aurora01p", username="ftizazu", password="Testing255!")
# result = shell.run(["echo", "-n", "hello"])
# print (result.output) # prints hello

import base64
import paramiko
import time
import pandas as pd

def fetchAuroraAlerts(auroraServer, userName, passWord, stime, etime, logFilePath):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(auroraServer, username=userName, password=passWord)
    #stdin, stdout, stderr = client.exec_command('cd /auroralog01/logs/mgm-aurora-tps-dist-3.13.3/tps1p')
    stdin, stdout, stderr = client.exec_command('pwd')
    for line in stdout:
        print('... ' + line.strip('\n'))
    execCommand = 'sed -n "/'+stime+':/,/'+etime+':/p" '+logFilePath+'  | grep -E "(sev)" >/home/ftizazu/s2aurora01p_tps_alert_logs_17Sep2018.csv'
    stdin, stdout, stderr = client.exec_command(execCommand)
    time.sleep(5)
    stdin, stdout, stderr = client.exec_command('cat /home/ftizazu/s2aurora01p_tps_alert_logs_17Sep2018.csv')

    keys = ['server', 'timeStamp', 'severity', 'status', 'channel', 'method', 'errorType', 'errorMessage']
    dictList = []
    i = 0
    for line in stdout:
        try:
            rec = line.strip('\n').split(',')
            serverName = rec[2].split('> ')[0]
            timeStamp = (rec[2].split('> ')[1]).split(' (')[0]
            sev = (rec[2].split(' (')[1]).split(')...')[0]
            status = (rec[2].split('...')[1]).split(' {')[0]
            channelName = rec[2].split(' {')[1]
            methodName = rec[3]
            errCategory = (rec[4].split('<')[1]).split('>')[0]
            errMessage = (rec[4].split('[')[1]).split(']')[0]

            results = [serverName, timeStamp, sev, status, channelName, methodName, errCategory, errMessage]
            dictList.append(dict(zip(keys, results)))
        except:
            print('Record could not be processed: ', line.strip('\n'))
    client.close()
    if len(dictList) > 0:
        df = pd.DataFrame(dictList)
        df = df[keys]
        print('Number of records from ', auroraServer, df.__len__())
    else:
        print('No data found in Alerts on ', server)
    return df

def generateSummary(excelfile,stime, etime, auroraVersion):
    auroraServer1 = 's2aurora01p'
    auroraServer2 = 's2aurora03p'
    auroraServer3 = 's2aurora05p'
    logFilePathNode1 = '/auroralog01/logs/mgm-aurora-tps-dist-'+auroraVersion+'/tps1p/aurora.tps.alert.log.*'
    logFilePathNode2 = '/auroralog01/logs/mgm-aurora-tps-dist-'+auroraVersion+'/tps2p/aurora.tps.alert.log.*'
    logFilePathNode3 = '/auroralog01/logs/mgm-aurora-tps-dist-'+auroraVersion+'/tps3p/aurora.tps.alert.log.*'
    userName = 'ftizazu'
    passWord = 'Testing255!'

    df1 = fetchAuroraAlerts(auroraServer1, userName, passWord, stime, etime, logFilePathNode1)
    df2 = fetchAuroraAlerts(auroraServer2, userName, passWord, stime, etime, logFilePathNode2)
    df3 = fetchAuroraAlerts(auroraServer3, userName, passWord, stime, etime, logFilePathNode3)

    result = df1
    result = result.append(df2, ignore_index=True)
    result = result.append(df3, ignore_index=True)
    print('Total number of records from all nodes:', result.__len__())

    # Generate DF for Server wise Error Count Summary
    df_server_summ = result.pivot_table(index=['server'],aggfunc='count',values='timeStamp', margins=True)

    # Generate DF for Error Category and Server wise Error Count Summary
    df_err_server_summ = result.pivot_table(index=['errorType'],columns=['server'],aggfunc='count',values='timeStamp', margins=True)

    # Generate DF for Method and Server wise Error Count Summary
    df_method_server_summ = result.pivot_table(index=['method'],columns=['server'],aggfunc='count',values='timeStamp', margins=True)

    # Generate DF for Error Category, Method and Server wise Error Count Summary
    df_err_method_server_summ = result.pivot_table(index=['errorType', 'method'],columns=['server'],aggfunc='count',values='timeStamp', margins=True)

    writer = pd.ExcelWriter(excelfile)  # Writing Dataframe to Excel for specific build
    df_server_summ.to_excel(writer, sheet_name='ServerSumm')
    df_err_server_summ.to_excel(writer, sheet_name='ErrCategorySumm')
    df_method_server_summ.to_excel(writer, sheet_name='MethodSumm')
    df_err_method_server_summ.to_excel(writer, sheet_name='ErrCategoryMethodSumm')
    result.to_excel(writer, index=False, sheet_name='Error Data')
    writer.save()
    df_server_summ = df_server_summ.reset_index()
    #del df_server_summ['index']

    return df_server_summ, df_err_server_summ, df_method_server_summ, df_err_method_server_summ

# Implementation:

stime = '20180914-13:40' # Start Time
etime = '20180914-13:50' # End Time
auroraVersion = '3.13.3' # Aurora Version - This is to locate the log folder path

# [df_server_summ, df_err_server_summ, df_method_server_summ, df_err_method_server_summ] = generateSummary("d:/AuroraAlertLogsSummary.xlsx",stime, etime, auroraVersion)
# print("df_server_summ")
# print(df_server_summ)
# print("df_err_server_summ")
# print(df_err_server_summ)
# print("df_method_server_summ")
# print(df_method_server_summ)
# print("df_err_method_server_summ")
# print(df_err_method_server_summ)
