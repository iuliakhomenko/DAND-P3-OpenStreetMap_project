# -*- coding: utf-8 -*-
from modules import *


from requests import get  
from time import sleep
from random import randint
import csv

#This function scrapes street names from 12 pages of provided url and writes the result into a streetnames.csv file.
def extract_streetnames():
    #the request structure to this website is as following :
    #'http://www.lvivcenter.org/uk/streets/streets/?pageno=' + int
    #we need to construct 12 requests, so we need list of string variables from '1' to '12'
    pages = [str(i) for i in range (1,13)]

    #this variable monitors how many requests we have already made
    requests = 0
    standard_street_names = []

    for page in pages: 
        response = get('http://www.lvivcenter.org/uk/streets/streets/?pageno='+page)
        
        #we don't want to overload the server with our requests,so we control our loop with 
        #function sleep()
        sleep(randint(10,15))
        requests += 1
        print('Running request #{}'.format(requests))
            
        soup = BeautifulSoup(response.text, 'lxml')
        #information for all streets is in <ul> tag that has attribute 'class_'  with
        #value 'bulletList listStreets clearfix'
        streets = soup.find_all("ul", class_ = 'bulletList listStreets clearfix')    
        
        for element in streets:
        	#extracting streetnames 
            for street_name in element.find_all('a'):
                name = street_name.text
                #the extracted streetname also contains date when the street was founded,
                #we remove it
                name = re.sub("\([^)]*\)", "", name)
                #do some more cleaning
                name = name.replace("\r\n","")

                standard_street_names.append(name)
    print 'Done! Now creating your csv file ...'
    standard_street_names = [i.encode('utf-8') for i in standard_street_names]

    with open('streetnames.csv', 'wb') as myfile:
    	wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    	wr.writerow(standard_street_names)

extract_streetnames()    	
