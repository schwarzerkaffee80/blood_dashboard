import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


st.set_page_config(
    page_title="Sophie's Blutwerte",
    page_icon="🧡",
    layout="wide",
)

@st.cache_data
def get_time_series(filename) -> pd.DataFrame:
    return pd.read_excel(filename)

units = {'CRP':'mg/dl', 'Interleukin 6':'pg/ml', 'Eiweiss':'g/dl', 'Leukocyten':'G/l', 
         'Erythrocyten':'T/l', 'Hämoglobin':'g/dl', 'Hämatokrit':'l/l', 'Thrombocyten':'G/l'}

#define side bar
with st.sidebar:
    st.header("Sophie's Blutwerte")
    st.text("")

    uploaded_file = st.file_uploader("Wähle Blutdatei", type='xlsx', accept_multiple_files=False)

    if uploaded_file is None:
        uploaded_file = "Blutbilder.xlsx"

    if uploaded_file is not None: 
        
        df = get_time_series(uploaded_file)
        columns = df.columns

        tstp_name = "Datum"
        df[tstp_name] = pd.to_datetime(df[tstp_name])

        valid_colnames = columns.delete(0)
        val_name = st.selectbox("Wähle ersten Blutwert", valid_colnames)

        second_ax = st.checkbox("Zweite Achse", False)
        if second_ax:
            valid_colnames_2 = valid_colnames.drop(val_name)
            val_name2 = st.selectbox("Wähle zweiten Blutwert", valid_colnames_2)





#define main window
subfig = make_subplots()
fig = px.line(data_frame=df, y=val_name, x=tstp_name)
subfig.add_traces(fig.data)

if second_ax:          
    subfig = make_subplots(specs=[[{"secondary_y": True}]])

    # create two independent figures with px.line each containing data from multiple columns
    fig2 = px.line(data_frame=df, y=val_name2, x=tstp_name)
    fig2.update_traces(line_color = "#4C0013", yaxis="y2")

    subfig.add_traces(fig.data + fig2.data)

st.write(subfig)
