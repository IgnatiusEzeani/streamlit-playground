import streamlit as st
import pandas as pd
from io import StringIO
import streamlit_antd_components as sac
# from PIL import Image
# image = Image.open('img/snare.png')
# st.image(image)

def do_stuff_on_page_load():
    st.set_page_config(layout="wide",
                       initial_sidebar_state="collapsed")
    st.markdown(
        """<style>[data-testid="collapsedControl"] {display: none}</style>""", unsafe_allow_html=True,
    )

do_stuff_on_page_load()
button = sac.buttons([
    sac.ButtonsItem(label='Use Sample Corpus', icon='gift', color='#b9ebe2'),
    sac.ButtonsItem(label='Upload your corpus', icon='upload', color='#b9ebe2'),
    sac.ButtonsItem(label='Paste your corpus', icon='clipboard', color='#b9ebe2'),
    sac.ButtonsItem(label='Open Existing Project', icon='folder2-open',color='#b9ebe2'),
    # sac.ButtonsItem(label='Run SPARQL Query', icon='cloud', color='#b9ebe2', disabled=True),
    # sac.ButtonsItem(label='Open an existing project', icon='share-fill', href='https://ant.design/components/button'),
    ], position='left', format_func='title', align='center')

if button=='Paste your corpus':
    text_data = st.text_area('', placeholder='Copy and paste your data from other applications or websites. You can use tabular (TSV, CSV, DSV) or JSON data.', height=200, )
    sac.buttons([
        sac.ButtonsItem(label='NEXT', color='#b9ebe2'),
        ], format_func='title', align='end')
elif button=='Open Existing Project':
    sac.tree(items=[
        sac.TreeItem('CLDW', icon="book",
                    #  tag=sac.Tag('tag', color='red', bordered=False), 
                     tooltip="Dataset of Corpus of Lake District Writings"),

        sac.TreeItem('HST',  icon='chat-text', 
                     tooltip="Dataset of Holocaust Survivors' Testmonies")])
elif button=='Upload your corpus':
    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
        # To read file as bytes:
        bytes_data = uploaded_file.getvalue()
        st.write(bytes_data)

        # To convert to a string based IO:
        stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
        st.write(stringio)

        # To read file as string:
        string_data = stringio.read()
        st.write(string_data)

        # Can be used wherever a "file-like" object is accepted:
        dataframe = pd.read_csv(uploaded_file)
        st.write(dataframe)
elif button=='Use Sample Corpus':
    st.info(f'''**Under Construction:** This page is still being developed.''', icon="🚧")
else:
    pass