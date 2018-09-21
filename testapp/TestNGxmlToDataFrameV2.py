# Reading xml using ElementTree
# =============================
print('=============================')
print('Reading xml using ElementTree')
print('=============================')

import xml.etree.ElementTree as ET
import pandas as pd
import numpy as np
import os

def parseTestNGXML(fileName):
    tree = ET.parse(fileName)
    root = tree.getroot()
    #print(root.tag) # Returns testng-results
    dictList = []
    keys = ['suite', 'suiteDuration', 'module', 'moduleDuration', 'testclass', 'testclassDuration', 'method', 'methodDuration', 'status', 'is.config', 'class', 'message', 'full-stacktrace']
    values = []
    for elem in root:
    #    print(' '*4, elem.tag)
        if (elem.tag == 'suite'): # Fetch Suite Name
            suite = elem.attrib['name']
            suiteDuration = elem.attrib['duration-ms']
            #print(' '*4, suite)
            for subelem in elem: # Fetch Module Name
                if (subelem.tag == 'test'):
                    module = subelem.attrib['name']
                    moduleDuration = elem.attrib['duration-ms']
                    #print(' '*8, module)
                    for ssubelem in subelem: # Fetch TestClass Name
                        testclass = ssubelem.attrib['name']
                        testclassDuration = elem.attrib['duration-ms']
                        #print(' '*12, testclass)
                        for sssubelem in ssubelem: # Fetch Method Name, Status, Is-Config
                            method = sssubelem.attrib['name']
                            methodDuration = elem.attrib['duration-ms']
                            # isConfig = sssubelem.attrib['is-config']
                            if method in ('afterMethod', 'afterSuite', 'beforeMethod', 'beforeSuite', 'beforeWebMethod', 'beforeWebTest'):
                                isConfig = 'TRUE'
                            else:
                                isConfig = ''
                            #print(method, isConfig)
                            status = sssubelem.attrib['status']
                            # print(' ' * 16, method, ' - ', isConfig, ' - ', 'status')
                            if status == 'FAIL':
                                for ssssubelem in sssubelem: # Fetch exception details
                                    if ssssubelem.tag == 'exception':
                                        vClass = ssssubelem.attrib['class']
                                        #print(' ' * 20, vClass)
                                        for sssssubelem in ssssubelem:
                                            if sssssubelem.tag == 'message':
                                                message = sssssubelem.text
                                                #print(' '*24, message)
                                            if sssssubelem.tag == 'full-stacktrace':
                                                full_stacktrace = sssssubelem.text
                                                #print(' '*24, full_stacktrace)
                                                values = [suite, suiteDuration, module, moduleDuration, testclass, testclassDuration, method, methodDuration, status, isConfig, vClass, message, full_stacktrace]
                                                dictList.append(dict(zip(keys, values)))
                            else:
                                values = [suite, suiteDuration, module, moduleDuration, testclass, testclassDuration, method, methodDuration, status, isConfig, '', '', '']
                                dictList.append(dict(zip(keys, values)))
    df = pd.DataFrame(dictList)
    df = df[['suite', 'suiteDuration', 'module', 'moduleDuration', 'testclass', 'testclassDuration', 'method', 'methodDuration', 'status', 'is.config', 'class', 'message', 'full-stacktrace']]
    #print(df)
    return df

def summarizeTestResults(testNGDataFrame):
    #summ_keys = ['module', 'testclass', 'cnt_pass', 'cnt_fail', 'cnt_skip', 'status', 'class', 'message', 'full-stacktrace']
    summ_keys = ['module', 'testclass', 'status', 'class', 'message', 'full-stacktrace']
    summ_values = []
    dictList = []

    df_tmp = testNGDataFrame # converting TestNG file to Dataframe

    # print(df_tmp.count())

    df_tmp = df_tmp.loc[df_tmp['is.config'] == ''] # Remove rows with is.config = 'TRUE'
    # Remove columns not needed for summary
    df_tmp = df_tmp.drop(columns=['suite', 'suiteDuration', 'moduleDuration', 'testclassDuration', 'methodDuration'])
    #df_tmp_sorted = df_tmp.sort_values(['module', 'testclass', 'method']) # Sort based on module, test class and method
    df_tmp_sorted = df_tmp.reset_index(drop=True) #Resetting the index by dropping existing index
    del df_tmp
    df_tmp = df_tmp_sorted
    del df_tmp_sorted
    print(df_tmp.count())

    module_nm = ''
    testclass_nm = ''
    cnt_pass = 0
    cnt_fail = 0
    cnt_skip = 0
    final_status = ''
    class_nm = ''
    txt_msg = ''
    txt_stacktrace = ''

    for index, row in df_tmp.iterrows():
        if index == 0:
            module_nm = row['module']
            testclass_nm = row['testclass']

        module_nm_new = row['module']
        testclass_nm_new = row['testclass']

        if testclass_nm != testclass_nm_new:
            if cnt_fail > 0:
                final_status = 'FAIL'
            elif cnt_skip > 0:
                final_status = 'SKIP'
            elif cnt_pass > 0:
                final_status = 'PASS'

            #summ_values = [str(module_nm).replace('(failed)',''), testclass_nm, cnt_pass, cnt_fail, cnt_skip, final_status, class_nm, txt_msg, txt_stacktrace]
            summ_values = [str(module_nm).replace('(failed)', ''), testclass_nm, final_status, class_nm, txt_msg, txt_stacktrace]
            dictList.append(dict(zip(summ_keys, summ_values)))
            print(summ_values)

            module_nm = module_nm_new
            testclass_nm = testclass_nm_new
            cnt_skip = 0
            cnt_fail = 0
            cnt_pass = 0

        if row['status'] == 'PASS':
            cnt_pass = cnt_pass + 1
        elif row['status'] == 'FAIL':
            cnt_fail = cnt_fail + 1
        elif row['status'] == 'SKIP':
            cnt_skip = cnt_skip + 1

        class_nm = row['class']
        txt_msg = row['message']
        txt_stacktrace = row['full-stacktrace']

        if index == (len(df_tmp) - 1):
            if cnt_fail > 0:
                final_status = 'FAIL'
            elif cnt_skip > 0:
                final_status = 'SKIP'
            elif cnt_pass > 0:
                final_status = 'PASS'

            #summ_values = [str(module_nm).replace('(failed)',''), testclass_nm, cnt_pass, cnt_fail, cnt_skip, final_status, class_nm, txt_msg, txt_stacktrace]
            summ_values = [str(module_nm).replace('(failed)', ''), testclass_nm, final_status, class_nm, txt_msg, txt_stacktrace]
            dictList.append(dict(zip(summ_keys, summ_values)))
            #print(summ_values)

    df = pd.DataFrame(dictList)
    #df = df[['module', 'testclass', 'cnt_pass', 'cnt_fail', 'cnt_skip', 'status', 'class', 'message', 'full-stacktrace']]
    df = df[['module', 'testclass', 'status', 'class', 'message', 'full-stacktrace']]
    return df

