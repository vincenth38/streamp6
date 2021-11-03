import pandas as pd
import gspread
from gspread_dataframe import set_with_dataframe
import datetime

# from gsheetsdb import connect
# import gspread



def import_clean():
    sheet_id = '19VyS_zz1iy8iK2pTSAumquQp6TWMrxxuYt_61t2IBDk'
    sheet_name = 'clean'
    # url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}'
    url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&sheet={sheet_name}'
    # df = pd.DataFrame
    df = pd.read_csv(url)
    # df = df.apply(pd.to_numeric, errors='coerce')
    df['Planned Units'] = pd.to_numeric(df['Planned Units'])
    df['Remaining Units'] = pd.to_numeric(df['Remaining Units'])
    df['At Completion Units'] = pd.to_numeric(df['At Completion Units'])
    df['Planned Duration'] = pd.to_numeric(df['Planned Duration'])
    df['Remaining Duration'] = pd.to_numeric(df['Remaining Duration'])
    df['At Completion Duration'] = pd.to_numeric(df['At Completion Duration'])
    df['Planned Labor Units'] = pd.to_numeric(df['Planned Labor Units'])
    df['Activity % Complete'] = pd.to_numeric(df['Activity % Complete'])
    df = df.loc[:, ~df.columns.duplicated()]
    return df


