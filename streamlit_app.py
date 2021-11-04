import json
from pandas.api.types import is_datetime64_any_dtype as is_datetime
import matplotlib
import plotly.express as px
# import plotly.graph_objects as go
import streamlit as st
# from streamlit import caching
from gsheetsdb import connect
import import_data
import import_data
from import_data import import_data,import_clean
from import_data import change_period
import re
import pandas as pd
import time
st.set_page_config(layout="wide")

# IMPORTANT: Cache the conversion to prevent computation on every rerun
def convert_df(df):
    return df.to_csv().encode('utf-8')


@st.cache
def load_data():
    # Create a text element and let the reader know the data is loading.
    # if df:
    #     del df
    df = import_clean()
    return df


def full_load():
    # Create a text element and let the reader know the data is loading.
    # if df:
    #     del df
    df = import_data()
    # return df


# Create a connection object.
conn = connect()

# d/1D2_X4p0qnX1C6cmizv4gJtGiaTY3RPNUW9qJyJaGsCU/

#https://towardsdatascience.com/deploy-a-public-streamlit-web-app-for-free-heres-how-bf56d46b2abe
#
# sheet_url = "https://docs.google.com/spreadsheets/d/1ixMrhGV1TPn14_oTyEIFjszuwuwO9xkbsc1WEBJH3N0/edit?usp=sharing"
# # conn = connect()
# rows = conn.execute(f'SELECT * FROM "{sheet_url}"')
# df_sheet = pd.DataFrame(rows)
# st.write(df_sheet)

# conn = connect()
# st.title(sheet_url)
# rows = conn.execute(f'SELECT * FROM "{sheet_url}"')
# df_sheet = pd.DataFrame(rows)
# st.write(df_sheet)

# USING ONEDRIVE
# https://towardsdatascience.com/onedrive-as-data-storage-for-python-project-2ff8d2d3a0aa
# import base64
# def create_onedrive_directdownload (onedrive_link):
#     data_bytes64 = base64.b64encode(bytes(onedrive_link, 'utf-8'))
#     data_bytes64_String = data_bytes64.decode('utf-8').replace('/','_').replace('+','-').rstrip("=")
#     resultUrl = f"https://api.onedrive.com/v1.0/shares/u!{data_bytes64_String}/root/content"
#     return resultUrl
# if st.sidebar.text("Clear history cache"):
#     caching.clear_cache()

st.sidebar.write("P6 raw data  [link](https://docs.google.com/spreadsheets/d/1D2_X4p0qnX1C6cmizv4gJtGiaTY3RPNUW9qJyJaGsCU/edit#gid=921908947)")
st.sidebar.write("Clean  [link](https://docs.google.com/spreadsheets/d/19VyS_zz1iy8iK2pTSAumquQp6TWMrxxuYt_61t2IBDk/edit#gid=505509094)")

if st.sidebar.button('Rebuild Clean data'):
    df = full_load()


df_load_state = st.sidebar.text('Loading data...')
df = load_data()
df_load_state.text("Done! (using st.cache)")


wbs_multi_selection = st.sidebar.multiselect(
    'Select wbs',
    df['L3'].unique().tolist(),
    default=["1.03.04"])

year_select = st.sidebar.multiselect(
    'Select years',
    ('2019','2020','2021','2022','2023','2024','2025','2026','2027','2028','2029','2030'),
    default=["2021","2022","2023"])
# h_o_FTE = 'FTE'

h_o_FTE = st.sidebar.selectbox(
    'Select Hours or FTE',
    ('hours','FTE'))

if h_o_FTE == 'FTE':
    suff = 'FTE'
else:
    suff =''

# duration = 'month'
duration = st.sidebar.selectbox(
    'Select Period',
    ('month','quarter','year'),
    )






