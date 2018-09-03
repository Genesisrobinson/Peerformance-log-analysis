import cx_Oracle as cx
import pandas as pd
import xlsxwriter

def runQuery(query, avgResponseTimeGreaterThan):
    df = pd.DataFrame()
    con = cx.connect('APPSERV_AURORASR4[AURORA_SR4]', 'Vi0l3t', 'mlifeoradbrscan.mgmresorts.local:1526/aixmlppd')
    cursor = con.cursor()
    cursor.execute(query)
    dictList = []

    keys = ['Agent-Leg', 'transCount', 'avgResponseTime', 'medResponseTime', 'maxResponseTime']

    for results in cursor:
        if results[3] >= avgResponseTimeGreaterThan:
            dictList.append(dict(zip(keys, results)))

    print(len(dictList))

    cursor.close()
    con.close()

    if len(dictList) > 0:
        df = pd.DataFrame(dictList)
        df = df[keys]

    return df

def AuroraPerfAnalyticsAggregate(stime, etime, avgResponseTimeGreaterThan):
    query = """select agent||'-'||leg, count(*) cnt, round(avg(procTime)/1000000, 2) avg,
        round(median(procTime)/1000000, 2) med, round(max(procTime)/1000000, 2) maxi
        from message_processing_time
        where Timestamp between '""" + stime + "' and '" + etime + "' group by agent||'-'||leg order by 4 desc"

    df = runQuery(query, avgResponseTimeGreaterThan)
    return df

def AuroraPerfAnalyticsDMP(stime, etime, avgResponseTimeGreaterThan):
    query = """select agent||'-'||leg, count(*) cnt, round(avg(procTime)/1000000, 2) avg,
        round(median(procTime)/1000000, 2) med, round(max(procTime)/1000000, 2) maxi
        from message_processing_time
        where agent in ('aurora-uat2-client-vdara','aurora-uat2-client-montecarlo','aurora-uat2-client-mirage',
                'aurora-uat2-client-mandalaybay','aurora-uat2-client-excalibur','aurora-uat2-client-aria',
                'aurora-uat2-client-mgmgrandlv','aurora-uat2-client-bellagio','aurora-uat2-client-beaurivage',
                'aurora-uat2-client-delano','aurora-uat2-client-goldstrike','aurora-uat2-client-luxor',
                'aurora-uat2-client-mgmgranddetroit','aurora-uat2-client-mgmnationalharbor',
                'aurora-uat2-client-newyorknewyork','aurora-uat2-client-signature')
        and Timestamp between '""" + stime + "' and '" + etime + "' group by agent||'-'||leg order by 4 desc"

    df = runQuery(query, avgResponseTimeGreaterThan)
    return df

def AuroraPerfAnalyticsMLIFE(stime, etime, avgResponseTimeGreaterThan):
    query = """select agent||'-'||leg, count(*) cnt, round(avg(procTime)/1000000, 2) avg,
        round(median(procTime)/1000000, 2) med, round(max(procTime)/1000000, 2) maxi
        from message_processing_time
        where agent like '%cabanas'
        and Timestamp between '""" + stime + "' and '" + etime + "' group by agent||'-'||leg order by 4 desc"

    df = runQuery(query, avgResponseTimeGreaterThan)
    return df

def AuroraPerfAnalyticsICE(stime, etime, avgResponseTimeGreaterThan):
    query = """select agent||'-'||leg, count(*) cnt, round(avg(procTime)/1000000, 2) avg,
        round(median(procTime)/1000000, 2) med, round(max(procTime)/1000000, 2) maxi
        from message_processing_time
        where agent like '%ice%'
        and Timestamp between '""" + stime + "' and '" + etime + "' group by agent||'-'||leg order by 4 desc"

    df = runQuery(query, avgResponseTimeGreaterThan)
    return df

def AuroraPerfAnalyticsTPS(stime, etime, avgResponseTimeGreaterThan):
    query = """select agent||'-'||leg, count(*) cnt, round(avg(procTime)/1000000, 2) avg,
        round(median(procTime)/1000000, 2) med, round(max(procTime)/1000000, 2) maxi
        from message_processing_time
        where agent in ('aurora-uat2-1', 'aurora-uat2-2', 'aurora-uat2-3')
        and Timestamp between '""" + stime + "' and '" + etime + "' group by agent||'-'||leg order by 4 desc"

    df = runQuery(query, avgResponseTimeGreaterThan)
    return df

