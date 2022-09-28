import os
import string
import random
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
pd.set_option('display.max_colwidth',None)

lang='en'
EXAMPLES_DIR = 'example_texts_pub'
# ---------------Checkbox options------------------
def checkbox_container(data):
    st.sidebar.markdown('What do you want to do with the data?')
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
    return [i.replace('dynamic_checkbox_','') for i in st.session_state.keys() if i.startswith('dynamic_checkbox_') and 
    st.session_state[i]]

def select_columns(data, key):
    # selected_columns = st.multiselect('Select column(s) below to analyse', data.columns, list(data.columns)[:5], help='Select columns you are interested in with this selection box', key=key)
    # if f"{key}_cols" in st.session_state.keys():
        # del st.session_state[f"{key}_cols"]
    selected_columns = st.multiselect('Select column(s) below to analyse', data.columns, help='Select columns you are interested in with this selection box', key= f"{key}_cols_multiselect")
    return data[selected_columns]

def get_wordcloud (data, key):
    st.markdown('''☁️ Word Cloud''')
    # cloud_columns = st.multiselect(
        # 'Select your free text columns:', data.columns, list(data.columns), help='Select free text columns to view the word cloud', key=f"{key}_cloud_multiselect")
    # input_data = ' '.join([' '.join([str(t) for t in list(data[col]) if t not in STOPWORDS]) for col in cloud_columns])
    input_data = ' '.join([' '.join([str(t) for t in list(data[col]) if t not in STOPWORDS]) for col in data])
    for c in PUNCS: input_data = input_data.lower().replace(c,'')
    
    input_bigrams = [' '.join(g) for g in nltk.ngrams(input_data.split(),2)]
    input_trigrams = [' '.join(g) for g in nltk.ngrams(input_data.split(),3)]
    input_4grams = [' '.join(g) for g in nltk.ngrams(input_data.split(),4)]
    
    mask = np.array(Image.open('img/welsh_flag.png'))
    # maxWords = st.number_input("Number of words:",
        # value=300,
        # step=50,
        # min_value=50,
        # max_value=300,
        # help='Maximum number of words featured in the cloud.',
        # key=fname
        # )
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(input_data)

    try:
        #creating wordcloud
        wc = WordCloud(
            # max_words=maxWords,
            stopwords=STOPWORDS,
            width=2000, height=1000,
            relative_scaling = 0,
            mask=mask,
            background_color="white",
            font_path='font/Ubuntu-B.ttf'
        ).generate(input_data)
            
        cloud_type = st.selectbox('Choose cloud category:',
            ['All words', 'Bigrams', 'Trigrams', '4-grams', 'Nouns', 'Proper nouns', 'Verbs', 'Adjectives', 'Adverbs', 'Numbers'], key= f"{key}_cloud_select")
        if cloud_type == 'All words':
            wordcloud = wc.generate(input_data)        
        elif cloud_type == 'Bigrams':
            wordcloud = wc.generate_from_frequencies(Counter(input_bigrams))        
        elif cloud_type == 'Trigrams':
            wordcloud = wc.generate_from_frequencies(Counter(input_trigrams))        
        elif cloud_type == '4-grams':
            wordcloud = wc.generate_from_frequencies(Counter(input_4grams))        
        elif cloud_type == 'Nouns':
            wordcloud = wc.generate_from_frequencies(Counter([token.text for token in doc if token.pos_ == "NOUN"]))        
        elif cloud_type == 'Proper nouns':
            wordcloud = wc.generate_from_frequencies(Counter([token.text for token in doc if token.pos_ == "PROPN"]))        
        elif cloud_type == 'Verbs':
            wordcloud = wc.generate_from_frequencies(Counter([token.text for token in doc if token.pos_ == "VERB"]))
        elif cloud_type == 'Adjectives':
            wordcloud = wc.generate_from_frequencies(Counter([token.text for token in doc if token.pos_ == "ADJ"]))
        elif cloud_type == 'Adverbs':
            wordcloud = wc.generate_from_frequencies(Counter([token.text for token in doc if token.pos_ == "ADV"]))
        elif cloud_type == 'Numbers':
            wordcloud = wc.generate_from_frequencies(Counter([token.text for token in doc if token.pos_ == "NUM"]))
        else: 
            pass
        color = st.radio('Switch image colour:', ('Color', 'Black'), key=f"{key}_cloud_radio")
        img_cols = ImageColorGenerator(mask) if color == 'Black' else None
        plt.figure(figsize=[20,15])
        plt.imshow(wordcloud.recolor(color_func=img_cols), interpolation="bilinear")
        plt.axis("off")
        st.set_option('deprecation.showPyplotGlobalUse', False)
        st.pyplot()
    except ValueError as err:
        st.info(f'Oh oh.. Please ensure that at least one free text column is chosen: {err}', icon="🤨")

