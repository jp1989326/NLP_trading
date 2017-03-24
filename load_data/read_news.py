'''created by Peng.
This module is for getting news titles using key words from reuters historical data and Livenews
and return list of strings. These strings can later be analyzed using sentimentscore in TwitterAxe. 
'''



from __future__ import print_function

import os
import pickle
import sys
sys.path.append('../Test_stocktalk')
import pandas as pd
import numpy as np


'''
This class is for finding key news titles from Database Reuters
'''
class read_reuters():
       
    def __init__(self, file_date, data_path='/home/peng/Documents/NLP/dataset/reuters_data/'):
        self.time_string = []
        self.title_string = []
        self.hyper_string = []
        self.file_date = file_date
        self.data_path = data_path

    def read_single(self):    
        list_dir = os.listdir(self.data_path)
        list_dir.sort()
        file = str(self.file_date) + '.pkl'
        if file in list_dir:
            with open(self.data_path + file, 'rb') as f:
                data = pickle.load(f, encoding = 'latin1')
                for datum in data:
                    self.time_string.append(datum['ts'])
                    self.title_string.append(datum['title'])
                    self.hyper_string.append(datum['href'])
        else:
            print ('There is no available news file on %r.' %(self.file_date[0:-4]))
    
    def locate_key(self, key_words):
        key_string = []
        self.read_single()
        for key_word in key_words:
            for title in self.title_string:
                if key_word in title.lower():
                    key_string.append(title.lower())
        return list(set(key_string))
 
'''
This class is for finding key news titles from Database NewsAPI
'''    
class read_newsapi(read_reuters):
    
    def __init__(self, file_date, data_path='/home/peng/Documents/NLP/dataset/NewsAPI/'):
        self.time_string = []
        self.title_string = []
        self.hyper_string = []
        self.file_date = file_date
        self.data_path = data_path
        self.detail_string = []
    
    def read_single(self):
        list_dir = os.listdir(self.data_path)
        list_dir.sort()
        file = str(self.file_date) + '.csv'
        if file in list_dir:
            df = pd.read_csv(self.data_path + file, header = 0)           
            self.time_string = np.array(df['time'])
            self.title_string = (np.array(df['title']))
            self.detail_string = (np.array(df['detail']))
            self.hyper_string = np.array(df['url']) 
        else:
            print ('There is no available news file on %r.' %(self.file_date))         