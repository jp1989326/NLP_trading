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
     

class request_news:
    
    def __init__(self, df_filter): 
        self.title_string = []
        self.detail_string = []
        self.time_string = []
        self.url_string =[]
        self.source_string =[] 
        self.df_filter = df_filter
        self.source_relate =  np.array(self.df_filter['source_id'])
        self.data_path = data_path = '/home/peng/Documents/NLP/dataset/NewsAPI/'
        
    def refresh_string(self): 
        self.__init__(self.df_filter) 
        #------------------------------------------------ self.title_string = []
        #----------------------------------------------- self.detail_string = []
        #------------------------------------------------- self.time_string = []
        #--------------------------------------------------- self.url_string =[]
        #------------------------------------------------ self.source_string =[]
        
    def query(self, source, sortby='top'):       
        url = 'https://newsapi.org/v1/articles?'
        apikey='apiKey=6edc312567cd47e7a670525767fe5e08'
        source_url = 'source='+source+'&'
        sortby_url = 'sortBy='+str(sortby)+'&'
        query = url + source_url + sortby_url + apikey
        r = requests.get((query),verify=True)
        return r.json()          
        
    def save_news(self):
        
        df_saved_news = pd.DataFrame({'source_id':self.source_string,'title':self.title_string,\
                                     'detail':self.detail_string, 'time':self.time_string, 'url': self.url_string})
                        
        time_now = strftime("%Y-%m-%d-%H-%M-%S", localtime())
        df_saved_news.to_csv(self.data_path + time_now[:-9]+'.csv', header = True)
        print ('file saved')          
        
    def request_all(self,rolling = True):    
        for source in self.source_relate:
            sort_methods = np.array(self.df_filter[self.df_filter['source_id']==source]['sort'])[0]
            if 'latest' in sort_methods:
                sort_ = 'latest'
            else:
                sort_ = 'top'
            news = self.query(source, sort_)
            for single_news in news['articles']:                            
                self.source_string.append(source)
                self.title_string.append(single_news['title'])
                self.detail_string.append(single_news['description'])
                self.time_string.append(single_news['publishedAt'])
                self.url_string.append(single_news['url'])
                
                if rolling == True:
                    end_day = strftime("%Y-%m-%d-%H-%M-%S", localtime())
                    if (len(self.title_string)%400 == 0):
                        self.save_news()
                    if  end_day[-8:-6] in ['23', '00']:
                        sleep(60*60*1.5)
                        self.refresh_string() 
                        
def run():
    
    data_path = '/home/peng/Documents/NLP/dataset/NewsAPI/'
            
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
        df_filter = df_source[df_source['relate']==1]
        source_relate = np.array(df_filter['source_id'])
        
        return  df_filter  
    
    
    time_interval = 60*60*1.5
    mining_period = 60*60*24*7
    
    
    df_filter = source_list()
    
    axe = request_news(df_filter)
    
    
    
    
    print ("starting...")
    rt = RepeatedTimer(time_interval, axe.request_all, rolling=True) # it auto-starts, no need of rt.start()
    try:
        sleep(mining_period) # your long-running job goes here...
    finally:
        rt.stop() # better in a try/finally block to make sure the program ends!
        
    axe.save_news()
    print ('finished...')          



                           
if __name__ == '__main__': run()




