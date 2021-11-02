import matplotlib
import plotly.express as px
# import plotly.graph_objects as go
import streamlit as st
from gsheetsdb import connect
# import import_data
from import_data import import_data,import_clean
import pandas as pd
import time


# IMPORTANT: Cache the conversion to prevent computation on every rerun
def convert_df(df):
    return df.to_csv().encode('utf-8')


# st.title("Convert P6")
# st.title("Connect to Google Sheets")
#Insert a file uploader that accepts multiple files at a time:
# uploaded_files = st.file_uploader("Choose a CSV file", accept_multiple_files=True)
# for uploaded_file in uploaded_files:
#   bytes_data = uploaded_file.read()
#   st.write("filename:", uploaded_file.name)
#   st.write(bytes_data)


# if uploaded_files is not None:
#   df = pd.read_csv(uploaded_files)
#   st.write(df)



# Create a connection object.
conn = connect()
# sheet_url = st.secrets["public_gsheets_url"]

# Perform SQL query on the Google Sheet.
# Uses st.cache to only rerun when the query changes or after 10 min.
# @st.cache(ttl=600)
# def run_query(query):
#     rows = conn.execute(query, headers=1)
#     return rows


# rows = run_query(f'SELECT * FROM "{sheet_url}"')

# Print results.
# for row in rows:
#     st.write(f"{row.name} has a :{row.pet}:")
    # st.write(row)
#


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
st.sidebar.write("P6 raw data  [link](https://docs.google.com/spreadsheets/d/1D2_X4p0qnX1C6cmizv4gJtGiaTY3RPNUW9qJyJaGsCU/edit#gid=921908947)")
st.sidebar.write("Clean  [link](https://docs.google.com/spreadsheets/d/19VyS_zz1iy8iK2pTSAumquQp6TWMrxxuYt_61t2IBDk/edit#gid=505509094)")
if st.sidebar.button('Rebuild Clean data'):
    import_data()
    # st.text("df")
    # st.write(df)

# try:
#     csv = convert_df(df)
#     st.download_button(
#         label="Download data as CSV",
#         data=csv,
#         file_name='df.csv',
#         mime='text/csv',
#     )
# except AttributeError:
#     pass
# # catch when it hasn't even been defined
# except NameError:
#     pass

# if st.button('save dataframe'):
#     open('df.csv', 'w').write(df.to_csv())
#
# # st.write(df)
# def get_table_download_link(df):
#     """Generates a link allowing the data in a given panda dataframe to be downloaded
#     in:  dataframe
#     out: href string
#     """
#     csv = df.to_csv(index=False)
#     b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
#     href = f'<a href="data:file/csv;base64,{b64}">Download csv file</a>'
# st.markdown(get_table_download_link(df), unsafe_allow_html=True)


@st.cache
def load_data():
    # Create a text element and let the reader know the data is loading.
    df = import_clean()
    # Notify the reader that the data was successfully loaded.
    return df




df_load_state = st.sidebar.text('Loading data...')
df = load_data()
df_load_state.text("Done! (using st.cache)")


# wbs_selection = st.sidebar.selectbox(
#     'Select wbs',
#     df['L3'].unique().tolist())

# if wbs_selection:
#     temp = df[(df['L3'] == wbs_selection ) & (df['Type'] == 'Labor') & (df['Trade'] != 'M&S')].groupby('Trade').sum().filter(regex=('^2022Q\d{1}$'))
#     temp = temp.loc[(temp != 0).any(axis=1)]
#     st.write(temp)

h_o_FTE = st.sidebar.selectbox(
    'Select Hours or FTE',
    ('hours','FTE'))

if h_o_FTE == 'FTE':
    suff = 'FTE'
else:
    suff =''
wbs_multi_selection = st.sidebar.multiselect(
    'Select wbs',
    df['L3'].unique().tolist())
if wbs_multi_selection:
    temp = df[(df['L3'].isin(wbs_multi_selection)) & (df['Type'] == 'Labor') & (df['Trade'] != 'M&S')].groupby('Trade').sum().filter(regex=('^2022Q\d{1}'+ suff + '$'))
    temp = temp.loc[(temp != 0).any(axis=1)]
    st.write(temp)
    # st.write(df[(df['L3'].isin(wbs_multi_selection)) & (df['Type'] == 'Labor') & (df['Trade'] != 'M&S')].groupby('Trade').sum().filter(regex=('^2022Q\d{1}$')))
    # st.write(temp.columns)
    # st.write(str(temp))
    # print(str(temp))
    print(temp)
    print(temp.index.tolist())
    print(temp.values.tolist())
    fig = px.bar(temp.transpose())
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
