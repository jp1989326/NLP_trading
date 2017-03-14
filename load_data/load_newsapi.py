import requests
import pandas as pd
import numpy as np
from threading import Timer
import schedule
from time import time, gmtime, localtime, strftime, sleep

class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer     = None
        self.function   = function
        self.interval   = interval
        self.is_running = False
        self.args       = args
        self.kwargs     = kwargs
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False
     

def run():
    
    data_path = '/home/peng/Documents/NLP/dataset/NewsAPI/'
    
    def query(source, sortby='top'):       
        url = 'https://newsapi.org/v1/articles?'
        apikey='apiKey=6edc312567cd47e7a670525767fe5e08'
        source_url = 'source='+source+'&'
        sortby_url = 'sortBy='+str(sortby)+'&'
        query = url + source_url + sortby_url + apikey
        r = requests.get((query),verify=True)
        return r.json()  
        
    def source_list():   
        new = requests.get('https://newsapi.org/v1/sources?language=en')
        category = []
        source_id =[]
        sort_ = []
        relate_list= []
        for i in new.json()['sources']:
            category.append(i['category'])
            if i['category'] in ['general', 'business', 'technology','science-and-nature']:
                relate_list.append(1)
            else:
                relate_list.append(0)
            source_id.append(i['id'])
            sort_.append(i['sortBysAvailable'])        
        df_source = pd.DataFrame({'cat':category, 'source_id':source_id, 'relate':relate_list, 'sort':sort_})      
        return df_source   
        
    def request_all(rolling = True):    
        for source in source_relate:
            sort_methods = np.array(df_filter[df_filter['source_id']==source]['sort'])[0]
            if 'latest' in sort_methods:
                sort_ = 'latest'
            else:
                sort_ = 'top'
            news = query(source, sort_)
            for single_news in news['articles']:                            
                source_string.append(source)
                title_string.append(single_news['title'])
                detail_string.append(single_news['description'])
                time_string.append(single_news['publishedAt'])
                url_string.append(single_news['url'])
                
                if rolling == True:
                    if len(title_string)%400 == 0:
                        df_saved_news = pd.DataFrame({'source_id':source_string,'title':title_string,\
                                                     'detail':detail_string, 'time':time_string, 'url': url_string})
                        
                        time_now = strftime("%Y-%m-%d-%H-%M-%S", gmtime())
                        df_saved_news.to_csv(data_path + time_now[:-9]+'.csv', header = True)
                        print ('file saved')  
                        
    df_source = source_list()
    df_filter = df_source[df_source['relate']==1]
    source_relate = np.array(df_filter['source_id'])
    
    title_string = []
    detail_string = []
    time_string = []
    url_string =[]
    source_string =[] 
    
    time_interval = 60*30
    mining_period = 60 * 60 * 8
    
    print ("starting...")
    rt = RepeatedTimer(time_interval, request_all, rolling=True) # it auto-starts, no need of rt.start()
    try:
        sleep(mining_period) # your long-running job goes here...
    finally:
        rt.stop() # better in a try/finally block to make sure the program ends!
    
                           
if __name__ == '__main__': run()




