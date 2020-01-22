#import all necessary libraries to use
from requests import get
import pandas as pd
from time import sleep
from time import time
from random import randint
from bs4 import BeautifulSoup
from IPython.core.display import clear_output
from warnings import warn

#create lists to store extracted data
#i_index = []
i_name = []
i_price = []
i_ROM = []
i_size = []
i_camera = []
i_processor = []
i_rating = []
#counter=0

#loop over pages
pages = [str(i) for i in range(1,9)]

# Preparing the monitoring of the loop
start_time = time()
requests = 0


for page in pages:
    my_url = get("https://www.flipkart.com/search?q=iphone&otracker=AS_Query_HistoryAutoSuggest_2_0&otracker1=AS_Query_HistoryAutoSuggest_2_0&marketplace=FLIPKART&as-show=on&as=off&as-pos=2&as-type=HISTORY&page="+page)
    
    # Pause the loop
    sleep(randint(8,15))

    # Monitor the requests
    requests += 1
    elapsed_time = time() - start_time
    print('Request:{}; Frequency: {} requests/s'.format(requests, requests/elapsed_time))
    clear_output(wait = True)

    # Throw a warning for non-200 status codes
    if my_url.status_code != 200:
        warn('Request: {}; Status code: {}'.format(requests, response.status_code))

        # Break the loop if the number of requests is greater than expected
    if requests > 72:
        warn('Number of requests was greater than expected.')  
        break 

    soup = BeautifulSoup(my_url.text, 'html.parser')

    containers = soup.findAll("div", {"class":"_1UoZlX"})
    #len(containers)
    
    #loop over items and prepare for saving
    for container in containers:
        iphone_name = container.find("div", {"class":"_3wU53n"}).text
        iphone_name = iphone_name.replace(",","|")
        i_name.append((iphone_name))
        iphone_price = container.find("div", {"class":"_1vC4OE _2rQ-NK"}).text
        iphone_price = iphone_price.replace("₹","")
        i_price.append((iphone_price))
        iphone_ROM = container.find("ul", {"class":"vFw0gD"}).contents[0].text
        iphone_ROM = iphone_ROM.replace("|","")
        i_ROM.append((iphone_ROM))
        iphone_size = container.find("ul", {"class":"vFw0gD"}).contents[1].text
        i_size.append((iphone_size))
        iphone_camera = container.find("ul", {"class":"vFw0gD"}).contents[2].text
        i_camera.append((iphone_camera))
        iphone_processor = container.find("ul", {"class":"vFw0gD"}).contents[3].text
        i_processor.append((iphone_processor))
        iphone_rating = container.find("div", {"class":"niH0FQ"}).text
        iphone_rating = iphone_rating[:3]
        i_rating.append((iphone_rating))
        #counter+=1
        #i_index.append((counter))

        
iphone_ratings = pd.DataFrame({#'id': i_index,
                               'name': i_name,
                                'camera': i_camera,
                                'display': i_size,
                                'price': i_price,
                                'processor': i_processor,
                                'rating': i_rating,
                                'rom': i_ROM
                              })
print(iphone_ratings.info())

#iphone_ratings.tail()
#save csv and json files into folders
import os
if not os.path.exists('csv'):
    os.mkdir('csv')
    iphone_ratings.to_csv('csv\iphones_flipkart.csv', index=False, encoding='utf-8')
    #save csv file for database CRUD
    iphone_ratings.to_csv('..\Database\DB\my_db\iphones_flipkart.csv', index=False, encoding='utf-8')
else:    
    #print("Directory already exists")
    iphone_ratings.to_csv('csv\iphones_flipkart.csv', index=False, encoding='utf-8')
    #save csv file for database CRUD
    iphone_ratings.to_csv('..\Database\DB\my_db\iphones_flipkart.csv', index=False, encoding='utf-8')
    
if not os.path.exists('json'):
    os.mkdir('json')
    iphone_ratings.to_json(r'json\iphones_flipkart.json')
else:    
    #print("Directory already exists")
    iphone_ratings.to_json(r'json\iphones_flipkart.json')