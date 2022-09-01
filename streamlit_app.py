import os
import pandas as pd
import streamlit as st
from collections import Counter
from labels import MESSAGES
'''
### Testing file upload
'''
lang='en'
EXAMPLES_DIR = 'example_texts_pub'

# read example and uploaded files
def read_file(file_source='example'):
    # fname, uploaded_file = '',None
    if file_source=='example':
        fname = st.sidebar.selectbox(MESSAGES[lang][4], sorted([f for f in os.listdir(EXAMPLES_DIR) if f.startswith('Reviews')]))
        fname = os.path.join(EXAMPLES_DIR, fname)
    elif file_source=='uploaded':
        uploaded_file = st.sidebar.file_uploader("Upload review data", type=['txt','tsv','xlsx', 'xls'])
        fname = uploaded_file.name
    else:
        return st.error(f"FileSourceError: '{file_source}' is not a valid file source. Use 'example' or 'uploaded' only.")

    if fname.endswith('.txt'):  
        text = open(fname, 'r', encoding='iso-8859-1').read() if file_source=='example' else uploaded_file.read()
        data = st.text_area('Review to analyse', text, height=150)
                
    elif fname.endswith(('.xls','.xlsx')):
        data = pd.read_excel(pd.ExcelFile(fname)) if file_source=='example' else pd.read_excel(uploaded_file)
        data

    elif fname.endswith('.tsv'):
        data = pd.read_csv(fname, sep='\t', encoding='cp1252') if file_source=='example' else pd.read_csv(uploaded_file, sep='\t', encoding='cp1252')
        data
        
pd.read_csv('c:/~/trainSetRel3.txt')


    else:
        return st.error(f"FileTypeError: Unrecognised file type. Use only '.txt', '.xlsx', '.xls', '.tsv' files.")
    return data

def read_pasted_data():
    return st.text_area('Paste reviews to analyze (replace the example text)',
'''Poor excuse for a hotel
Not really what we expected
Not bad Not bad
small but clean good location
give us a smile!
Not for claustrophobics
This is not a three stars hotel!
Sssshh - really good value!!!
Great hotel
Loved the Shellbourne Hotel''', height=150)

def select_columns(dataframe): 
    "Total number of reviews: ", len(dataframe)
    options = st.sidebar.multiselect(
         'Select columns to analyse',
         list(dataframe.keys()),
         list(dataframe.keys())[:4])
    return dataframe[options]


# def read_example_file():
    # example_fname = st.sidebar.selectbox(MESSAGES[lang][4], sorted([f for f in os.listdir(EXAMPLES_DIR) if f.startswith('Reviews')]))
    # if example_fname.endswith('.txt'):
        # with open(os.path.join(EXAMPLES_DIR, example_fname), 'r', encoding='iso-8859-1') as example_file:
            # data = st.text_area('Review to analyse', example_file.read(), height=150)
           
    # elif example_fname.endswith(('.xls','.xlsx')):
        # data = pd.read_excel(pd.ExcelFile(os.path.join(EXAMPLES_DIR, example_fname)))
        # data
        
    # elif example_fname.endswith('.tsv'):
        # data = pd.read_table(os.path.join(EXAMPLES_DIR, example_fname), encoding='cp1252')
        # data
    
    # else:
        # data = 'Invalid file format'
    
    # return data

# def read_uploaded_data():
    # uploaded_fname=''
    # uploaded_file = st.sidebar.file_uploader("Upload review data", type=['txt','tsv','xlsx', 'xls'])
    # if uploaded_file is not None:
        # uploaded_fname = uploaded_file.name

    # if uploaded_fname.endswith('.txt'):
        # data = st.text_area('Review to analyse', uploaded_file.read(), height=150)
    # elif uploaded_fname.endswith(('.xls','.xlsx')):
        # data = pd.read_excel(uploaded_file)
        # data
    # elif uploaded_fname.endswith('.tsv'):
        # data = pd.read_table(uploaded_file, encoding='cp1252')
        # data
    # else:
        # data = 'Invalid file format'
    # return data

option = st.sidebar.radio(MESSAGES[lang][0], (MESSAGES[lang][1], MESSAGES[lang][2], MESSAGES[lang][3]))
if option == MESSAGES[lang][1]:
    # input_data = read_example_file()
    input_data = read_file()

elif option == MESSAGES[lang][2]:
    # input_data = read_uploaded_data()
    input_data = read_file(file_source='uploaded')

elif option == MESSAGES[lang][3]:
    input_data = read_pasted_data()
else:
    pass

#----------------------------
    # for option in options:
        # option, Counter(dataframe[option])

# df1 = df[['a', 'b']]
# test_uploaded_file = st.sidebar.file_uploader("Just testing file upload", type=['txt','xlsx', 'xls'])
# if test_uploaded_file is not None:
    # if test_uploaded_file.type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
        # process_excel_file(test_uploaded_file)
