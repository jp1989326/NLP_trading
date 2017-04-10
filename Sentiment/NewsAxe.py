import sys
sys.path.append('../Load_data')

import read_news
import TwitterAxe as Twa
import numpy as np
import pandas as pd

'''Generate buy sell hold signal[1,0,-1] according to the socre and threshold value'''
def buy_sell_signal(score, thres=[-0.005, 0.052]):
    if score > thres[1]:
        signal = 1
    elif score < thres[0]:
        signal = -1
    else:
        signal = 0
    return signal     

'''generate index score based on individual stock and the corresponding weight. Weight is defaultly set as
uniform'''
def index_score(scores, weights=None):
    if weights == None:
        weights = ([1/len(scores)]*len(scores))        
    return np.dot(scores, weights)

''' get the stock sentimental score'''
def stock_score(date, key_words=['']):
    read = read_news.read_reuters(file_date = date)
    key_string = read.locate_key(key_words)
    score = Twa.sentimentScore(key_string)  
    return score

'''get the scores for multiple companies/stocks... elements_list must be in [[''], [''], ['']] format'''
def multistocks_score(date, elements_list):
    scores = []
    for element in elements_list:
        scores.append(stock_score(date, key_words=element))
    return scores    