#--------------Get Top n most_common words plus counts---------------
def getTopNWords(text, topn=5, removeStops=False):
    text = text.translate(text.maketrans("", "", string.punctuation))
    text = [word for word in text.lower().split()
                if word not in STOPWORDS] if removeStops else text.lower().split()
    return Counter(text).most_common(topn)        

#---------------------keyword in context ----------------------------
def get_kwic(text, keyword, window_size=1, maxInstances=10, lower_case=False):
    text = text.translate(text.maketrans("", "", string.punctuation))
    if lower_case:
        text = text.lower()
        keyword = keyword.lower()
    kwic_insts = []
    tokens = text.split()
    keyword_indexes = [i for i in range(len(tokens)) if tokens[i].lower() == keyword.lower()]
    for index in keyword_indexes[:maxInstances]:
        left_context = ' '.join(tokens[index-window_size:index])
        target_word = tokens[index]
        right_context = ' '.join(tokens[index+1:index+window_size+1])
        kwic_insts.append((left_context, target_word, right_context))
    return kwic_insts

#---------- get collocation ------------------------
def get_collocs(kwic_insts, topn=10):
    words=[]
    for l, t, r in kwic_insts:
        words += l.split() + r.split()
    all_words = [word for word in words if word not in STOPWORDS]
    return Counter(all_words).most_common(topn)

#----------- plot collocation ------------------------
def plot_collocation(keyword, collocs):
    words, counts = zip(*collocs)
    N, total = len(counts), sum(counts)
    plt.figure(figsize=(8,8))
    plt.xlim([-0.5, 0.5])
    plt.ylim([-0.5, 0.5])
    plt.plot([0],[0], '-o', color='blue',  markersize=25, alpha=0.7)
    plt.text(0,0, keyword, color='red', fontsize=14)
    for i in range(N):
        x, y = random.uniform((i+1)/(2*N),(i+1.5)/(2*N)), random.uniform((i+1)/(2*N), (i+1.5)/(2*N)) 
        x = x if random.choice((True, False)) else -x
        y = y if random.choice((True, False)) else -y
        plt.plot(x, y, '-og', markersize=counts[i]*10, alpha=0.3)
        plt.text(x, y, words[i], fontsize=12)
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.pyplot()

#-------------------------- N-gram Generator ---------------------------
def gen_ngram(text, _ngrams=2, topn=10):
    if _ngrams==1:
        return getTopNWords(text, topn)
    ngram_list=[]
    for sent in sent_tokenize(text):
        for char in sent:
            if char in PUNCS: sent = sent.replace(char, "")
        ngram_list += ngrams(word_tokenize(sent), _ngrams)
    ngram_counts = Counter(ngram_list).most_common(topn)
    sum_ngram_counts = sum([c for _, c in ngram_counts])
    return [(f"{' '.join(ng):27s}", f"{c:10d}", f"{c/sum_ngram_counts:.2f}%")
            for ng, c in ngram_counts]

