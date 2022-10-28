# Python App

import streamlit as st
import pandas as pd
import numpy as np

st.title('Energy Dashboard')
with st.sidebar:
    with st.echo():
        st.write("This code will be printed to the sidebar.")
