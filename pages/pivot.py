import streamlit as st
import streamlit.components.v1 as components
from pivottablejs import pivot_ui
import pandas as pd
def import_clean2():
    df = pd.read_csv('data/df_clean.csv')
    df.drop(list(df.filter(regex='^20')), axis=1, inplace=True)
    df = df.loc[:, ~df.columns.duplicated()]
    return df

# @st.cache
def app():


    iris = import_clean2()

    t = pivot_ui(iris)

    with open(t.src) as t:
        components.html(t.read(), width=900, height=1000, scrolling=True)
