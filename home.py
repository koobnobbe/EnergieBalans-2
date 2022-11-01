# Python App
################
import streamlit as st
import pandas as pd
import numpy as np

from lib import api_p1mon as p1
from lib import constants as const
from lib import streamlit_objects as sobj
#from lib import api_solaredge as slr
################

######################
# Application settings
######################
st.set_page_config( page_title="EnergieBalans - Home", layout="wide")
# Use the full page instead of a narrow central column


##################
# Data Collection
##################
@st.cache(persist=True, show_spinner=True)
def load_p1_powergas_day(reporting_year, reporting_month):
   df = p1.df_powergas_day[['date', 'month','day','year','month_code', 'cons', 'prd', 'afn', 'gas']].copy()
   df= df.query('year==' + reporting_year).query('month==' + reporting_month)
   return df



######################
# sidebar presentation
######################
st.title('Energy Dashboard')
with st.sidebar:
   selectedYear = st.slider("Year :", min_value=2020, max_value=2023, value=const.current_year, step=1)
   selectedMonth = st.slider("Month :", min_value=1, max_value=12, value=const.current_month, step=1)


#########################
# mainscreen presentation
#########################
st.write(str(selectedYear)+'-'+str(selectedMonth))
