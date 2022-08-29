# -*- coding: utf-8 -*-
"""
Created on Wed Aug 24 15:17:25 2022

@author: lechu
"""



# streamlit_app.py

import streamlit as st
from gsheetsdb import connect
import plotly.express as px
import pandas as pd

# Create a connection object.
conn = connect()

# Perform SQL query on the Google Sheet.
# Uses st.cache to only rerun when the query changes or after 10 min.
@st.cache(ttl=6000)
def run_query(query):
    rows = conn.execute(query, headers=1)
    rows = rows.fetchall()
    return rows

sheet_url = st.secrets["public_gsheets_url"]


st.title(sheet_url)
rows = run_query(f'SELECT * FROM "{sheet_url}"')


data = []

for row in rows:
    #st.write(f"{row.Contratista} has a :{row.Volumen}:")
    datas = (row.Contratista,row.Rodal,row.Fecha, row.Volumen)
    
    data.append(datas)

print(data)
    
st.dataframe(data)
  

#fig = px.bar(data,x = 2,y = 1, color = 0 , orientation = "h")
#st.write(fig)


fig = px.timeline(data, x_start=2, x_end=2, y=1)
fig.update_yaxes(autorange="reversed") # otherwise tasks are listed from the bottom up

st.write(fig)

