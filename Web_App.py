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
    return pd.read_csv(filename, sep = ";")

units = get_time_series("Wertetabelle.csv")
units.set_index("Name", inplace = True, drop = True)

#define side bar
with st.sidebar:
    st.header("Sophie's Blutwerte")
    st.text("")

    uploaded_file = st.file_uploader("Wähle Blutdatei", type='csv', accept_multiple_files=False)

    if uploaded_file is None:
        uploaded_file = "Blutbilder.csv"

    if uploaded_file is not None: 
        
        df = get_time_series(uploaded_file)
        columns = df.columns

        tstp_name = "Datum"
        df[tstp_name] = pd.to_datetime(df[tstp_name], format = "%d.%m.%Y")

        valid_colnames = columns.delete(0)
        val_name = st.selectbox("Wähle ersten Blutwert", valid_colnames)
        meta = units.loc[val_name]

        second_ax = st.checkbox("Zweite Achse", False)
        if second_ax:
            valid_colnames_2 = valid_colnames.drop(val_name)
            val_name2 = st.selectbox("Wähle zweiten Blutwert", valid_colnames_2)
            meta2 = units.loc[val_name2]
            thresh = False
        
        chemo = st.checkbox("Zeige Chemo Fenster")

        if not second_ax:
            thresh = st.checkbox("Zeige Normalbereich")
        


#define main window
subfig = make_subplots()
#subfig.add_trace(go.Scatter(x=df.index, y=df[val_name]), row=1, col=1)
fig = px.line(data_frame=df, y=val_name, x=tstp_name, labels=val_name)
fig['data'][0]['showlegend']=True
fig['data'][0]['name']=val_name
subfig.add_traces(fig.data)
if thresh:
    subfig.add_hrect(y0 = meta.untereGrenze,y1 = meta.obereGrenze, 
                     line_width=0, fillcolor="red", opacity=0.2, annotation_text="Normbereich")

subfig.update_layout(
  title= "Sophie's Reise",
  xaxis_title="Datum",
  yaxis_title= val_name + ' ' + meta.Einheit,
)

if second_ax:          
    subfig = make_subplots(specs=[[{"secondary_y": True}]])

    fig2 = px.line(data_frame=df, y=val_name2, x=tstp_name)
    fig2['data'][0]['showlegend']=True
    fig2['data'][0]['name']=val_name2
    fig2.update_traces(line_color = "#4C0013", yaxis="y2")

    subfig.add_traces(fig.data + fig2.data)
    subfig.update_yaxes(title_text = val_name + ' ' + meta.Einheit, secondary_y=False)
    subfig.update_yaxes(title_text = val_name2 + ' ' + meta2.Einheit, secondary_y=True)

    subfig.update_layout(
    title= "Sophie's Reise",
    xaxis_title="Datum")

if chemo:
    subfig.add_vrect(x0=pd.to_datetime("2023-04-20"), x1=pd.to_datetime("2023-04-27"), line_width=0, fillcolor="red", opacity=0.2)
st.plotly_chart(subfig, theme=None,  use_container_width=True)
