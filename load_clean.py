import pandas as pd
import gspread
from gspread_dataframe import set_with_dataframe
# from gsheetsdb import connect
# import gspread
api_key = 'AIzaSyDfZcKxsxvrUuss4EW4lBhTrSX3GmVjyu8'

# @st.cache
def import_clean():
    sheet_id = '19VyS_zz1iy8iK2pTSAumquQp6TWMrxxuYt_61t2IBDk'
    sheet_name = 'clean'
    url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}'
    df = pd.read_csv(url, error_bad_lines=False)
    return df