import streamlit as st
import streamlit_antd_components as sac

sac.buttons([
    sac.ButtonsItem(label='button'),
    sac.ButtonsItem(icon='apple'),
    sac.ButtonsItem(label='google', icon='google', color='#25C3B0'),
    sac.ButtonsItem(label='disabled', disabled=True),
    sac.ButtonsItem(label='link', icon='share-fill', href='https://ant.design/components/button'),
], position='left', format_func='title', align='center')

text_data = st.text_area('','Copy and paste your data from other applications or websites. You can use tabular (TSV, CSV, DSV) or JSON data.', height=200)