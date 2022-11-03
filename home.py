# Python App
################
import streamlit as st
from streamlit_extras.dataframe_explorer import dataframe_explorer
import pandas as pd
import numpy as np

from lib import api_p1mon as p1
from lib import api_wallbox as wb
# from lib import api_solaredge as slr
from lib import calculations as calc
from lib import constants as const
from lib import streamlit_objects as sobj
from lib import utils as utils
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode
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
#st.write(str(selectedYear)+'-'+str(selectedMonth))
#st.write(p1.df_powergas_day.copy())
st.write('Today : ' + str(const.now))
st.write('First date of the week : ' + str(const.start_of_week))
#st.write(st.secrets["wallbox"]["username"])
#st.write(calc.df_power_combined_day)

#filtered_df = dataframe_explorer(calc.df_power_combined_day[['timestamp','int_low']])
#st.dataframe(filtered_df)
#st.write(calc.df_energy)\

st.metric(label= 'Temp', value= 21, delta= 3, delta_color='inverse')

df_graph = calc.df_energy.reset_index().query('year == '+str(selectedYear)+' and month == '+str(selectedMonth)+' and action != "Balans"')

sobj.show_graph(df_graph,'date','amount','name')
sobj.show_bargraph(calc.df_energy.reset_index() , selectedYear, selectedMonth)