import streamlit as st
import pandas as pd
import numpy as np
from lib import constants as const
#-------------------------------------------------------------
# Application settings
#-------------------------------------------------------------
st.set_page_config( page_title="EnergieBalans - Monthly" )
#-------------------------------------------------------------

#-------------------------------------------------------------
# Data Collection
#-------------------------------------------------------------

#-------------------------------------------------------------


# -------------------------------------------------------------
# screen presentation
# -------------------------------------------------------------
st.title('Energy Dashboard - Monthly')
with st.sidebar:
   selectedYear = st.slider("Year :", min_value=2020, max_value=2023, value=const.current_year, step=1)
   selectedMonth = st.slider("Month :", min_value=1, max_value=12, value=const.current_month, step=1)
#-------------------------------------------------------------

st.write("Not Yet Implemented")