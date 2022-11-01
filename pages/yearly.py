import streamlit as st
import pandas as pd
import numpy as np

import plotly.graph_objs as go
import plotly_express as px
from plotly.subplots import make_subplots

from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode

################
from lib import api_p1mon as p1
from lib import constants as const
#from lib import api_solaredge as slr
################

#-------------------------------------------------------------
# Application settings
#-------------------------------------------------------------
st.set_page_config( page_title="EnergieBalans - Yearly" ,layout="wide")
#-------------------------------------------------------------

#-------------------------------------------------------------
# Data Collection
#-------------------------------------------------------------

#-------------------------------------------------------------
# Data Collection
#-------------------------------------------------------------
@st.cache(persist=True, show_spinner=True)
def load_p1_powergas_day(reporting_year, reporting_month):
   df = p1.df_powergas_day[['timestamp_local', 'cons', 'prd', 'afn', 'gas']]
   df['month'] = pd.DatetimeIndex(df['timestamp_local']).month
   df['year'] = pd.DatetimeIndex(df['timestamp_local']).year
   df['day'] = pd.DatetimeIndex(df['timestamp_local']).day

   df = df[['day','month','year', 'cons', 'prd', 'afn', 'gas']].copy()
   df= df.query('year==' + reporting_year).query('month==' + reporting_month)
   return df
#-------------------------------------------------------------
def show_table(df):
   gb = GridOptionsBuilder.from_dataframe(df)
   gb.configure_pagination(paginationAutoPageSize=True)  # Add pagination
   #gb.configure_side_bar()  # Add a sidebar
   #gb.configure_selection('multiple', use_checkbox=True,
   #                       groupSelectsChildren="Group checkbox select children")  # Enable multi-row selection
   gridOptions = gb.build()

   grid_response = AgGrid(
      df,
      gridOptions=gridOptions,
   #   data_return_mode='AS_INPUT',
   #   update_mode='MODEL_CHANGED',
      fit_columns_on_grid_load=True,
      theme='alpine',  # Add theme color to the table
      enable_enterprise_modules=False,
      #height='100%',
      #width='100%',
      reload_data=True,
   )
def show_table_day(df):
   gb = GridOptionsBuilder.from_dataframe(df)
   gb.configure_pagination(paginationAutoPageSize=True)  # Add pagination
   gb.configure_side_bar()  # Add a sidebar
   gb.configure_selection('multiple', use_checkbox=True,
                          groupSelectsChildren="Group checkbox select children")  # Enable multi-row selection
   gridOptions = gb.build()

   grid_response = AgGrid(
      df,
      gridOptions=gridOptions,
      data_return_mode='AS_INPUT',
      update_mode='MODEL_CHANGED',
      fit_columns_on_grid_load=True,
      theme='alpine',  # Add theme color to the table
      enable_enterprise_modules=False,
      #height='100%',
      #width='100%',
      reload_data=True,
   )

def show_graph_day(df):
   df = df[[ 'day', 'cons', 'prd', 'afn']]
   fig = px.histogram(df, x='day', y='cons')
   st.plotly_chart(fig)


def show_Graph_bar(df, title):
   df_now = df.query('year==' + str(selectedYear))
   df_now = df_now.groupby('month').sum().reset_index()

   df_lastyear = df.query('year==' + str(selectedYear- 1))
   df_lastyear = df_lastyear.groupby('month').sum().reset_index()

   df_year2 = df.query('year==' + str(selectedYear- 2))
   df_year2 = df_year2.groupby('month').sum().reset_index()

   df_year3 = df.query('year==' + str(selectedYear - 3))
   df_year3 = df_year3.groupby('month').sum().reset_index()

   fig = make_subplots(specs=[[{"secondary_y": True}]])
   fig.add_trace(
      go.Bar(
         x=df_now['month']
         , y=df_now['cons']
         , name=str(selectedYear)
      )
      , secondary_y=False
   )

   fig.add_trace(
      go.Bar(
         x=df_lastyear['month']
         , y=df_lastyear['cons']
         , name=str(selectedYear - 1)
      )
      , secondary_y=False
   )

   fig.add_trace(
      go.Bar(
         x=df_year2['month']
         , y=df_year2['cons']
         , name=str(selectedYear - 2)
      )
      , secondary_y=False
   )

   fig.add_trace(
      go.Bar(
         x=df_year3['month']
         , y=df_year3['cons']
         , name=str(selectedYear - 3)
      )
      , secondary_y=False
   )

   # Adding title text to the figure
   fig.update_layout(
      title_text='<b>'+title+'</b>'
   )

   # Naming x-axis
   fig.update_xaxes(title_text="<b>Maand</b>")

   # Naming y-axes
   fig.update_yaxes(title_text="<b>Energie (kwh)</b>", secondary_y=False)
   st.plotly_chart(fig)

def show_Graph_circle_year(df, title):
   df_now = df.groupby('year').sum().reset_index()
   df = df_now[['year','cons']]
   #df
   fig = px.pie(df, names='year', values='cons',title=title)
   st.plotly_chart(fig)

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

    fig.update_layout( title_text='Verschil opbrengst tov vorig jaar') # Adding title text to the figure
    fig.update_xaxes(title_text="<b>dag van de Maand </b>") # Naming x-axis
    fig.update_yaxes(title_text="<b>Energie (kwh)</b>", secondary_y=False) # Naming y-axes
    st.write(fig)
#-------------------------------------------------------------


# -------------------------------------------------------------
# screen presentation
# -------------------------------------------------------------
st.title('Energy Dashboard - Yearly')
with st.sidebar:
   selectedYear = st.slider("Year :", min_value=2020, max_value=2023, value=2022, step=1)
#-------------------------------------------------------------
df2 = p1.df_powergas_day[['year','month','cons']]
df2['cons'] = df2['cons'].apply(np.round)
df2.style.format(na_rep='', precision=1)

c1,c2 = st.columns([10,8])
with c1:
   show_Graph_bar(df2,'Stroomverbruik per jaar')
with c2:
   # df2.drop(['month'], axis=1, inplace=True)
   df3 = df2.groupby(['year','month']).sum('cons').sort_values(by=['year','month']).reset_index()
   df3['year'] = df3 ['year'].astype('string')
   #df3['month'] = df3 ['month'].astype('string')
   df3['cons'] = df3['cons'].apply(np.round).astype('string')
   #df3['month2'] = df3['month']
   df4= df3.pivot(index='month', columns='year', values='cons')
   show_table(df4)
