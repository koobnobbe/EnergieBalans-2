import streamlit as st
import pandas as pd
import numpy as np
from lib import constants as const
#-------------------------------------------------------------
# Application settings
#-------------------------------------------------------------
st.set_page_config( page_title="EnergieBalans - Weekly" )
#-------------------------------------------------------------

#-------------------------------------------------------------
# Data Collection
#-------------------------------------------------------------

#-------------------------------------------------------------


# -------------------------------------------------------------
# screen presentation
# -------------------------------------------------------------
st.title('Energy Dashboard - Weekly')
with st.sidebar:
   selectedYear = st.slider("Year :", min_value=2020, max_value=const.current_year+1, value=const.current_year, step=1)
   selectedWeek = st.slider("Week :", min_value=1, max_value=53, value=const.current_week, step=1)
#-------------------------------------------------------------
st.write("Not Yet Implemented")