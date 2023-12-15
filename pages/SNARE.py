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

# st.markdown("""<style> ul{list-style-type: none; padding: 10px 10px; margin:0; overflow: hidden; background-color: #d5dade;}
#             li.left {float: left;} li.right {float: right;} li a:hover {background-color: #111; } </style>""", unsafe_allow_html=True)

# st.markdown("""<ul><li class='left'><b>📑SNARE 1.0</b> Spatial Narrative Representation Environment</li>
#             <li class='right'><a href="#SNARE">About</a></li> 
#             <li class='right'><a href="#ADVANCED">Advanced</a></li></ul>""", unsafe_allow_html=True)

st.markdown("""<style>
            .header{color: black; background-color: #d5dade; position: fixed; left: 0; width: 100%; margin-top:-110px; font-size: 18px;}
  .header tr {height:15%;} .header td {padding:10; border:none; word-wrap: break-word;}
  .footer{color: black; background-color: #a5a9b0; position: fixed; bottom: 0; left:0; font-size: 18px;}
  .footer td {padding:10; border:none; word-wrap: break-word; border-collapse:collapse;}
</style>""", unsafe_allow_html=True)

st.markdown("<h3 style='text-align: center; color: #0c0d0c;'><b>1. Load your corpus</b></h>", unsafe_allow_html=True)

st.markdown("""<table class="header">
  <tr>
    <td style="background-color:#d5dade; padding:10x 10x">📑 <b>SNARE <font color='gray'>1.0</font></b> Spatial Narrative Representation Environment</td>
    <td style="text-align: center; width:10%"><a href="#ADVANCED">Advanced</a></td>
    <td style="text-align: center; width:10%"><a href="#ABOUT">About</a></td>
  </tr>
</table>""", unsafe_allow_html=True)

button = sac.buttons([
    sac.ButtonsItem(label='Use Sample Corpus',     icon='gift',          color='#b9ebe2'),
    sac.ButtonsItem(label='Upload your corpus',    icon='upload',        color='#b9ebe2'),
    sac.ButtonsItem(label='Paste your corpus',     icon='clipboard',     color='#b9ebe2'),
    sac.ButtonsItem(label='Open Existing Project', icon='folder2-open',  color='#b9ebe2'),
    sac.ButtonsItem(label='Run SPARQL Query',      icon='cloud',         color='#b9ebe2' , disabled=True),
    # sac.ButtonsItem(label='Open an existing project', icon='share-fill', href='https://ant.design/components/button'),
    ], position='left', format_func='title', align='center', )


if button=='Paste your corpus':
    text_data = st.text_area('', placeholder='Copy and paste your data from other applications or websites. You can use tabular (TSV, CSV, DSV) or JSON data.', height=250)
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

github_svg = """<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-github" viewBox="0 0 16 16">
 <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.012 8.012 0 0 0 16 8c0-4.42-3.58-8-8-8"/>
</svg>"""

st.markdown(f"""<link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" rel="stylesheet"/>
<table class="footer">
  <tr>
    <td colspan="7"; style="background-color:#d5dade; padding:10x 10x;">📑<b>SNARE <font color='gray'>1.0</font></b></td>
  </tr>
  <tr>
    <td style="vertical-align:middle; text-align:right; width:6%; vertical-align: top; vertical-align: top">
        <img src="https://github.com/SpaceTimeNarratives/spacetimenarratives.github.io/blob/master/assets/images/STNlogo.png?raw=true" alt="STNLogo" height=40 width=40></img></td>
    <td style="width:35%; font-size:16px"><b>SNARE</b> is a project designed<br>and developed by the<br>Spatial Narratives Collaborative<br>© 2023 (Apache License 2.0) &nbsp;&nbsp; {github_svg} Github</td>
    <td style="width:5%;"></td>
    <td style="width:15%;"><img src="https://comms.leeds.ac.uk/wp-content/uploads/sites/51/2021/04/Visual-identity-section-images--e1618925864440.png" alt="Leeds Logo" height=60 width=180></img></td>
    <td style="width:15%;"><img src="https://www.lancaster.ac.uk/media/wdp/style-assets/images/logos/lu-logo.svg" alt="Lancs_Logo" height=50 width=150></img></td>
    <td style="width:30%;"><img src="https://identity.stanford.edu/wp-content/uploads/sites/3/2020/07/block-s-right.png" alt="Stanford logo.png" height=100 width=90></img>
      <img src="https://identity.stanford.edu/wp-content/uploads/sites/3/2020/06/wordmark-nospace-stacked-red.png" alt="Stanford logo.png" height=40 width=90></img></td>


    <td><image src="Manchester Logo.png?raw=true" alt="Manchester Logo" height=5 width=30></image></td>
  </tr>
</table>""", unsafe_allow_html=True)

# st.write(os.listdir())