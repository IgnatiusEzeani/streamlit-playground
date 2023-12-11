import streamlit as st
import streamlit_antd_components as sac
# from PIL import Image
# image = Image.open('img/snare.png')
# st.image(image)

def do_stuff_on_page_load():
    st.set_page_config(layout="wide",
                       initial_sidebar_state="collapsed")
    st.markdown(
        """<style>
            [data-testid="collapsedControl"] {
            display: none}
        </style>""",
        unsafe_allow_html=True,
    )

do_stuff_on_page_load()
button = sac.buttons([
    sac.ButtonsItem(label='Paste your corpus', icon='clipboard', color='#b9ebe2'),
    sac.ButtonsItem(label='Open Existing Project', icon='folder2-open',color='#b9ebe2'),
    sac.ButtonsItem(label='Upload your corpus', icon='upload', color='#b9ebe2'),
    sac.ButtonsItem(label='Use Sample Corpus', icon='gift', color='#b9ebe2'),
    sac.ButtonsItem(label='Run SPARQL Query', icon='cloud', color='#b9ebe2', disabled=True),
#    sac.ButtonsItem(label='Open an existing project', icon='share-fill', href='https://ant.design/components/button'),
    ], position='left', format_func='title', align='center')

if button=='Paste your corpus':
    st.write("The selected button label is: "+ button)
    text_data = st.text_area('', placeholder='Copy and paste your data from other applications or websites. You can use tabular (TSV, CSV, DSV) or JSON data.', height=200, )
    sac.buttons([
        sac.ButtonsItem(label='NEXT', color='#b9ebe2'),
        ], format_func='title', align='end')