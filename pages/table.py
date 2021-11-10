from st_aggrid import AgGrid
import pandas as pd

import streamlit as st
import pandas as pd
def import_clean2():
    df = pd.read_csv('data/df_clean.csv')
    df.drop(list(df.filter(regex='^20')), axis=1, inplace=True)
    df = df.loc[:, ~df.columns.duplicated()]
    return df

# @st.cache
def app():
    AgGrid(import_clean2())
    # st.table(import_clean())
