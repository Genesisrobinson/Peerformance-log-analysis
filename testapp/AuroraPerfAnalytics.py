import cx_Oracle as cx
import pandas as pd
import xlsxwriter


def runQuery(query):
    df = pd.DataFrame()
    con = cx.connect('APPSERV_AURORASR4[AURORA_SR4]', 'Vi0l3t', 'mlifeoradbrscan.mgmresorts.local:1526/aixmlppd')
    cursor = con.cursor()
    cursor.execute(query)
    dictList = []

    keys = ['Agent', 'Leg', 'transCount', 'avgResponseTime', 'medResponseTime', 'maxResponseTime']

    for results in cursor:
        dictList.append(dict(zip(keys, results)))

    print(len(dictList))

    cursor.close()
    con.close()

    if len(dictList) > 0:
        df = pd.DataFrame(dictList)
        df = df[keys]

    return df


def AuroraPerfAnalyticsAggregate(stime, etime):
    query = """select agent, leg, count(*) cnt, round(avg(procTime)/1000000, 2) avg,
        round(median(procTime)/1000000, 2) med, round(max(procTime)/1000000, 2) maxi
        from message_processing_time
        where Timestamp between '""" + stime + "' and '" + etime + "' group by agent, leg order by 4 desc"

    df = runQuery(query)
    return df


def AuroraPerfAnalyticsDMP(df_agg):
    filterList = ['aurora-uat2-client-vdara', 'aurora-uat2-client-montecarlo', 'aurora-uat2-client-mirage',
                  'aurora-uat2-client-mandalaybay', 'aurora-uat2-client-excalibur', 'aurora-uat2-client-aria',
                  'aurora-uat2-client-mgmgrandlv', 'aurora-uat2-client-bellagio', 'aurora-uat2-client-beaurivage',
                  'aurora-uat2-client-delano', 'aurora-uat2-client-goldstrike', 'aurora-uat2-client-luxor',
                  'aurora-uat2-client-mgmgranddetroit', 'aurora-uat2-client-mgmnationalharbor',
                  'aurora-uat2-client-newyorknewyork', 'aurora-uat2-client-signature']

    df = df_agg[df_agg['Agent'].isin(filterList)]
    df = df.reset_index()
    del df['index']

    return df


def AuroraPerfAnalyticsMLIFE(df_agg):
    df = df_agg[df_agg['Agent'].str.contains('cabanas')]
    df = df.reset_index()
    del df['index']

    return df


def AuroraPerfAnalyticsICE(df_agg):
    df = df_agg[df_agg['Agent'].str.contains('ice')]
    df = df.reset_index()
    del df['index']

    return df


def AuroraPerfAnalyticsTPS(df_agg):
    filterList = ['aurora-uat2-1', 'aurora-uat2-2', 'aurora-uat2-3']

    df = df_agg[df_agg['Agent'].isin(filterList)]
    df = df.reset_index()
    del df['index']

    return df


def AuroraPerfAnalyticsARIS(df_agg):
    filterList = ['aurora-aris-uat2-1', 'aurora-aris-uat2-2', 'aurora-aris-uat2-3', 'aurora-aris-uat2-4']

    df = df_agg[df_agg['Agent'].isin(filterList)]
    df = df.reset_index()
    del df['index']

    return df


def AuroraPerfAnalyticsDIST(df_agg):
    filterList = ['GetRoomPricingAndAvailabilityExRequest']

    df = df_agg[df_agg['Leg'].isin(filterList)]
    df = df.reset_index()
    del df['index']

    return df


