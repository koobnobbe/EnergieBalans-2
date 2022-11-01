import streamlit as st
import pandas as pd
import numpy as np


################
from lib import api_p1mon as p1
from lib import constants as const
from lib import streamlit_objects as sobj
################

#-------------------------------------------------------------
# Application settings
#-------------------------------------------------------------
st.set_page_config( page_title="EnergieBalans - Monthly" )
#-------------------------------------------------------------

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
sobj.show_graph_bar_diff( p1.df_powergas_day[['year','month','day','cons']]
                         , 'Verschil stroomverbruik'
                         ,  selectedYear, selectedMonth)

sobj.show_graph_bar_diff( p1.df_powergas_day[['year','month','day','cons']]
                         , 'Verschil stroomverbruik'
                         , selectedYear, selectedMonth-1)

sobj.show_graph_bar_diff( p1.df_powergas_day[['year','month','day','cons']]
                         , 'Verschil stroomverbruik'
                         , selectedYear, selectedMonth-2)
