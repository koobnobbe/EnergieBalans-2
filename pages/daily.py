import streamlit as st
import datetime
import pandas as pd
import numpy as np
from lib import constants as const
#-------------------------------------------------------------
# Application settings
#-------------------------------------------------------------
st.set_page_config( page_title="EnergieBalans - Daily" )

#-------------------------------------------------------------

#-------------------------------------------------------------
# Data Collection
#-------------------------------------------------------------

#-------------------------------------------------------------


# -------------------------------------------------------------
# screen presentation
# -------------------------------------------------------------
#st.image('images/knc_Logo_Compact.png')
st.title('Energy Dashboard - Daily')
with st.sidebar:
   selecteddate = st.date_input("date:", value= datetime.date(2022, 10,27), max_value=datetime.date(2022, 10,28),)
#-------------------------------------------------------------

st.write("Not Yet Implemented")