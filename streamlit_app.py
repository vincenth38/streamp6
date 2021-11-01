import pandas as pd
import streamlit as st
from gsheetsdb import connect


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
sheet_url = st.secrets["public_gsheets_url"]

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

sheet_id = '1D2_X4p0qnX1C6cmizv4gJtGiaTY3RPNUW9qJyJaGsCU'
sheet_name = 'ressources'
url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}'
df = pd.read_csv(url, error_bad_lines=False)

df_baseline = pd.read_csv(f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet=baseline', error_bad_lines=False)
df_gantt = pd.read_csv(f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet=gantt', error_bad_lines=False)
df_wbs = pd.read_csv(f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet=wbs', error_bad_lines=False)
df_cat_ressources = pd.read_csv(f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet=cat_ressources', error_bad_lines=False)

st.write(df_gantt.head())