def plot_kwic(data, key):
    st.markdown('''💬 Key Word in Context''')
    # cloud_columns = st.multiselect(
        # 'Select your free text columns:', data.columns, list(data.columns), help='Select free text columns to view the word cloud', key=f"{key}_kwic_multiselect")
        
    # input_data = ' '.join([' '.join([str(t) for t in list(data[col]) if t not in STOPWORDS]) for col in cloud_columns])
    input_data = ' '.join([' '.join([str(t) for t in list(data[col]) if t not in STOPWORDS]) for col in data])
    for c in PUNCS: input_data = input_data.lower().replace(c,'')
    
    try:
        topwords = [f"{w} ({c})" for w, c in getTopNWords(input_data, removeStops=True)]
        keyword = st.selectbox('Select a keyword:', topwords).split('(',1)[0].strip()
        window_size = st.slider('Select the window size:', 1, 10, 2)
        maxInsts = st.slider('Maximum number of instances:', 5, 50, 10, 5)
        # col2_lcase = st.checkbox("Lowercase?", key='col2_checkbox')
        kwic_instances = get_kwic(input_data, keyword, window_size, maxInsts, True)

        keyword_analysis = st.radio('Anaysis:', ('Keyword in context', 'Collocation'))
        if keyword_analysis == 'Keyword in context':
            kwic_instances_df = pd.DataFrame(kwic_instances,
                columns =['Left context', 'Keyword', 'Right context'])
            kwic_instances_df.style.set_properties(column='Left context', align = 'right')
            # subset=['Left context', 'Keyword', 'Right context'],
            # kwic_instances_df
            st.dataframe(kwic_instances_df)
            
        else: #Could you replace with NLTK concordance later?
            # keyword = st.text_input('Enter a keyword:','staff')
            collocs = get_collocs(kwic_instances) #TODO: Modify to accept 'topn'               
            colloc_str = ', '.join([f"{w}[{c}]" for w, c in collocs])
            st.write(f"Collocations for '{keyword}':\n{colloc_str}")
            plot_collocation(keyword, collocs)
    except ValueError as err:
        st.info(f'Oh oh.. Please ensure that at least one free text column is chosen: {err}', icon="🤨")


# reading example and uploaded files
def read_file(fname, file_source):
    file_name = fname if file_source=='example' else fname.name
    if file_name.endswith('.txt'):
        data = open(fname, 'r', encoding='cp1252').read().split('\n') if file_source=='example' else fname.read().decode('utf8').split('\n')
        data = pd.DataFrame.from_dict({i+1: data[i] for i in range(len(data))}, orient='index', columns = ['Reviews'])
        
    elif file_name.endswith(('.xls','.xlsx')):
        data = pd.read_excel(pd.ExcelFile(fname)) if file_source=='example' else pd.read_excel(fname)

    elif file_name.endswith('.tsv'):
        data = pd.read_csv(fname, sep='\t', encoding='cp1252') if file_source=='example' else pd.read_csv(fname, sep='\t', encoding='cp1252')
    else:
        return False, st.error(f"""**FileFormatError:** Unrecognised file format. Please ensure your file name has the extension `.txt`, `.xlsx`, `.xls`, `.tsv`.""", icon="🚨")
    return True, data

