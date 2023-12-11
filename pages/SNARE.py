import streamlit as st
import pandas as pd
from io import StringIO
import streamlit_antd_components as sac


def do_stuff_on_page_load():
    st.set_page_config(layout="wide",
                       initial_sidebar_state="collapsed")
    st.markdown(
        """<style>[data-testid="collapsedControl"] {display: none}</style>""", unsafe_allow_html=True,
    )

do_stuff_on_page_load()

# st.markdown('''<style> ul {list-style-type: none; margin: 0; padding: 1; overflow: hidden; background-color: #adb5ba;}
#             li {float: left;} li a {display: block; color: white; text-align: center; padding: 14px 16px; text-decoration: none;}
#             li a:hover {background-color: #111; } </style>''', unsafe_allow_html=True)


st.markdown("""<script "https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta3/dist/css/bootstrap.min.css"
            rel="stylesheet"
            integrity="sha384-eOJMYsd53ii+scO/bJGFsiCZc+5NDVN2yr8+0RDqr0Ql0h+rP48ckxlpbzKgwra6"
            crossorigin="anonymous"></script>""", unsafe_allow_html=True)

st.markdown('''<nav class="navbar navbar-expand-lg navbar-light bg-light">
    <div class="container-fluid">
      <a class="navbar-brand" href="#">Navbar</a>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavAltMarkup" aria-controls="navbarNavAltMarkup" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse justify-content-end" id="navbarNavAltMarkup">
        <div class="navbar-nav">
          <a class="nav-link active" aria-current="page" href="#">Home</a>
          <a class="nav-link" href="#">About</a>
          <a class="nav-link" href="#">Team</a>
          <a class="nav-link" href="#">Contact Us</a>
        </div>
      </div>
    </div>
  </nav>''', unsafe_allow_html=True)

# st.markdown("""<li><b>SNARE 1.0</b> Spatial Narrative Representation Environment</li>""", unsafe_allow_html=True)

# st.markdown('### 1. Load your corpus')

button = sac.buttons([
    sac.ButtonsItem(label='Use Sample Corpus', icon='gift', color='#b9ebe2'),
    sac.ButtonsItem(label='Upload your corpus', icon='upload', color='#b9ebe2'),
    sac.ButtonsItem(label='Paste your corpus', icon='clipboard', color='#b9ebe2'),
    sac.ButtonsItem(label='Open Existing Project', icon='folder2-open',color='#b9ebe2'),
    # sac.ButtonsItem(label='Run SPARQL Query', icon='cloud', color='#b9ebe2', disabled=True),
    # sac.ButtonsItem(label='Open an existing project', icon='share-fill', href='https://ant.design/components/button'),
    ], position='left', format_func='title', align='center')


if button=='Paste your corpus':
    text_data = st.text_area('', placeholder='Copy and paste your data from other applications or websites. You can use tabular (TSV, CSV, DSV) or JSON data.', height=250)
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