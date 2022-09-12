import os
import pandas as pd
import numpy as np
import streamlit as st
from collections import Counter
from labels import MESSAGES
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

class Analysis:
    def __init__(self, reviews):
        self.reviews = reviews

    def show_reviews(self):
        '''##### List of reviews'''
        status, data = self.reviews
        if status:
            st.dataframe(data)
            st.write('No of reviews: ', len(data))
    
    def get_wordcloud (self):
        status, data = self.reviews
        if status:
            cloud_columns = st.multiselect('Select your free text columns:', data.columns, list(data.columns), help='Select free text columns to view the word cloud')
            
            input_data = ' '.join([' '.join([str(t) for t in list(data[col]) if t not in STOPWORDS]) for col in cloud_columns])
            for c in PUNCS: input_data = input_data.lower().replace(c,'')
            
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
            nouns = Counter([token.lemma_ for token in doc if token.pos_ == "NOUN"])
            verbs = Counter([token.lemma_ for token in doc if token.pos_ == "VERB"])
            proper_nouns = Counter([token.lemma_ for token in doc if token.pos_ == "PROPN"])
            adjectives = Counter([token for token in doc if token.pos_ == "ADJ"])
            adverbs = Counter([token.lemma_ for token in doc if token.pos_ == "ADV"])
            numbers = Counter([token.lemma_ for token in doc if token.pos_ == "NUM"])

            #creating wordcloud
            wc = WordCloud(
                max_words=maxWords,
                stopwords=STOPWORDS,
                width=2000, height=1000,
                # contour_color= "black", 
                relative_scaling = 0,
                mask=mask,
                background_color="white",
                font_path='font/Ubuntu-B.ttf'
            ).generate(input_data)
                
            cloud_type = st.selectbox('Choose cloud type:', ['All words', 'Nouns', 'Proper nouns', 'Verbs', 'Adjectives', 'Adverbs', 'Numbers'])
            if cloud_type == 'All words':
                wordcloud = wc.generate(input_data)        
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
                
            # image_colors = ImageColorGenerator(mask)
            plt.figure(figsize=[20,15])
            
            # plt.imshow(wordcloud.recolor(color_func=image_colors), interpolation="bilinear")
            plt.imshow(wordcloud.recolor(color_func=img_cols), interpolation="bilinear")
            plt.axis("off")
            st.set_option('deprecation.showPyplotGlobalUse', False)
            st.pyplot()


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
        data = open(fname, 'r', encoding='cp1252').read().split('\n') if file_source=='example' else uploaded_file.read().decode('utf8').split('\n')
        data = st.dataframe({i: data[i] for i in range(len(data))})
        # data = st.text_area('Review to analyse', text, height=150).split('\n')
                
    elif fname.endswith(('.xls','.xlsx')):
        data = pd.read_excel(pd.ExcelFile(fname)) if file_source=='example' else pd.read_excel(uploaded_file)
        selected_columns = st.multiselect('Select columns to analyse', data.columns, list(data.columns)[:5], help='Select columns you are interested in with this selection box')
        # selected_columns = ['Q3. What date and time did you visit?', 'Q9. Anything you would like to tell us?', 'Other factors preventing you from visiting heritage sites:']
        data=data[selected_columns]

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

option = st.sidebar.radio(MESSAGES[lang][0], (MESSAGES[lang][1], MESSAGES[lang][2], MESSAGES[lang][3]))
if   option == MESSAGES[lang][1]: input_data = read_file()
elif option == MESSAGES[lang][2]: input_data = read_file(file_source='uploaded')
elif option == MESSAGES[lang][3]: input_data = read_pasted_data()
else: pass

analysis1 = Analysis(input_data)
analysis1.show_reviews()
analysis1.get_wordcloud()