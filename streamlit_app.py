import pandas as pd
import streamlit as st
from gsheetsdb import connect
# import import_data
from import_data import import_data
import base64

@st.cache
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

if st.button('update data'):
    df = import_data()
    st.text("df")
    # st.write(df)


try:
    csv = convert_df(df)
    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name='df.csv',
        mime='text/csv',
    )
except AttributeError:
    pass
# catch when it hasn't even been defined
except NameError:
    pass

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
