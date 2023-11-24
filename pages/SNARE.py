import streamlit as st
import streamlit_antd_components as sac

sac.buttons([
    sac.ButtonsItem(label='Open Existing Project', icon='folder2-open',color='#b9ebe2'),
    sac.ButtonsItem(label='Paste your corpus', icon='clipboard', color='#b9ebe2'),
    sac.ButtonsItem(label='Upload your corpus', icon='upload', color='#b9ebe2'),
    sac.ButtonsItem(label='Use Sample Corpus', color='#b9ebe2'),
    sac.ButtonsItem(label='Run SPARQL Query', disabled=True, color='#b9ebe2'),
#    sac.ButtonsItem(label='Open an existing project', icon='share-fill', href='https://ant.design/components/button'),
], position='left', format_func='title', align='center')

text_data = st.text_area('', placeholder='Copy and paste your data from other applications or websites. You can use tabular (TSV, CSV, DSV) or JSON data.', height=200, )

sac.buttons([
    sac.ButtonsItem(label='NEXT', color='#b9ebe2'),
], position='right', format_func='title', align='right')