import os
import pandas as pd
import numpy as np
import streamlit as st
from collections import Counter
import spacy
import nltk
import en_core_web_sm
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx
from PIL import Image
from textblob import TextBlob
from nltk import word_tokenize, sent_tokenize, ngrams
from wordcloud import WordCloud, ImageColorGenerator
from nltk.corpus import stopwords
from labels import MESSAGES
nltk.download('punkt') # one time execution
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')

# Update with the Welsh stopwords (source: https://github.com/techiaith/ataleiriau)
en_stopwords = list(stopwords.words('english'))
cy_stopwords = open('welsh_stopwords.txt', 'r', encoding='iso-8859-1').read().split('\n') # replaced 'utf8' with 'iso-8859-1'
STOPWORDS = set(en_stopwords + cy_stopwords)
PUNCS = '''!→()-[]{};:'"\,<>./?@#$%^&*_~'''

lang='en'
EXAMPLES_DIR = 'example_texts_pub'

# ---------------Testing out options------------------
def checkbox_container(data):
    st.sidebar.write('What do you want to see')
    layout = st.sidebar.columns(2)
    if layout[0].button('Select All'):
        for i in data:
            st.session_state['dynamic_checkbox_' + i] = True
        st.experimental_rerun()
    if layout[1].button('UnSelect All'):
        for i in data:
            st.session_state['dynamic_checkbox_' + i] = False
        st.experimental_rerun()
    for i in data:
        st.sidebar.checkbox(i, key='dynamic_checkbox_' + i)
        
def get_selected_checkboxes():
    return [i.replace('dynamic_checkbox_','') for i in st.session_state.keys() if i.startswith('dynamic_checkbox_') and st.session_state[i]]

# read example and uploaded files
def read_file(file_source='example'):
    fname = ''
    try:
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
            return False, st.error(f"FileSourceError: '{file_source}'  may be invalid or empty. Use 'example' or 'uploaded' only.")

        if fname.endswith('.txt'):
            data = open(fname, 'r', encoding='cp1252').read().split('\n') if file_source=='example' else uploaded_file.read().decode('utf8').split('\n')
            data = pd.DataFrame.from_dict({i+1: data[i] for i in range(len(data))}, orient='index', columns = ['Reviews'])
                    
        elif fname.endswith(('.xls','.xlsx')):
            data = pd.read_excel(pd.ExcelFile(fname)) if file_source=='example' else pd.read_excel(uploaded_file)
            selected_columns = st.multiselect('Select columns to analyse', data.columns, list(data.columns)[:5], help='Select columns you are interested in with this selection box')
            data=data[selected_columns]

        elif fname.endswith('.tsv'):
            data = pd.read_csv(fname, sep='\t', encoding='cp1252') if file_source=='example' else pd.read_csv(uploaded_file, sep='\t', encoding='cp1252')
        else:
            return False, st.error(f"""**FileTypeError:** Unrecognised file format. Please ensure your file name has the extension `.txt`, `.xlsx`, `.xls`, `.tsv`.""", icon="🚨")
        return True, data
    except Exception as err:
        return False, st.error(f"""**FileError:** `{err}`: '{fname}' may be invalid or empty. Use a valid non-empty file.""", icon="🚨")

def read_example_data():
    fname = os.path.join(EXAMPLES_DIR, 'example_reviews.txt')
    text = open(fname, 'r', encoding='cp1252').read()
    lines = st.text_area('Paste reviews (replace the example text) to analyze', text, height=150).split('\n')
    return True, pd.DataFrame.from_dict({i+1: lines[i] for i in range(len(lines))}, orient='index', columns = ['Reviews'])