def HighCostUrls(stime, etime, avgResponseTimeGreaterThan):
    if avgResponseTimeGreaterThan < 10:
        avgResponseTimeGreaterThan = 10
    query = """select * from message_processing_time 
                where Timestamp between '""" + stime + "' and '" + etime + "' and proctime > " + str(
        avgResponseTimeGreaterThan)

    con = cx.connect('APPSERV_AURORASR4[AURORA_SR4]', 'Vi0l3t', 'mlifeoradbrscan.mgmresorts.local:1526/aixmlppd')
    keys = ['TimeStamp', 'Transaction', 'Agent', 'Leg', 'QueueTime', 'ProcessTime']
    df = pd.read_sql(query, con)
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
            # 'fill': {'color': brews['Spectral'][i]},
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
    avgResponseTimeGreaterThan = float(avgResponseTimeGreaterThan)

    df_agg = pd.DataFrame()
    df_dmp = pd.DataFrame()
    df_ice = pd.DataFrame()
    df_mlife = pd.DataFrame()
    df_tps = pd.DataFrame()
    df_aris = pd.DataFrame()

    writer = pd.ExcelWriter(excel_file, engine='xlsxwriter')
    df_agg = AuroraPerfAnalyticsAggregate(stime, etime)
    if len(df_agg) > 0:
        df_agg.to_excel(writer, sheet_name='Aggregate', index=False)

        df_dmp = AuroraPerfAnalyticsDMP(df_agg)
        df_ice = AuroraPerfAnalyticsICE(df_agg)
        df_mlife = AuroraPerfAnalyticsMLIFE(df_agg)
        df_tps = AuroraPerfAnalyticsTPS(df_agg)
        df_aris = AuroraPerfAnalyticsARIS(df_agg)
        df_dist = AuroraPerfAnalyticsDIST(df_agg)

        df_agg = df_agg[df_agg['avgResponseTime'] > avgResponseTimeGreaterThan]
        df_agg['Agent'] = df_agg[['Agent', 'Leg']].apply(lambda x: '-'.join(x), axis=1)
        del df_agg['Leg']

        if len(df_dist) > 0:
            df_dist.to_excel(writer, sheet_name='DIST', index=False)
            df_dist['Agent'] = df_dist[['Agent', 'Leg']].apply(lambda x: '-'.join(x), axis=1)
            del df_dist['Leg']

        if len(df_dmp) > 0:
            df_dmp.to_excel(writer, sheet_name='DMP', index=False)
            df_dmp = df_dmp[df_dmp['avgResponseTime'] > avgResponseTimeGreaterThan]
            df_dmp['Agent'] = df_dmp[['Agent', 'Leg']].apply(lambda x: '-'.join(x), axis=1)
            del df_dmp['Leg']

        if len(df_ice) > 0:
            df_ice.to_excel(writer, sheet_name='ICE', index=False)
            df_ice = df_ice[df_ice['avgResponseTime'] > avgResponseTimeGreaterThan]
            df_ice['Agent'] = df_ice[['Agent', 'Leg']].apply(lambda x: '-'.join(x), axis=1)
            del df_ice['Leg']

        if len(df_mlife) > 0:
            df_mlife.to_excel(writer, sheet_name='MLIFE', index=False)
            df_mlife = df_mlife[df_aris['avgResponseTime'] > avgResponseTimeGreaterThan]
            df_mlife['Agent'] = df_mlife[['Agent', 'Leg']].apply(lambda x: '-'.join(x), axis=1)
            del df_mlife['Leg']

        if len(df_tps) > 0:
            df_tps.to_excel(writer, sheet_name='TPS', index=False)
            df_tps = df_tps[df_tps['avgResponseTime'] > avgResponseTimeGreaterThan]
            df_tps['Agent'] = df_tps[['Agent', 'Leg']].apply(lambda x: '-'.join(x), axis=1)
            del df_tps['Leg']

        if len(df_aris) > 0:
            df_aris.to_excel(writer, sheet_name='ARIS', index=False)
            df_aris = df_aris[df_aris['avgResponseTime'] > avgResponseTimeGreaterThan]
            df_aris['Agent'] = df_aris[['Agent', 'Leg']].apply(lambda x: '-'.join(x), axis=1)
            del df_aris['Leg']

    else:
        print('No data available for given criteria')

    # Close the Pandas Excel writer and output the Excel file.
    # ========================================================
    writer.save()
    return [df_agg, df_dmp, df_ice, df_mlife, df_tps, df_aris, df_dist]


#excel_file = 'D:/AuroraPerfStats.xlsx'
#stime = '10-SEP-18 11.30.48.019000000 PM'
#etime = '11-SEP-18 02.17.15.625000000 AM'
#avgResponseTimeGreaterThan = 2

#[df_agg,df_dmp,df_ice,df_mlife,df_tps,df_aris,df_dist]=generateExcelCharts(excel_file, stime, etime, avgResponseTimeGreaterThan)

# print("df_agg")
# print(df_agg)
# print("df_ice")
# print(df_ice)
# print("df_mlife")
# print(df_mlife)
# print("df_tps")
# print(df_tps)
# print("df_aris")
# print(df_aris)re
