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
            .header{color: black; background-color: #d5dade; position: fixed; left: 0; width: 100%; margin-top:-100px; font-size: 18px;}
  .header tr {height:15%;} .header td {padding:10; border:none; word-wrap: break-word;}
  .footer{color: black; background-color: #a5a9b0; position: fixed; bottom: 0; left:0; font-size: 18px;}
  .footer td {border:none; word-wrap: break-word; border-collapse:collapse; vertical-align:middle; text-align:center;}
</style>""", unsafe_allow_html=True)

# st.markdown("<h3 style='text-align: center; color: #0c0d0c;'><b>1. Load your corpus</b></h>", unsafe_allow_html=True)

st.markdown("""<h3 style='text-align: center; color: #0c0d0c;'><b>1. Load your corpus</b></h>
<table class="header">
  <tr>
    <td style="background-color:#d5dade;text-align:left;">📑 <b>SNARE <font color='gray'>1.0</font></b> Spatial Narrative Representation Environment</td>
    <td style="text-align: center; width:10%"><a href="#ADVANCED">Advanced</a></td>
    <td style="text-align: center; width:10%"><a href="#ABOUT">About</a></td>
  </tr>
</table>""", unsafe_allow_html=True)

github_svg = """<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-github" viewBox="0 0 16 16">
 <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.012 8.012 0 0 0 16 8c0-4.42-3.58-8-8-8"/>
</svg>"""

st.markdown(f"""<link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" rel="stylesheet"/>
<table class="footer">
  <tr>
    <td colspan="9"; style="background-color:#d5dade; padding:10x 10x; text-align:left;">📑<b>SNARE <font color='gray'>1.0</font></b></td>
  </tr>
  <tr>
    <td style="text-align:right; vertical-align: top;">
        <img src="https://github.com/SpaceTimeNarratives/spacetimenarratives.github.io/blob/master/assets/images/STNlogo.png?raw=true" alt="STNLogo" height=30 width=30></img></td>
    <td style="width:25%; font-size:1vw; text-align:left;"><b>SNARE</b> is a project designed<br>and developed by the<br>Spatial Narratives Collaborative<br>© 2023 (Apache License 2.0) &nbsp;&nbsp; {github_svg} Github</td>
    <td style="width:12%;"><img src="https://raw.githubusercontent.com/IgnatiusEzeani/streamlit-playground/main/img/lancs-logo.svg" alt="Lancs_Logo" height=auto width=80%></img></td>
    <td style="width:12%;"><img src="https://raw.githubusercontent.com/IgnatiusEzeani/streamlit-playground/main/img/leeds.webp" alt="Leeds Logo" height=auto width=100%></img></td>
    <td style="width:12%;"><img src="https://github.com/IgnatiusEzeani/streamlit-playground/blob/main/img/Stanford.png?raw=true" alt="Stanford logo.png" height=auto width=80%></img></td>
    <td style="width:12%;"><img src="https://github.com/IgnatiusEzeani/streamlit-playground/blob/main/img/manchester_logo.png?raw=true" alt="Manchester Logo" height=auto width=80%></image></td>
    <td style="width:12%;"><img src="https://github.com/IgnatiusEzeani/streamlit-playground/blob/main/img/bristol_logo.png?raw=true" alt="Bristol Logo" height=auto width=100%></image></td>
    <td style="width:12%;"><img src="https://github.com/IgnatiusEzeani/streamlit-playground/blob/main/img/IUPUI_logo.png?raw=true" alt="IUPUI Logo" height=auto width=80%></image></td>

  </tr>
</table>""", unsafe_allow_html=True)

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