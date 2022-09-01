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
from datetime import datetime

# Create a connection object.
conn = connect()

st.header("Andres A Leszczuk")

# Perform SQL query on the Google Sheet.
# Uses st.cache to only rerun when the query changes or after 10 min.
@st.cache(ttl=60)
def run_query(query):
    rows = conn.execute(query, headers=1)
    rows = rows.fetchall()
    return rows

sheet_url = st.secrets["public_gsheets_url"]

# ---- Header ----
st.title(":bar_chart: Dashboard de produccion")
st.markdown("##")
st.markdown('***Link de base de datos:***')
st.write(sheet_url)
rows = run_query(f'SELECT * FROM "{sheet_url}"')

# ---- Data frame ----
data = []
for row in rows:
    #st.write(f"{row.Contratista} has a :{row.Volumen}:")
    datas = (str(row.Contratista),
             str(row.Rodal),
             row.Fecha_Inicio,
             row.Fecha_Final,
             float(row.Volumen),
             float(row.Costo),
             str(row.Estado))
    data.append(datas)
#print(data)
#st.dataframe(data)

# Convert list in data frame
# link of plot https://towardsdatascience.com/gantt-charts-with-pythons-matplotlib-395b7af72d72
df = pd.DataFrame(data,columns = ['Contratista', 'Rodal', 'fecha_i', 'fecha_f','Vol','Cost', 'Estado'])
  

#fig = px.bar(data,x = 3,y = 2, color = 0 , orientation = "h")
#st.write(fig)
# ---- Side Bar ----
st.sidebar.header("Filtros:")
contratista = st.sidebar.multiselect(
    "Seleccione contratista:",
    options=df["Contratista"].unique(),
    default=df["Contratista"].unique()
)
rodal = st.sidebar.multiselect(
    "Seleccione contratista:",
    options=df["Rodal"].unique(),
    default=df["Rodal"].unique()
)

df_selection = df.query(
    "Contratista == @contratista & Rodal == @rodal"
)
# ----- DAY VARIABLES ----
# Prooject_start date
projStar = df.fecha_i.min()
# number of days from project start to task start
df_selection['start_num'] = (df_selection.fecha_i-projStar).dt.days
# number of days from project start to end of tasks
df_selection['end_num'] = (df_selection.fecha_f-projStar).dt.days
# days between start and end of each task
df_selection['days_start_to_end'] = df_selection.end_num - df_selection.start_num



# ---- MAINPAGE ----

volTotal = int(df_selection["Vol"].sum())
volMean = round(int(df_selection["Vol"].mean())/int(df_selection["days_start_to_end"].sum()),1)
#volCont = df_selection.groupby(by=["Contratista"]).sum()[["Vol"]][1]


left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Volumen total :")
    st.subheader(f"{volTotal:,} m³")

with middle_column:
    st.subheader("Volumen promedio :")
    st.subheader(f"{volMean:,} m³/día")

#with right_column:
#    st.write(f"{volCont:,}")
# ---- Gantt Plot ----



#st.write(df)

fig = px.timeline(df_selection, x_start="fecha_i", x_end="fecha_f", y="Rodal", color = "Estado",
                  facet_row = "Contratista")
fig.update_yaxes(autorange="reversed") # otherwise tasks are listed from the bottom up
st.write(fig)