if duration and h_o_FTE and wbs_multi_selection and year_select:
    # df= full_load()
    df_date = change_period(df, duration, h_o_FTE)
    column_selection = df_date.columns

    df_date  = df_date[(df_date['L3'].isin(wbs_multi_selection)) & (df_date['Type'] == 'Labor') & (df_date['Trade'] != 'M&S')]

    df_date =  df_date.groupby('Trade').sum() #+year_select)+

    a = '|'.join([str(x) for x in year_select])

    reg_exp = '\b(?<!@)('+a+')\b'


    df_date = df_date.filter(regex=('^'+a))


    # df_date = df_date.loc[(df_date != 0).any(axis=1)]

    # pattern = re.compile("|".join(year_select))
    # result = [i for i in df_date.columns.astype(str) if pattern.match(i)]
    # result.append('Trade')
    # st.write(result)
    #
    # # df_date = df_date[df_date.columns.intersection(set(result))]
    #
    df_date = df_date.loc[~(df_date == 0).all(axis=1)]
    st.dataframe(df_date)
    # st.write(df_date.columns)

    if duration == 'month':

        fig = px.bar(df_date.transpose())
        fig.update_layout(
            autosize = True,
            width=1400,
            height=600,
            margin=dict(l=10, r=10, t=20, b=20),
        )

        st.plotly_chart(fig)

    if duration == 'quarter' or duration == 'year':
        df_date_T= df_date.T
        df_date_T['date'] = df_date_T.index
        if duration == 'quarter':
            qs = df_date_T.index.astype(str).str.replace(r'(d+)(Qd)', r'2-1')
            df_date_T['date'] = pd.PeriodIndex(qs, freq='Q').to_timestamp()
        if duration == 'year':
            # qs = df_date_T.index.astype(str).str.replace(r'(d+)(Qd)', r'2-1')
            df_date_T['date'] = pd.PeriodIndex(df_date_T.index).to_timestamp()

        labels = print(list(df_date_T.index.astype(str)))
        print(df_date_T['date'])

        colonnes = list(df_date_T.iloc[:, 1:-1].columns)

        fig = px.bar(df_date_T,x=df_date_T.date,y=colonnes)
        fig.update_layout(
            autosize = True,
            width=800,
            height=500,
            margin=dict(l=20, r=20, t=20, b=20),

        )

        st.plotly_chart(fig)


# long_df = px.data.medals_long()
# fig = px.bar(temp, x=temp.index, y=temp.values, color=temp.index, title="Long-Form Input")
# fig.show()



#https://discuss.streamlit.io/t/pass-filtered-dataframe-through-three-dropdown-levels/5562

# def df_filtered(
#     df: pd.DataFrame,  # Source dataframe
#     f_date_range: [int, int],  # Current value of an ST date slider
#     f_manager: list = [],  # Current value of an ST multi-select
#     f_program: list = [],  # Current value of another ST multi-select
# ) -> pd.DataFrame:
#     dff = df.loc[f_date_range[0] : f_date_range[1]].reset_index(drop=True)
#     if len(f_manager) > 0:
#         dff = dff.loc[(dff["owner"].isin(f_manager))].reset_index(drop=True)
#     if len(f_program) > 0:
#         dff = dff.loc[(dff["program"].isin(f_program))].reset_index(drop=True)
#     return dff
#
# dff = df_filtered(df, f_date_range=ctl_date_slider, f_manager=ctl_manager_multi, f_program=ctl_program_multi)

#
# another way
# def select_1(source_df: pd.DataFrame) -> pd.DataFrame:
#     selected_mgr = st.multiselect(
#         "Select Manager Name for further exploration below",
#         source_df["manager"].unique(),
#     )
#     selected_1_df = source_df[(source_df["manager"].isin(selected_mgr))]
#     if selected_mgr:
#         st.write('You have selected', selected_mgr)
#     return selected_1_df





# *******Gantt Chart
# df_1 = pd.DataFrame([
#     dict(Disc="Civ", Start='2021-01-04', Finish='2021-08-10'),
#     dict(Disc="Mec", Start='2021-03-05', Finish='2021-09-15'),
#     dict(Disc="Pip", Start='2021-04-20', Finish='2021-11-30'),
#     dict(Disc="Ele", Start='2021-05-20', Finish='2021-12-05'),
#     dict(Disc="Ins", Start='2021-06-20', Finish='2021-12-20'),
#     dict(Disc="Com", Start='2021-07-20', Finish='2021-12-30')
# ])
# fig2 = px.timeline(df_1, x_start="Start", x_end="Finish", y='Disc')
# fig2.update_yaxes(autorange="reversed")
# fig2.update_layout(title={'text': "Main dates", 'x': 0.5}, plot_bgcolor="#eef9ea", paper_bgcolor="#eef9ea",
#                    font={'color': "#008080", 'family': "Georgia"}, height=340, width=550, margin=dict(
#         l=51, r=5, b=10, t=50))
# fig2.update_traces(marker_color='#17A2B8', selector=dict(type='bar'))
# st.plotly_chart(fig2)



# df_test  = df[(df['L3'].isin(wbs_multi_selection)) & (df['Type'] == 'Labor') & (df['Trade'] != 'M&S')]
# df_test2 = df_test[['Trade','Start','Finish']
# prd = pd.period_range(df_test2.loc[0, 'Start'], df.loc[0, 'Finish'], freq='D')
# prd = pd.Series(1, prd) # empty series to get the number of days in the monthly period
# prd = prd.resample('Q').size() * (df.loc[0, 'spend'] / prd.resample('Q').size().sum())
# prd = prd.to_frame()
# st.write(prd)

