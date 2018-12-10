# -*- coding: utf-8 -*-

import requests
import pandas as pd
import time
from functools import reduce
import numpy as np
import time
from bs4 import BeautifulSoup
import requests
import nltk 
#cleaning function
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk import word_tokenize
import string
from nltk.tokenize import RegexpTokenizer
from textblob import Word
from nltk.corpus import wordnet
from nltk.stem.snowball import SnowballStemmer
#clustering function
from sklearn.cluster import KMeans
from scipy.spatial.distance import cdist
import matplotlib.pyplot as plt
from IPython.display import Image
from IPython.core.display import HTML 
from importlib import reload
import unicodedata
import matplotlib as mpl
from wordcloud import WordCloud, STOPWORDS
from operator import itemgetter

#--------extracting data---------

def extractring_page(url):
    try:
        l=[]
        soup=BeautifulSoup(requests.get(url).text, "html.parser")
        time.sleep(2)
        try:
            y=soup.findAll('p',{'titolo text-primary'})# extract the content of the tag which contains the links
            for house in y:
                # extracting the links, some links are not started with s string,therefore we they don't work
                s='https://www.immobiliare.it'
                s1=house.contents[1]['href'] 
                if s1.startswith("https")==False:
                    s1=s+s1# s is added to the incomplete links.
                l.append(s1)
        except:
            pass
    except:
        l=['The page does not exit']
    return(l)

#In the following function the required information for each announcent is extracted from Scrappinglink file that contains the links.

def Objective_page(url):
    try:
        tag=BeautifulSoup(requests.get(url).text, "html.parser")
        time.sleep(2)
        l1=['piano','bagni','superficie','locali']
        df=[]
        # the tag that contains the information of the house such as locali...
        x=tag.findAll('div',{'class':'im-property__features'})
        y=tag.findAll('div',{'class':'clearfix description'}) #the tag that contains the description 
        d={}
        # the texts of the tag is extracted and with stripped_strings  attribute the white spaces of the string is removed
        house=[text for text in x[0].stripped_strings]
        house.reverse()# we reverse the list of our text that makes the extractions easier
        house1=[text for text in y[0].stripped_strings]
        house1=" ".join(house1)
        #Below the superfice, bagni, locali and price is extracted based on their position in the list.
        for i in l1:
            if i in house:
                index=house.index(i)
                if i=='superficie':
                    d[i]=house[index+3]
                else:
                    d[i]=house[index+1]
                if house[-1].find('€')!=-1:
                    d['prezzo(€)']=house[-1]
        d['description']=house1
    except:
        d['description']="there was a problem in this link"
    del tag
    return(d)
# function for removing the accents
import unicodedata
def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])


#function for removing the punctuation
o=string.punctuation+'“–”’'
def remove_punctuations(text):
    for punctuation in o:
        text = text.replace(punctuation, '')
    return text


def jaccard_similarity(a, b):
    c = a.intersection(b)
    return float(len(c)) / (len(a) + len(b) - len(c))

from operator import itemgetter
def jaccard_calculation(l,l1):
    dictS={}
    for i in range(6):
        jaccard=[]
        for k in l:
            if k[1]==i:
                jaccard.append(k[0])
        for j in range(7):
            jaccard1=[]
            for k1 in l1:
                if k1[1]==j:
                    jaccard1.append(k1[0])
            dictS[(i,j)]=funtions.jaccard_similarity(set(jaccard),set(jaccard1))
    dictS1=sorted(dictS.items(), key=itemgetter(1))
    return(dictS1)



