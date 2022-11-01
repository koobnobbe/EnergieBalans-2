import streamlit as st
import pandas as pd
import numpy as np

import plotly.graph_objs as go
import plotly_express as px
from plotly.subplots import make_subplots

################
from lib import api_p1mon as p1
from lib import constants as const
#from lib import api_solaredge as slr
################

#-------------------------------------------------------------
# Application settings
#-------------------------------------------------------------
st.set_page_config( page_title="EnergieBalans - Yearly" )
#-------------------------------------------------------------

#-------------------------------------------------------------
# Data Collection
#-------------------------------------------------------------

#-------------------------------------------------------------
def show_graph_bar_diff(df, title, year, month):
    df = df[['year', 'month', 'day', 'cons']].copy()
    df_now = df.query('year==' + str(year)).query('month==' + str(month))
    df_lastyear = df.query('year==' + str(year - 1)).query('month==' + str(month))
    df_lastyear.rename(columns={'cons': 'lastyear'}, inplace=True)
    df_lastyear.drop(['year'], axis=1, inplace=True)
    df_diff = pd.merge(df_now, df_lastyear, on=['month', 'day'], how="outer")

    df_diff['diff'] = df_diff['cons'] - df_diff['lastyear']

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
       go.Bar(
          x=df_diff['day']
          , y=df_diff['diff']
          , name='Opbrengst ' + str(year)
          , marker={'color': df_diff['diff'], 'colorscale': 'RdYlGn'}
       )
       , secondary_y=False
    )
    title  = title + ' : '+str(year) +' - '+ str(month)+ ' with '+str(year-1) +' - '+ str(month)
    fig.update_layout( title_text='<b>'+title+'</b>') # Adding title text to the figure
    fig.update_xaxes(title_text="<b>dag van de Maand </b>") # Naming x-axis
    fig.update_yaxes(title_text="<b>Energie (kwh)</b>", secondary_y=False) # Naming y-axes
    st.write(fig)

# -------------------------------------------------------------
# screen presentation
# -------------------------------------------------------------
st.title('Energy Dashboard - Monthly')
with st.sidebar:
    selectedYear = st.slider("Year :", min_value=2020, max_value=2023, value=const.current_year, step=1)
    selectedMonth = st.slider("Month :", min_value=1, max_value=12, value=const.current_month, step=1)
#-------------------------------------------------------------

# -------------------------------------------------------------
# mainscreen presentation
# -------------------------------------------------------------
show_graph_bar_diff( p1.df_powergas_day[['year','month','day','cons']]
                    , 'Verschil stroomverbruik'
                    , selectedYear, selectedMonth)