def get_data(file_source='example'):
    try:
        if file_source=='example':
            example_files = sorted([f for f in os.listdir(EXAMPLES_DIR) if f.startswith('Reviews')])
            fnames = st.sidebar.multiselect('Select example data file(s)', example_files, example_files[0])
            if fnames:
                return True, {fname:read_file(os.path.join(EXAMPLES_DIR, fname), file_source) for fname in fnames}
            else:
                return False, st.info('''**NoFileSelected:** Please select at least one file from the sidebar list.''', icon="ℹ️")
        
        elif file_source=='uploaded': # Todo: Consider a maximum number of files for memory management. 
            uploaded_files = st.sidebar.file_uploader("Upload your data file(s)", accept_multiple_files=True, type=['txt','tsv','xlsx', 'xls'])
            if uploaded_files:
                return True, {uploaded_file.name:read_file(uploaded_file, file_source) for uploaded_file in uploaded_files}
            else:
                return False, st.info('''**NoFileUploaded:** Please upload files with the upload button or by dragging the file into the upload area. Acceptable file formats include `.txt`, `.xlsx`, `.xls`, `.tsv`.''', icon="ℹ️")
        else:
            return False, st.error(f'''**UnexpectedFileError:** Some or all of your files may be empty or invalid. Acceptable file formats include `.txt`, `.xlsx`, `.xls`, `.tsv`.''', icon="🚨")
    except Exception as err:
        return False, st.error(f'''**UnexpectedFileError:** {err} Some or all of your files may be empty or invalid. Acceptable file formats include `.txt`, `.xlsx`, `.xls`, `.tsv`.''', icon="🚨")

class Analysis:
    def __init__(self, reviews):
        self.reviews = reviews

    def show_reviews(self, fname):
        st.markdown(f'''📄 Viewing data: `{fname}`''')
        st.dataframe(self.reviews)
        st.write('Total number of reviews: ', len(self.reviews))
        
    def show_wordcloud(self, fname):
        get_wordcloud(self.reviews, fname)
    
    def show_kwic(self, fname):
        plot_kwic(self.reviews, fname)

st.sidebar.markdown('''# 🌼 Free Text Visualizer''')
option = st.sidebar.radio(MESSAGES[lang][0], (MESSAGES[lang][1], MESSAGES[lang][2])) #, MESSAGES[lang][3]))
if   option == MESSAGES[lang][1]: input_data = get_data()
elif option == MESSAGES[lang][2]: input_data = get_data(file_source='uploaded')
# elif option == MESSAGES[lang][3]: input_data = read_example_data()
else: pass

status, data = input_data
if status:
    if 'feature_list' not in st.session_state.keys():
        feature_list = ['Data View', 'WordCloud','Keyword and Collocation','View Keyword in Context', 'View Sentiments']
        st.session_state['feature_list'] = feature_list
    else:
        feature_list = st.session_state['feature_list']
    checkbox_container(feature_list)
    feature_options = get_selected_checkboxes()
    
# With tabbed multiselect
    filenames = list(data.keys())
    tab_titles= [f"Analysis-{i}" for i in range(len(filenames))]
    tabs = st.tabs(tab_titles)
    for i in range(len(tabs)):
        with tabs[i]:
            _, df = data[filenames[i]]
            df = select_columns(df, key=i)
            analysis = Analysis(df)
            if not feature_options: st.info('Please select one or more actions from the sidebar checkboxes.', icon="ℹ️")
            if 'Data View' in feature_options: analysis.show_reviews(filenames[i])
            if 'WordCloud' in feature_options: analysis.show_wordcloud(filenames[i])
            if 'Keyword and Collocation' in feature_options: analysis.show_kwic(filenames[i])
            # st.info('Sorry, this feature is being updated. Call back later.', icon="ℹ️")
            if 'View Sentiments' in feature_options: st.info('Sorry, this feature is being updated. Call back later.', icon="ℹ️")

# 🏴󠁧󠁢󠁷󠁬󠁳󠁿🥸😎🤨🤔👍☑️👏🤝🏻

# def read_example_data():
    # fname = os.path.join(EXAMPLES_DIR, 'example_reviews.txt')
    # text = open(fname, 'r', encoding='cp1252').read()
    # lines = st.text_area('Paste reviews (replace the example text) to analyze', text, height=150).split('\n')
    # return True, pd.DataFrame.from_dict({i+1: lines[i] for i in range(len(lines))}, orient='index', columns = ['Reviews'])
    
    # df = df.astype(dtype={'name': 'string'})