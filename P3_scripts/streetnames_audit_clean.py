# -*- coding: utf-8 -*-

from modules import *
from transliterate import translit

#as a starting point define the street types that we expect to see in the streetname
expected_street_types = ["площа", "вулиця", "проїзд", "провулок", "проспект", "дорога"]
#we convert strings in this list to unicode to compare them to values from our xml doc
expected_street_types = [i.decode('utf-8') for i in expected_street_types]

#this function audits streetnames in the osm file and returns a set of unique streetnames which 
#do not have conventional street type defined in expected_street_types list
def audit_streetnames(osm_file):
	unexpected_streetnames = set()
	parser = ET.iterparse(osm_file, events = ('start',))
	for event, element in parser:
	    if element.tag == 'way' or element.tag == 'node' or element.tag == 'relation':
	        for tag in element.iter():
	            try:
	                if search_for_value (tag, 'addr:street'):
	                    if tag.attrib['v'].split()[-1] not in expected_street_types: 
	                        unexpected_streetnames.add(tag.attrib['v'])
	            except KeyError:
	                continue
	return unexpected_streetnames

unexpected_streetnames = audit_streetnames(file_path)	  

'''
Problems encountered during streetnames audit:
- some streetnames are written in Latin letters while the others in Cyrilic;
- street type comes before street name;
- streetnames are written without streettype (e.g. 'Pasichna Street' is written as 'Pasichna')

Cleaning plan :
- use Python transliterate package to convet Latin streetnames to Cyrillic;
- use regex to identify if the streettype is mentioned in the streetname and if so, 
  move it to the end of the string;
- check the streetnames with no streettype against a list of correct streetnames  and avenues 
  for Lviv area, if the given name is in the list, change it as written in the list;
- manually correct remaining small issues and typos using mapping;
'''  
'''
To prepare for cleaning, we scrape the correct list of streetnames from
http://www.lvivcenter.org/uk/streets/streets/, using extract_streetname() function (please check README)
and write them into streetnames.csv file

'''
#create strandard_street_names list from streetnames.csv file
import csv

with open('streetnames.csv', 'rb') as f:
    reader = csv.reader(f)
    your_list = list(reader)

#we extract the list we need from the list of lists we read from csv file 
standard_street_names = your_list[0]
#we convert all elements in the list from bytes to unicode and remove extra spaces
standard_street_names = [unicode(street_name, 'utf-8').strip() for street_name in standard_street_names]

  
#Now that we have correct streetnames list, we also define list of avenues. Since there are only
#four avenues in Lviv, we can compile the avenue list manually

avenues = ["В'ячеслава Чорновола", "Свободи", "Тараса Шевченка", "Червоної Калини"]
avenues = [i.decode('utf-8') for i in avenues]

#we also create mapping to correct the typos we noticed during the audit
street_names_mapping = {u'Тершаківців' : u'Тершаковців вулиця',
                        u'Тершаковцев улица' : u'Тершаковців вулиця',
                        u'Богомолціа': u'Богомольця вулиця' ,
                        u'Залізнична Стреет' : u'Залізнична вулиця',
                        u'Лісова' : u'Лісна вулиця',
                        u'Львів, вул.Наукова' : u'Наукова вулиця',
                        u'Івана Франка' : u'Франка І. вулиця',
                        u'Христини Сушка Скачківської':u'Христини Сушко-Скачківської вулиця',
                        u'Білика' : u'Білика вулиця',
                        u"Солов'їна": u"Солов'їна вулиця",
                        u'Сухомлинського':u'Сухомлинського вулиця'}


#Now we are ready to do the actual cleaning 
def clean_streetnames (name):
    #checking if the name contain Latin characters and if so convert it to Cyrillic
    if re.search('[a-zA-Z]', name):
        name = translit(name, 'uk')

    #capturing a single letter at the beginning of string (e.g. Victor Hugo Avenue 
    #in Ukrainian is perfectly valid as V. Hugo Avenue or Hugo V. Avenue) 
    #or housenumber written in the street name and delete them
    name = re.sub(r'^\w\.(\s)?|\d+(\w$)?','', name, flags = re.UNICODE)   
    
    #checking if the street name is lowercase and if so capitalize it
    if name.islower():
        name = name.capitalize()    

    #checking if there is a streettype and if so, put it after the street name
    for street_type in expected_street_types:
        if street_type in name:
            name_list = name.split()
            name_list.append(street_type)
            name_list.remove(street_type) 
            name = ' '.join(name_list)
        else:
            #checking strings that contain only street names against the correct list of streetnames
            # if the streetname is in the list we add 'street' streettype to the string
            for standard_name in standard_street_names: 
                if name in standard_name:
                    name = standard_name + ' ' +u'вулиця'            
            #check if the string belong to avenues and if so add 'avenue' street type to the string
            for standard_avenue in avenues:
                if name in standard_avenue:
                    name = standard_name +' ' + u'проспект'

    #correct typos using mapping                
    if name in street_names_mapping.keys():
    	name = name.replace(name,street_names_mapping[name])                
    return name        

if __name__ == '__main__':
    parser = ET.iterparse(file_path, events = ('start',))
    for event, element in parser:
        if element.tag == 'way' or element.tag == 'node' or element.tag == 'relation':
            for tag in element.iter():
                try:
                    if search_for_value (tag, 'addr:street'):
                        if tag.attrib['v'].split()[-1] not in expected_street_types:
                            print clean_streetnames(tag.attrib['v'])
                except KeyError:
                    continue            