def AuroraPerfAnalyticsARIS(stime, etime, avgResponseTimeGreaterThan):
    query = """select agent||'-'||leg, count(*) cnt, round(avg(procTime)/1000000, 2) avg,
        round(median(procTime)/1000000, 2) med, round(max(procTime)/1000000, 2) maxi
        from message_processing_time
        where agent in ('aurora-aris-uat2-1', 'aurora-aris-uat2-2', 'aurora-aris-uat2-3', 'aurora-aris-uat2-4')
        and Timestamp between '""" + stime + "' and '" + etime + "' group by agent||'-'||leg order by 4 desc"

    df = runQuery(query, avgResponseTimeGreaterThan)
    return df

def addNewChart(writer, sheet_name, df, chartTitle, x_axis_nm, y_axis_nm, chartWidth, chartHeight):
    df.to_excel(writer, sheet_name=sheet_name)
    workbook = writer.book
    worksheet = writer.sheets[sheet_name]

    # Create a chart object.
    chart = workbook.add_chart({'type': 'column'})

    max_row = len(df) + 1
    for i in range(len(df.columns)):
        col = i + 1
        chart.add_series({
            'name': [sheet_name, 0, col],
            'categories': [sheet_name, 1, 1, max_row, col],
            'values': [sheet_name, 1, col, max_row, col],
            #'fill': {'color': brews['Spectral'][i]},
        })

    # Configure the chart axes.
    chart.set_y_axis({'name': y_axis_nm, 'major_gridlines': {'visible': False}})
    chart.set_x_axis({'name': x_axis_nm, 'num_font': {'rotation': 45}})
    chart.set_legend({'position': 'none'})
    chart.set_size({'width': chartWidth, 'height': chartHeight})
    chart.set_title({'name': chartTitle})
    chart.set_legend({'position': 'top'})

    # Insert the chart into the worksheet.
    worksheet.insert_chart('I1', chart)


def generateExcelCharts(excel_file, stime, etime, avgResponseTimeGreaterThan):
    df_agg = pd.DataFrame()
    df_dmp = pd.DataFrame()
    df_ice = pd.DataFrame()
    df_mlife = pd.DataFrame()
    df_tps = pd.DataFrame()
    df_aris = pd.DataFrame()

    writer = pd.ExcelWriter(excel_file, engine='xlsxwriter')
    df_agg = AuroraPerfAnalyticsAggregate(stime, etime, avgResponseTimeGreaterThan)
    df_dmp = AuroraPerfAnalyticsDMP(stime, etime, avgResponseTimeGreaterThan)
    df_ice = AuroraPerfAnalyticsICE(stime, etime, avgResponseTimeGreaterThan)
    df_mlife = AuroraPerfAnalyticsMLIFE(stime, etime, avgResponseTimeGreaterThan)
    df_tps = AuroraPerfAnalyticsTPS(stime, etime, avgResponseTimeGreaterThan)
    df_aris = AuroraPerfAnalyticsARIS(stime, etime, avgResponseTimeGreaterThan)

    if len(df_agg) > 0:
        addNewChart(writer, 'Aggregate', df_agg, 'Aggregate Transactions Stats', 'Agent-Leg', 'Count \ Response Time (Sec)', 1300, 750)
    else:
        print('No data available for given criteria')
    if len(df_dmp) > 0:
        addNewChart(writer, 'DMP', df_dmp, 'DMP Transactions Stats', 'Agent-Leg', 'Count \ Response Time (Sec)', 1300, 750)
    if len(df_ice) > 0:
        addNewChart(writer, 'ICE', df_ice, 'ICE Transactions Stats', 'Agent-Leg', 'Count \ Response Time (Sec)', 1300, 750)
    if len(df_mlife) > 0:
        addNewChart(writer, 'Mlife', df_mlife, 'Mlife Transactions Stats', 'Agent-Leg', 'Count \ Response Time (Sec)', 1300, 750)
    if len(df_tps) > 0:
        addNewChart(writer, 'TPS', df_tps, 'TPS Transactions Stats', 'Agent-Leg', 'Count \ Response Time (Sec)', 1300, 750)
    if len(df_aris) > 0:
        addNewChart(writer, 'ARIS', df_aris, 'ARIS Transactions Stats', 'Agent-Leg', 'Count \ Response Time (Sec)', 1300, 750)

    # Close the Pandas Excel writer and output the Excel file.
    # ========================================================
    writer.save()
    return [df_agg,df_dmp,df_ice,df_mlife,df_tps,df_aris]

excel_file = 'D:/AuroraPerfStats.xlsx'
stime = '31-AUG-18 02.12.48.019000000 AM'
etime = '31-AUG-18 05.17.15.625000000 AM'
avgResponseTimeGreaterThan = 2

[df_agg,df_dmp,df_ice,df_mlife,df_tps,df_aris]=generateExcelCharts(excel_file, stime, etime, avgResponseTimeGreaterThan)

print("df_agg")
print(df_agg)
print(df_dmp)
print(df_ice)
print(df_mlife)
print(df_tps)
print(df_aris)
