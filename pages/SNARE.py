import os
import streamlit as st
import pandas as pd
from io import StringIO
import streamlit_antd_components as sac

def do_stuff_on_page_load():
    st.set_page_config(layout="wide",
                       initial_sidebar_state="collapsed")
    st.markdown(
        """<style>
            [data-testid="collapsedControl"] {display: none;}
            .stDeployButton {visibility: hidden;}
        </style>""", unsafe_allow_html=True,
    )

do_stuff_on_page_load()

st.markdown("""<style>
  .header{background-color: #d5dade; left: 0; width: 100%; margin-top:-124px; font-size: 20px; position: fixed;}

  .footer{background-color: #a5a9b0; position: fixed; bottom: 0; left:0; font-size: 20px;}            
</style>""", unsafe_allow_html=True)

st.markdown(f"""<h3 style='text-align: center; color: #0c0d0c;'>1. Load your corpus</h>            
<table class="header">
  <tr>
    <td style="background-color:#d5dade;text-align:left;">📑 <b>SNARE <font color='gray'>1.0</font></b> Spatial Narrative Representation Environment</td>
    <td style="text-align: center; width:10%"><a href="#ADVANCED">Advanced</a></td>
    <td style="text-align: center; width:10%"><a href="#ABOUT">About</a></td>
  </tr>
</table>
            

  <table class="footer">
  <tr>
    <td colspan="9"; style="background-color:#d5dade; padding:10x 10x; text-align:left;">📑<b>SNARE <font color='gray'>1.0</font></b></td>
  </tr>
  <tr>
    <td style="text-align:right; vertical-align: top;">
        <img src="https://github.com/SpaceTimeNarratives/spacetimenarratives.github.io/blob/master/assets/images/STNlogo.png?raw=true" alt="STNLogo" height=30 width=30></img></td>
    <td style="width:25%; font-size:1vw; text-align:left;"><b>SNARE</b> is a project designed<br>and developed by the<br>Spatial Narratives Collaborative<br>© 2023 (Apache License 2.0) &nbsp;&nbsp; {open("img/github.svg").read()} Github</td>
    <td style="width:12%;"><img src="https://raw.githubusercontent.com/IgnatiusEzeani/streamlit-playground/main/img/lancs-logo.svg" alt="Lancs_Logo" height=auto width=80%></img></td>
    <td style="width:12%;"><img src="https://raw.githubusercontent.com/IgnatiusEzeani/streamlit-playground/main/img/leeds.webp" alt="Leeds Logo" height=auto width=100%></img></td>
    <td style="width:12%;"><img src="https://github.com/IgnatiusEzeani/streamlit-playground/blob/main/img/Stanford.png?raw=true" alt="Stanford logo.png" height=auto width=80%></img></td>
    <td style="width:12%;"><img src="https://github.com/IgnatiusEzeani/streamlit-playground/blob/main/img/manchester_logo.png?raw=true" alt="Manchester Logo" height=auto width=80%></image></td>
    <td style="width:12%;"><img src="https://github.com/IgnatiusEzeani/streamlit-playground/blob/main/img/bristol_logo.png?raw=true" alt="Bristol Logo" height=auto width=100%></image></td>
    <td style="width:12%;"><img src="https://github.com/IgnatiusEzeani/streamlit-playground/blob/main/img/IUPUI_logo.png?raw=true" alt="IUPUI Logo" height=auto width=80%></image></td>
  </tr>
</table>
""", unsafe_allow_html=True)

button = sac.buttons([
    sac.ButtonsItem(label='Paste your corpus',     icon='clipboard',     color='#b9ebe2'),
    sac.ButtonsItem(label='Use Sample Corpus',     icon='gift',          color='#b9ebe2'),
    sac.ButtonsItem(label='Upload your corpus',    icon='upload',        color='#b9ebe2'),
    sac.ButtonsItem(label='Open Existing Project', icon='folder2-open',  color='#b9ebe2'),
    sac.ButtonsItem(label='Run SPARQL Query',      icon='cloud',         color='#b9ebe2' , disabled=True),
    # sac.ButtonsItem(label='Open an existing project', icon='share-fill', href='https://ant.design/components/button'),
    ], position='left', format_func='title', align='center', )


if button=='Paste your corpus':
    text_data = st.text_area('', placeholder='Copy and paste your data from other applications or websites. You can use tabular (TSV, CSV, DSV) or JSON data.', height=150)
    sac.buttons([
        sac.ButtonsItem(label='NEXT', color='#b9ebe2'),
        ], format_func='title', align='end')
    
elif button=='Open Existing Project':
    sac.tree(
        items=[
            sac.TreeItem('CLDW', icon="book", tooltip="Dataset of Corpus of Lake District Writings"),
            sac.TreeItem('HST',  icon='chat-text', tooltip="Dataset of Holocaust Survivors' Testmonies")
            ]
            )
    
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
    st.info(f"""#### 🚧 **Under Construction:** This page is still being developed.""")

else:
    pass
# st.write(os.listdir())