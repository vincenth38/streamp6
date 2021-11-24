import streamlit as st
import numpy as np
import pandas as pd
import sqlite3
from pages import utils


@st.cache
def import_clean():
    sheet_id = '19VyS_zz1iy8iK2pTSAumquQp6TWMrxxuYt_61t2IBDk'
    sheet_name = 'clean'
    # url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}'
    url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&sheet={sheet_name}'
    # df = pd.DataFrame
    df = pd.read_csv(url)
    # df = df.apply(pd.to_numeric, errors='coerce')
    df['Planned Units'] = pd.to_numeric(df['Planned Units'])
    df['Remaining Units'] = pd.to_numeric(df['Remaining Units'])
    df['At Completion Units'] = pd.to_numeric(df['At Completion Units'])
    df['Planned Duration'] = pd.to_numeric(df['Planned Duration'])
    df['Remaining Duration'] = pd.to_numeric(df['Remaining Duration'])
    df['At Completion Duration'] = pd.to_numeric(df['At Completion Duration'])
    df['Planned Labor Units'] = pd.to_numeric(df['Planned Labor Units'])
    df['Activity % Complete'] = pd.to_numeric(df['Activity % Complete'])
    df = df.loc[:, ~df.columns.duplicated()]
    df.to_csv('data/df_clean.csv')
    return df

def app():
    df_load_state = st.sidebar.text('Loading data...')
    df = import_clean()
    df_load_state.text("Done! (using st.cache)")
    st.markdown("## Data Upload")

    # Upload the dataset and save as csv
    st.markdown("### Upload a csv file for analysis. (Not used yet ...)")
    st.write("\n")

    # Code to read a single file 
    uploaded_file = st.file_uploader("Choose a file", type = ['csv', 'xlsx'])
    global data
    if uploaded_file is not None:
        try:
            # chunksize = 10
            conn = sqlite3.connect('data\info.db')
            wb = pd.read_excel(uploaded_file, sheet_name=None)  #, chunksize=chunksize)
            for sheet in wb:
                wb[sheet].to_sql(name=sheet, con=conn, if_exists='append')
            con.commit()
            con.close()






        except Exception as e:
            print(e)
            # wb = pd.read_excel(uploaded_file, sheet_name=None)


        # dfs = pd.read_excel('somefile.xlsx', sheet_name=None)
        # wb = pd.read_excel('CPS\CPS.xlsx', sheet_name=None)




    
    # uploaded_files = st.file_uploader("Upload your CSV file here.", type='csv', accept_multiple_files=False)
    # # Check if file exists 
    # if uploaded_files:
    #     for file in uploaded_files:
    #         file.seek(0)
    #     uploaded_data_read = [pd.read_csv(file) for file in uploaded_files]
    #     raw_data = pd.concat(uploaded_data_read)
    
    # uploaded_files = st.file_uploader("Upload CSV", type="csv", accept_multiple_files=False)
    # print(uploaded_files, type(uploaded_files))
    # if uploaded_files:
    #     for file in uploaded_files:
    #         file.seek(0)
    #     uploaded_data_read = [pd.read_csv(file) for file in uploaded_files]
    #     raw_data = pd.concat(uploaded_data_read)
    
    # read temp data 
    # data = pd.read_csv('data/2015.csv')


    ''' Load the data and save the columns with categories as a dataframe. 
    This section also allows changes in the numerical and categorical columns. '''
    if st.button("Load Data"):
        
        # Raw data 
        st.dataframe(data)
        #utils.getProfile(data)
        #st.markdown("<a href='output.html' download target='_blank' > Download profiling report </a>",unsafe_allow_html=True)
        #HtmlFile = open("data/output.html", 'r', encoding='utf-8')
        #source_code = HtmlFile.read() 
        #components.iframe("data/output.html")# Save the data to a new file 
        data.to_csv('data/main_data.csv', index=False)
        
        #Generate a pandas profiling report
        #if st.button("Generate an analysis report"):
        #    utils.getProfile(data)
            #Open HTML file

        # 	pass

        # Collect the categorical and numerical columns 
        
        numeric_cols = data.select_dtypes(include=np.number).columns.tolist()
        categorical_cols = list(set(list(data.columns)) - set(numeric_cols))
        
        # Save the columns as a dataframe or dictionary
        columns = []

        # Iterate through the numerical and categorical columns and save in columns 
        columns = utils.genMetaData(data) 
        
        # Save the columns as a dataframe with categories
        # Here column_name is the name of the field and the type is whether it's numerical or categorical
        columns_df = pd.DataFrame(columns, columns = ['column_name', 'type'])
        columns_df.to_csv('data/metadata/column_type_desc.csv', index = False)

        # Display columns 
        st.markdown("**Column Name**-**Type**")
        for i in range(columns_df.shape[0]):
            st.write(f"{i+1}. **{columns_df.iloc[i]['column_name']}** - {columns_df.iloc[i]['type']}")
        
        st.markdown("""The above are the automated column types detected by the application in the data. 
        In case you wish to change the column types, head over to the **Column Change** section. """)