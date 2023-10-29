
from datetime import datetime, timedelta
import json
import csv
import pandas as pd
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time

#determine current time
time_now = datetime.now()

#convert to a timestamp and round
timestamp_now = round(time_now.timestamp())

#specify a time in days to extract data from
interval = timedelta(days = 62)

#open the browsing history
with open('History.json', encoding='UTF-8') as file:
    records = json.load(file)
    
    #search through records
    for record in records['Browser History']:
        
        #extract search time, change its format
        search_time = round(record['time_usec']/1000000)
        changed_time = datetime.fromtimestamp(search_time)
        difference = time_now-changed_time
        
        #set the file name
        file_name = 'pronunciation_' + str(time_now.date()) + '.csv'
        
        if "dictionary.cambridge" in record['url']:
            
            #put data in the file
            with open(file_name, 'a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file, delimiter=';',quotechar='"')
                formatted_name = record['title'].split('|')[0]
                writer.writerow([formatted_name, record['url'], changed_time])
            
        #break if time interval is reached
        if difference.days == interval.days:
            break

#sort, remove duplicates, save
sheet = pd.read_csv(file_name, sep=';', encoding='UTF-8')
sheet.sort_values(by=sheet.columns[2], ascending=False, inplace=True)
sheet.drop_duplicates(subset=sheet.columns[0], keep='first', inplace=True)
pd.DataFrame.to_csv(sheet, path_or_buf=file_name, sep=';', index=False)

