import streamlit as st
import os

# @st.cache
def app():
    filelist = []
    for root, dirs, files in os.walk("data"):
        for file in files:
            filename = os.path.join(root, file)
            filelist.append(filename)
    st.write(filelist)
