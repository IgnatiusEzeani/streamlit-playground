import os
import pandas as pd
import streamlit as st
from collections import Counter
from labels import MESSAGES
'''
##### List of reviews
'''
lang='en'
EXAMPLES_DIR = 'example_texts_pub'

# read example and uploaded files
def read_file(file_source='example'):
    fname = ''
    if file_source=='example':
        fname = st.sidebar.selectbox(MESSAGES[lang][4], sorted([f for f in os.listdir(EXAMPLES_DIR) if f.startswith('Reviews')]))
        fname = os.path.join(EXAMPLES_DIR, fname)
    elif file_source=='uploaded':
        uploaded_file = st.sidebar.file_uploader("Upload review data", type=['txt','tsv','xlsx', 'xls'])
        if uploaded_file:
            fname = uploaded_file.name
        else:
            return False, st.info('''**NoFileUploaded:** Please upload your file using the upload button or by dragging the file into the upload area. Acceptable file formats include `.txt`, `.xlsx`, `.xls`, `.tsv`.''', icon="ℹ️")
    else:
        return False, st.error(f"FileSourceError: '{file_source}' is not a valid file source. Use 'example' or 'uploaded' only.")

    if fname.endswith('.txt'):
        text = open(fname, 'r', encoding='utf8').read() if file_source=='example' else uploaded_file.read().decode('utf8')
        data = st.text_area('Review to analyse', text, height=150).split('\n')
                
    elif fname.endswith(('.xls','.xlsx')):
        data = pd.read_excel(pd.ExcelFile(fname)) if file_source=='example' else pd.read_excel(uploaded_file)
        # data

    elif fname.endswith('.tsv'):
        data = pd.read_csv(fname, sep='\t', encoding='cp1252') if file_source=='example' else pd.read_csv(uploaded_file, sep='\t', encoding='cp1252')
        # data     
    else:
        return False, st.error(f"""**FileTypeError:** Unrecognised file format. Please ensure your file name has the extension `.txt`, `.xlsx`, `.xls`, `.tsv`.""", icon="🚨")
    return True, data

def read_pasted_data():
    return True, st.text_area('Paste reviews (replace the example text) to analyze',
'''Poor excuse for a hotel
Not really what we expected
Not bad Not bad
small but clean good location
give us a smile!
Not for claustrophobics
This is not a three stars hotel!
Sssshh - really good value!!!
Great hotel
Loved the Shellbourne Hotel''', height=150).split('\n')

def select_columns(dataframe): 
    "Total number of reviews: ", len(dataframe)
    options = st.sidebar.multiselect(
         'Select columns to analyse',
         list(dataframe.keys()),
         list(dataframe.keys())[:4])
    return dataframe[options]

option = st.sidebar.radio(MESSAGES[lang][0], (MESSAGES[lang][1], MESSAGES[lang][2], MESSAGES[lang][3]))
if option == MESSAGES[lang][1]: input_data = read_file()
elif option == MESSAGES[lang][2]: input_data = read_file(file_source='uploaded')
elif option == MESSAGES[lang][3]: input_data = read_pasted_data()
else: pass

class Analysis:
    def __init__(self, reviews):
        self.reviews = reviews

    def count_reviews(self):
        status, data = self.reviews
        return len(data) if status else None

analysis1 = Analysis(input_data)
'No of reviews: ', analysis1.count_reviews()