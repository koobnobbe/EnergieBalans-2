# Python App

import streamlit as st

import pandas as pd
import numpy as np

from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode
################
from lib import api_p1mon as p1
from lib import constants as const
#from lib import api_solaredge as slr
################

#-------------------------------------------------------------
# Application settings
#-------------------------------------------------------------
st.set_page_config( page_title="EnergieBalans - Home" )
#-------------------------------------------------------------

#-------------------------------------------------------------
# Data Collection
#-------------------------------------------------------------
@st.cache
def load_p1_powergas_day():
   data = p1.df_powergas_day
   return data
#-------------------------------------------------------------
def show_table(df):
   gb = GridOptionsBuilder.from_dataframe(df)
   gb.configure_pagination(paginationAutoPageSize=False)  # Add pagination
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
   df2 = grid_response['data']
   df2


# -------------------------------------------------------------
# sidebar presentation
# -------------------------------------------------------------
st.title('Energy Dashboard')
with st.sidebar:
   selectedYear = st.slider("Year :", min_value=2020, max_value=2023, value=const.current_year, step=1)
   selectedMonth = st.slider("Month :", min_value=1, max_value=12, value=const.current_month, step=1)
#-------------------------------------------------------------

df = p1.df_powergas_day[['timestamp_local','cons','prd','afn','gas']]
df['month'] = pd.DatetimeIndex(df['timestamp_local']).month
df['year']  = pd.DatetimeIndex(df['timestamp_local']).year
df['day'] = pd.DatetimeIndex(df['timestamp_local']).day
df = df.query('year==' + str(const.current_year)).query('month==' + str(const.current_month))
df = df[['day' ,'cons','prd','afn','gas']].copy()

show_table(df)