def import_data():
    sheet_id = '1D2_X4p0qnX1C6cmizv4gJtGiaTY3RPNUW9qJyJaGsCU'
    sheet_name = 'ressources'
    url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}'
    df = pd.DataFrame
    df = pd.read_csv(url)

    # df_ressources= pd.read_csv(f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet=ressources', error_bad_lines=False)
    df_BL = pd.read_csv(f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet=baseline', error_bad_lines=False)
    df_Gantt = pd.read_csv(f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet=gantt', error_bad_lines=False)
    df_WBS = pd.read_csv(f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet=wbs', error_bad_lines=False)
    df_res_cat = pd.read_csv(f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet=cat_ressources', error_bad_lines=False)


    # Clean IDs
    df_Gantt['Activity ID'] = df_Gantt['Activity ID'].astype(str)
    df_Gantt['Activity ID'] = df_Gantt['Activity ID'].str.strip()
    df['Activity ID'] = df['Activity ID'].str.strip()
    df['Activity ID'] = df['Activity ID'].astype(str)
    # Clean WBS Path
    df_Gantt['WBS Path'] = df_Gantt['WBS Path'].str.strip()
    df_Gantt['WBS Path'] = df_Gantt['WBS Path'].astype(str)
    df['WBS Path'] = df['WBS Path'].str.strip()
    df['WBS Path'] = df['WBS Path'].astype(str)


    # Sfocus on 1.03
    df['L2'] = df['WBS Path'].str[:4]
    df = df[(df['L2'] == '1.03')]
    df['L3'] = df['WBS Path'].str[:7]
    df['L4'] = df['WBS Path'].str[:10]
    df['L5'] = df['WBS Path'].str[:13]
    # Select No Ressoures activitiy from Gantt
    df_No_Res = df_Gantt[(df_Gantt['Resource IDs'].isnull()) & (df_Gantt['WBS Path'].str.startswith('1.03'))]
    # Add No ressources activity to the reources main tables
    df = pd.concat([df, df_No_Res], axis=0, ignore_index=True)


    # Add Names for each WBS Level
    df_WBS['WBS Path'] = df_WBS['WBS Path'].str.strip()
    df_WBS['WBS Path'] = df_WBS['WBS Path'].astype(str)
    df.merge(df_WBS, on='WBS Path', how='left')

    df_BL_dates = pd.concat(
        [df_BL['Activity ID'].str.strip(),
         df_BL['Start'].str.strip(),
         df_BL['Finish'].str.strip()],
        axis=1)
    df_BL_dates.columns = ['Activity ID', 'BL1 Start', 'BL1 Finish']

    df = df.merge(df_BL_dates, on='Activity ID', how='left')

    # Add Links to main tables from gantt table
    df_links = pd.concat(
        [df_Gantt['Activity ID'].str.strip(),
         df_Gantt['Predecessor Details'].str.strip(),
         df_Gantt['Successor Details'].str.strip(),
         df_Gantt['HE Req: Special Coding'].str.strip()],
        axis=1)
    df = df.merge(df_links, on='Activity ID', how='left')

    # Relocate pred and success columns
    # index_no = df.columns.get_loc("Finish")
    # Pred_col = df.pop('Predecessor Details')
    # Succ_col = df.pop('Successor Details')
    # df.insert(index_no + 1, 'Predecessor Details', Pred_col)
    # df.insert(index_no + 2, 'Successor Details', Succ_col)





    spec_chars_date = ["a", 'A', "AM", "*", "PM", "d", "h","%"]
    for char in spec_chars_date:
        # df['Start'] = df['Start'].astype(str)
        df['Start'] = df['Start'].str.replace(char, '')
        # df['Finish'] = df['Finish'].astype(str)
        df['Finish'] = df['Finish'].str.replace(char, '')
        # df['BL1 Start'] = df['BL1 Start'].astype(str)
        df['BL1 Start'] = df['BL1 Start'].str.replace(char, '')
        df['BL1 Finish'] = df['BL1 Finish'].str.replace(char, '')
        # df['BL1 Finish'] = df['BL1 Finish'].astype(str)
        df['Planned Units'] = df['Planned Units'].str.replace(char, '')
        df['Remaining Units'] = df['Remaining Units'].str.replace(char, '')
        df['At Completion Units'] = df['At Completion Units'].str.replace(char, '')
        df['Planned Duration'] = df['Planned Duration'].str.replace(char, '')
        df['Remaining Duration'] = df['Remaining Duration'].str.replace(char, '')
        df['At Completion Duration'] = df['At Completion Duration'].str.replace(char, '')
        df['Remaining Units'] = df['Remaining Units'].str.replace(char, '')
        df['Remaining Labor Units'] = df['Remaining Labor Units'].str.replace(char, '')
        df['Planned Labor Units'] = df['Planned Labor Units'].str.replace(char, '')
        df['Actual Duration'] = df['Actual Duration'].str.replace(char, '')
        df['Activity % Complete'] = df['Activity % Complete'].str.replace(char, '')
        # df['Planned Nonlabor Units'] = df['Planned Nonlabor Units'].str.replace(char, '')

    # df['Start']= pd.to_datetime(df['Start'])
    # df['Finish']= pd.to_datetime(df['Finish'])
    df['Planned Units'] = pd.to_numeric(df['Planned Units'])
    df['Remaining Units'] = pd.to_numeric(df['Remaining Units'])
    df['Remaining Labor Units'] = pd.to_numeric(df['Remaining Labor Units'])
    df['At Completion Units'] = pd.to_numeric(df['At Completion Units'])
    df['Planned Duration'] = pd.to_numeric(df['Planned Duration'])
    df['Remaining Duration'] = pd.to_numeric(df['Remaining Duration'])
    df['At Completion Duration'] = pd.to_numeric(df['At Completion Duration'])
    df['Planned Labor Units'] = pd.to_numeric(df['Planned Labor Units'])
    df['Actual Duration'] = pd.to_numeric(df['Actual Duration'])
    df['Activity % Complete'] = pd.to_numeric(df['Activity % Complete'])
    # df['Planned Nonlabor Units'] = df['Planned Nonlabor Units'].str.replace(char, '')

    # df.filter(like='FY', axis=1).replace('h','',regex=True,inplace=True)

    df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

          # df_WBS
    # df.insert(0, 'L2', '')
    # df.insert(1, 'L3', '')
    # df.insert(2, 'L4', '')
    # df.insert(3, 'L5', '')


    df_L2_Name = df_WBS[df_WBS['WBS Path'].str.match('^1\.\d{2}$') == True]
    df_L2_Name.columns = ["L2", "L2_Name"]
    # df['L2_Name']=df.L2.map(df_L2_Name.L2_Name)
    df = df.merge(df_L2_Name, on='L2', how='left')
    df['L2_Name'] = df['L2'].astype(str) + '_' + df['L2_Name']
    del df_L2_Name

    df_L3_Name = df_WBS[df_WBS['WBS Path'].str.match('^1\.\d{2}.\d{2}$') == True]
    df_L3_Name.columns = ["L3", "L3_Name"]
    # df['L3_Name']=df.L3.map(df_L3_Name.L3_Name)
    df = df.merge(df_L3_Name, on='L3', how='left')
    df['L3_Name'] = df['L3'].astype(str) + '_' + df['L3_Name']
    del df_L3_Name

    df_L4_Name = df_WBS[df_WBS['WBS Path'].str.match('^1\.\d{2}.\d{2}.\d{2}$') == True]
    df_L4_Name.columns = ["L4", "L4_Name"]
    # df['L4_Name']=df.L4.map(df_L4_Name.L4_Name)
    df = df.merge(df_L4_Name, on='L4', how='left')
    df['L4_Name'] = df['L4'].astype(str) + '_' + df['L4_Name']
    del df_L4_Name

    df_L5_Name = df_WBS[df_WBS['WBS Path'].str.match('^1\.\d{2}.\d{2}.\d{2}.\d{2}$') == True]
    df_L5_Name.columns = ["L5", "L5_Name"]
    # df['L5_Name']=df.L5.map(df_L5_Name.L5_Name)
    df = df.merge(df_L5_Name, on='L5', how='left')
    df['L5_Name'] = df['L5'].astype(str) + '_' + df['L5_Name']
    del df_L5_Name
    df['ID_and_Name'] = df['Activity ID'].astype(str) + '_' + df['Activity Name'].astype(str)

    # Generate a list of all resources used
    # Get unique Resources ID :
    # unique_ressource = df['Resource Name'].unique()
    # df_unique_ressource = pd.DataFrame(unique_ressource, columns = [0])
    # df_unique_ressource.to_csv('/content/drive/MyDrive/Colab Notebooks/unique_ressource.csv', encoding='utf-8', index=False)

    # unique_ressource = pd.dataframe
    # np.savetxt('unique_ressource.csv',unique_ressource, delimiter=',')
    # unique_ressource.to_csv('unique_ressource.csv')
    # unique_ressource.to_csv('unique_ressource.csv', encoding='utf-8', index=False)

    # Read the category of resources
    df = df.merge(df_res_cat, on='Resource Name', how='left')

    # Concatenate all the dataframe into one
    # df = pd.concat([df, df_FM,df_FM_FTE,df_FQ,df_FQ_FTE,df_FY,df_FY_FTE], axis=1)


    # df.drop('WBS Path', axis=1, inplace=True)


    # st.write(df[500:510])


    # df_date = pd.to_numeric(df_date, downcast='float')
    # df = pd.concat([df, df_date], axis=1)

    # df = df[(df['L2']=='1.03') & (df['Type']=='Labor')& (df['Trade'] !='M&S')]

    df_FM = df.loc[:, df.columns.str.startswith('FY')].replace('h', '', regex=True)
    df.drop(list(df.filter(regex='^FY')), axis=1, inplace=True)
    df = df.fillna(0)
    # df = df.apply(pd.to_numeric, errors='ignore')

    # Convert Columns to date
    df_FM.columns = df_FM.columns.str.replace(", FM", "-")
    df_FM.columns = df_FM.columns.str.replace("FY", "")
    df_FM = df_FM.add_suffix('-01')
    # df_FM.columns = pd.to_datetime(df_FM.columns, utc=False) #).dt.date
    # df_FM.columns = pd.to_datetime(df_FM.columns, format = "%m/%d/%Y %I:%M:%S %p")
    df_FM.columns = pd.to_datetime(df_FM.columns, format="%Y-%m-%d",utc=False)

    # CONVERSION TO REAL DATE
    df_FM.columns = df_FM.columns + pd.DateOffset(months=-3)
    df_FM = df_FM.fillna(0)
    df_FM = df_FM.astype(float)
    # df_FM = pd.to_numeric(df_FM, errors='coerce')
    # df_FM = df_FM.apply(pd.to_numeric, downcast='float', errors='coerce')

    df = pd.concat([df, df_FM], axis=1)
    # df = df.loc[:, ~df.columns.duplicated()]

# WRITE INTO GOOGLESHEET
    gc = gspread.service_account(filename='cloud_google.json')
    sh = gc.open_by_key('19VyS_zz1iy8iK2pTSAumquQp6TWMrxxuYt_61t2IBDk')
    worksheet = sh.get_worksheet(0)  # -> 0 - first sheet, 1 - second sheet etc.
    worksheet.clear()
    set_with_dataframe(worksheet, df)  # -> THIS EXPORTS YOUR DATAFRAME TO THE GOOGLE SHEET
    return df

def set_date(df,duration, h_o_FTE):
    # df = df.dropna()

    df_Period_2 = pd.DataFrame
    df_Period = df.loc[:, df.columns.str.startswith('20')]

    # df_Period = df.filter(regex='^20')
    df_date = df.drop(df.loc[:, df.columns[df.columns.str.startswith('20')]], axis=1)


    # df_date = df
    # df_date.drop(list(df_date.filter(regex='^20')), axis=1) , inplace=True)

    if h_o_FTE == 'hours' and duration == 'month' :
        df_Period_2 = df_Period

    elif h_o_FTE == 'FTE' and duration == 'month':
        df_Period_2 = df_Period / (145)

    elif h_o_FTE == 'FTE' and duration == 'quarter':
        df_Period_2 = df_Period.groupby(pd.PeriodIndex(df_Period.columns, freq='Q-SEP'), axis=1).sum()
        df_Period_2 = df_Period_2 / (145*3)

    elif h_o_FTE == 'hours' and duration == 'quarter':
        df_Period_2 = df_Period.groupby(pd.PeriodIndex(df_Period.columns, freq='Q-SEP'), axis=1).sum()

    elif h_o_FTE == 'hours' and duration == 'year':
        df_Period_2 = df_Period.groupby(pd.PeriodIndex(df_Period.columns, freq='A-SEP'), axis=1).sum()

    elif h_o_FTE == 'FTE' and duration == 'year':
        df_Period_2 = df_Period.groupby(pd.PeriodIndex(df_Period.columns, freq='A-SEP'), axis=1).sum()
        df_Period_2 = df_Period_2 / (1740)

    else:
        df_Period_2 = df_Period

    # # df = pd.concat([df,df_FY_FTE, df_FQ, df_FQ_FTE, df_FY, df_FM_FTE, df_FM], axis=1)
    df_date_2 =  pd.concat([df_date,df_Period_2], axis=1)
    return  df_date_2