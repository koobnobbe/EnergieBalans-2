################
import streamlit as st
import pandas as pd
import numpy as np

from lib import api_p1mon as p1
from lib import constants as const
from lib import streamlit_objects as sobj
#########################################

######################
# Application settings
######################
st.set_page_config( page_title="EnergieBalans - Yearly" ,layout="wide")

#################
# Data Collection
#################
@st.cache(persist=True, show_spinner=True)
def load_p1_powergas_day(reporting_year, reporting_month):
   df = p1.df_powergas_day[['timestamp_local', 'cons', 'prd', 'afn', 'gas']]
   df['month'] = pd.DatetimeIndex(df['timestamp_local']).month
   df['year'] = pd.DatetimeIndex(df['timestamp_local']).year
   df['day'] = pd.DatetimeIndex(df['timestamp_local']).day

   df = df[['day','month','year', 'cons', 'prd', 'afn', 'gas']].copy()
   df= df.query('year==' + reporting_year).query('month==' + reporting_month)
   return df

#####################
# screen presentation
#####################
st.title('Energy Dashboard - Yearly')
with st.sidebar:
    selectedYear = st.slider("Year :", min_value=2020, max_value=2023, value=2022, step=1)

#########################
# mainscreen presentation
#########################

df2 = p1.df_powergas_day[['year','month','cons']]
df2['cons'] = df2['cons'].apply(np.round)

c1,c2 = st.columns([10,8])
with c1:
    sobj.show_graph_bar(df2, selectedYear,'Stroomverbruik per jaar')
with c2:
    df3 = df2.groupby(['year','month']).sum('cons').sort_values(by=['year','month']).reset_index()
    df3['year'] = df3 ['year'].astype('string')
    df3['cons'] = df3['cons'].apply(np.round).astype('string')
    df4= df3.pivot(index='month', columns='year', values='cons')
    sobj.show_table(df4 )
