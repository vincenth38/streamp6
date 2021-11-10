import os
import streamlit as st
import numpy as np
# from PIL import  Image

# Custom imports 
from multipage import MultiPage
from pages import data_upload, ressources_analyze, file_explorer, table #pivot  import your pages here

# Create an instance of the app 
app = MultiPage()

st.set_page_config(page_title="My App",layout='wide')

# title_alignment="""<style>#the-title {  text-align: center}</style>"""
# st.title("The title")
# Title of the main page
# display = Image.open('Logo.png')
# display = np.array(display)
# st.image(display, width = 400)
# st.title("Data Storyteller Application")

col1, col2 = st.columns(2)
# col1.image(display, width = 400)
# col2.title("Data Storyteller Application")

# Add all your application here
app.add_page("Upload Data", data_upload.app)
app.add_page("Files", file_explorer.app)
app.add_page("ressources analyze", ressources_analyze.app)
app.add_page("table", table.app)
# app.add_page("pivot", pivot.app)

# The main app
app.run()
