import argparse

parser = argparse.ArgumentParser(description="scrap website python project and print on secreen (u r free to chose the number of pages to scrap with range arguments)")

parser.add_argument("x", type=int, help="page top range")
parser.add_argument("y", type=int, help="page end range")
args = parser.parse_args()

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
pages = [str(i) for i in range(args.x,args.y)]

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

all_records=[]
all_records.append((i_name, i_camera, i_size, i_price, i_processor, i_rating, i_ROM))

#print(iphone_ratings.info())
print(all_records)