def generateTestSummary(jenkinsJobFolder, builds, outputFolder):
    #dirList = filter(lambda x: os.path.isdir(jenkinsJobFolder + 'builds/'+ x), os.listdir(jenkinsJobFolder + 'builds/'))
    result = pd.DataFrame()
    dictDF = {}
    for x in builds.split(','):
        x = x.strip(' ')
        fileName = jenkinsJobFolder + x + '/testng-results.xml' # Getting TestNG file name
        dfnm = x
        print(x, fileName)
        df1 = parseTestNGXML(fileName)
        df2 = summarizeTestResults(df1)
        dictDF[dfnm] = df2
        summFileName = outputFolder + x + '_summ.xlsx'  # Generating file name to save Dataframe
        writer = pd.ExcelWriter(summFileName)  # Writing Dataframe to Excel for specific build
        df2.to_excel(writer)
        writer.save()
        if len(result) == 0:
            result = df2
            # below line is not working here; hence taken value of x in x1 and updated column names at end
            #result.rename(columns={'status':'status'+x, 'class':'class'+x, 'message':'message'+x, 'full-stacktrace':'full-stacktrace'+x}, inplace=True)
            x1 = x
        else:
            result = pd.merge(result, df2, how='outer', on=['module', 'testclass'], suffixes=('', x))
    result.rename(columns={'status': 'status' + x1, 'class': 'class' + x1, 'message': 'message' + x1, 'full-stacktrace': 'full-stacktrace' + x1}, inplace=True)

    # Adding column for Package Name
    temp = pd.DataFrame(result['testclass'].str.rsplit('.', 1).tolist(), columns="package testclass".split())
    result.insert(loc=1, column='package', value=temp['package'])

    # Adding column for final status of test case
    cols = [col for col in result.columns if 'status' in col]
    finalStatus=[]
    summ_keys=['module', 'testclass', 'finalStatus']
    for ind, row in result.iterrows():
        fStatus = ''
        for col in cols:
            if row[col] in ['PASS', 'FAIL', 'SKIP']:
                fStatus = row[col]
        summ_values = [row['module'], row['testclass'], fStatus]
        finalStatus.append(dict(zip(summ_keys, summ_values)))

    df = pd.DataFrame(finalStatus)
    result = pd.merge(result, df, how='outer', on=['module', 'testclass'], suffixes=('', ''))
    print(result)

    # Generate DF for Pacakge wise Summary
    df_pivot = result.pivot_table(index=['module', 'package'],columns=['finalStatus'],aggfunc='count',values='testclass', margins=True)
    print(df_pivot)

    writer = pd.ExcelWriter(outputFolder + 'FinalSummary.xlsx')  # Writing Dataframe to Excel for specific build
    result.to_excel(writer, index=False, sheet_name='Execution Data')
    df_pivot.to_excel(writer, sheet_name='Overall Summary')
    writer.save()

    return [result, df_pivot]

jenkinsJobFolder = 'D:/report/tmp/DMP/'
outputFolder = 'D:/report/tmp/'
generateTestSummary(jenkinsJobFolder, '13, 14,15,68,70,72', outputFolder)

# Implementation from Package / Module
# ====================================
#from testNG import MergeTestNGxmlsToExcel as MTE
#folder = 'D:/tmp/DMP/'
#result = MTE.generateTestSummary(folder)
#print(result)