class Analysis:
    def __init__(self, reviews):
        self.reviews = reviews

    def show_reviews(self):
        if status:
            st.markdown('''#### 📄 Review data''')
            st.dataframe(self.reviews)
            st.write('Total number of reviews: ', len(self.reviews))
            
    def get_wordcloud (self):
        cloud_columns = st.multiselect('Select your free text columns:', self.reviews.columns, list(self.reviews.columns), help='Select free text columns to view the word cloud')
        input_data = ' '.join([' '.join([str(t) for t in list(self.reviews[col]) if t not in STOPWORDS]) for col in cloud_columns])
        for c in PUNCS: input_data = input_data.lower().replace(c,'')
        
        input_bigrams = [' '.join(g) for g in nltk.ngrams(input_data.split(),2)]
        input_trigrams = [' '.join(g) for g in nltk.ngrams(input_data.split(),3)]
        input_4grams = [' '.join(g) for g in nltk.ngrams(input_data.split(),4)]
        
        mask = np.array(Image.open('img/welsh_flag.png'))
        maxWords = st.number_input("Number of words:",
            value=300,
            step=50,
            min_value=50,
            max_value=300,
            help='Maximum number of words featured in the cloud.'
            )
        nlp = spacy.load('en_core_web_sm')
        doc = nlp(input_data)
        
        bigrams      = Counter(input_bigrams)
        trigrams     = Counter(input_trigrams)
        fourgrams     = Counter(input_4grams)
        nouns        = Counter([token.text for token in doc if token.pos_ == "NOUN"])
        verbs        = Counter([token.text for token in doc if token.pos_ == "VERB"])
        proper_nouns = Counter([token.text for token in doc if token.pos_ == "PROPN"])
        adjectives   = Counter([token.text for token in doc if token.pos_ == "ADJ"])
        adverbs      = Counter([token.text for token in doc if token.pos_ == "ADV"])
        numbers      = Counter([token.text for token in doc if token.pos_ == "NUM"])
        try:
            #creating wordcloud
            wc = WordCloud(
                max_words=maxWords,
                stopwords=STOPWORDS,
                width=2000, height=1000,
                relative_scaling = 0,
                mask=mask,
                background_color="white",
                font_path='font/Ubuntu-B.ttf'
            ).generate(input_data)
                
            cloud_type = st.selectbox('Choose cloud category:',
                ['All words', 'Bigrams', 'Trigrams', '4-grams', 'Nouns', 'Proper nouns', 'Verbs', 'Adjectives', 'Adverbs', 'Numbers'])
            if cloud_type == 'All words':
                wordcloud = wc.generate(input_data)        
            elif cloud_type == 'Bigrams':
                wordcloud = wc.generate_from_frequencies(bigrams)        
            elif cloud_type == 'Trigrams':
                wordcloud = wc.generate_from_frequencies(trigrams)        
            elif cloud_type == '4-grams':
                wordcloud = wc.generate_from_frequencies(fourgrams)        
            elif cloud_type == 'Nouns':
                wordcloud = wc.generate_from_frequencies(nouns)        
            elif cloud_type == 'Proper nouns':
                wordcloud = wc.generate_from_frequencies(proper_nouns)        
            elif cloud_type == 'Verbs':
                wordcloud = wc.generate_from_frequencies(verbs)
            elif cloud_type == 'Adjectives':
                wordcloud = wc.generate_from_frequencies(adjectives)
            elif cloud_type == 'Adverbs':
                wordcloud = wc.generate_from_frequencies(adverbs)
            elif cloud_type == 'Numbers':
                wordcloud = wc.generate_from_frequencies(numbers)
            else: 
                pass
            color = st.radio('Switch image colour:', ('Color', 'Black'))
            img_cols = ImageColorGenerator(mask) if color == 'Black' else None
            plt.figure(figsize=[20,15])
            plt.imshow(wordcloud.recolor(color_func=img_cols), interpolation="bilinear")
            plt.axis("off")
            st.set_option('deprecation.showPyplotGlobalUse', False)
            st.pyplot()
        except ValueError as err:
            st.info(f'Oh oh..Please ensure that at least one free text column is chosen: {err}', icon="🤨")

st.sidebar.markdown('''# 🌼 Free Text Visualizer''')
option = st.sidebar.radio(MESSAGES[lang][0], (MESSAGES[lang][1], MESSAGES[lang][2], MESSAGES[lang][3]))
if   option == MESSAGES[lang][1]: input_data = read_file()
elif option == MESSAGES[lang][2]: input_data = read_file(file_source='uploaded')
elif option == MESSAGES[lang][3]: input_data = read_example_data()
else: pass

status, data = input_data
if status:
    analysis1 = Analysis(data)
    if 'feature_list' not in st.session_state.keys():
        feature_list = ['View data', 'View WordCloud','View Collocation','View Keyword in Context', 'View Sentiments']
        st.session_state['feature_list'] = feature_list
    else:
        feature_list = st.session_state['feature_list']
    checkbox_container(feature_list)
    feature_options = get_selected_checkboxes() 

    if 'View data' in feature_options: analysis1.show_reviews()
    if 'View WordCloud' in feature_options: analysis1.get_wordcloud()
    if 'View Collocation' in feature_options: st.info('Sorry, this feature is being updated. Call back later.', icon="ℹ️")
    if 'View Keyword in Context' in feature_options: st.info('Sorry, this feature is being updated. Call back later.', icon="ℹ️")
    if 'View Sentiments' in feature_options: st.info('Sorry, this feature is being updated. Call back later.', icon="ℹ️")
    
# 🏴󠁧󠁢󠁷󠁬󠁳󠁿🥸😎🤨🤔👍☑️👏🤝🏻