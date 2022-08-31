# -*- coding: utf-8 -*-
"""
Created on Wed Aug 24 15:17:25 2022

@author: lechu
"""



# streamlit_app.py

import streamlit as st
from gsheetsdb import connect

# Create a connection object.
conn = connect()

# Perform SQL query on the Google Sheet.
# Uses st.cache to only rerun when the query changes or after 10 min.
@st.cache(ttl=600)
def run_query(query):
    rows = conn.execute(query, headers=1)
    rows = rows.fetchall()
    return rows

sheet_url = st.secrets["public_gsheets_url"]


st.title(sheet_url)
rows = run_query(f'SELECT * FROM "{sheet_url}"')

# Print results.
for row in rows:
    print(row[3])
    #st.write(row.S1)
    
    #st.write(f"{row.S1} has a :{row.Contratista}:")
    
    

