import pandas as pd
import streamlit as st

st.title("Convert P6")
#Insert a file uploader that accepts multiple files at a time:
uploaded_files = st.file_uploader("Choose a CSV file", accept_multiple_files=True)
# for uploaded_file in uploaded_files:
#   bytes_data = uploaded_file.read()
#   st.write("filename:", uploaded_file.name)
#   st.write(bytes_data)


if uploaded_files is not None:
  df = pd.read_csv(uploaded_files)
  st.write(df)