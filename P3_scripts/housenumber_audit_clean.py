# -*- coding: utf-8 -*-
from modules import *


#The traditional structure of a housenumber: a number (e.g.35) or a number followed 
#by a lowercase letter (35b), or a number followed by slash followed by a number (e.g. 35/1)
#this function checks if a housenumber has a conventional structure
def is_expected_housenumber (housenumber): 
    return bool(re.match(ur'^\d+(\-\d+)?[а-я]?(\/\d+)?$', housenumber, re.UNICODE))
       

#this function returns a list of housenumbers that         
def audit_housenumber (osm_file):        
	problem_housenumbers = []    
	parser = ET.iterparse(osm_file, events = ('start',))
	for event, element in parser:
	    if element.tag == 'way' or element.tag == 'node' or element.tag =='relation':
	        for tag in element.iter():
	            try:
	                if search_for_value (tag, 'addr:housenumber'):
	                    if is_expected_housenumber(tag.attrib['v'])== False:
	                        problem_housenumbers.append(tag.attrib['v'])
	            except KeyError:
	                continue
	return problem_housenumbers  

#problems = audit_housenumber(file_path)

'''
For the housenumbers there are several problems:
- inconsistant capitalization of letters in housenumbers;
- inconsistant whitespaces after housenumber digits;
'''	 

def clean_housenumber (housenumber):
    buildingnames = ["к", "корп", "корп.", "к."]
    #specifying data points, that we didn't catch for cleaning programmatically, so they should be manually corrected
    manual_correct = {u'60а, 1 корпус': u'60а корпус 1', u't' : u'', u'73a, корпус 4': u'73a корпус 4'}
    # convert mapping dictionary keys and values to unicode
    mapping = {}
    mapping [u'корпус'] = [unicode(x,'utf-8') for x in buildingnames]
    if housenumber in manual_correct.keys():
    	housenumber = manual_correct.values()[0]
    #housenumber = re.sub(ur'^[a-z]+$','',housenumber, flags = re.UNICODE )
    #removing punctuation and some other characters 
    housenumber = re.sub(ur'[\.№\-;]','',housenumber, flags = re.UNICODE)
    #cleaning those with inconsistant letter capitalization and spaces, convert to lowercase:
    if re.match(r'(^\d+)(\s+)?(\w$)', housenumber, flags = re.UNICODE):
        housenumber_list = housenumber.split()
        housenumber_list[-1] = housenumber_list[-1].lower()
        housenumber = ''.join(housenumber_list)
    #correct building number using mapping
    if re.match(ur'^\d+\w?\,?\s+?([а-я]+)(\W+)?(\d+)?$', housenumber, flags = re.UNICODE):
        building_name = re.match(ur'^\d+\w?\,?\s+?([а-я]+)(\W+)?(\d+)?$', housenumber, flags = re.UNICODE).group(1)
        if building_name in mapping[u'корпус']:
            housenumber = housenumber.replace(building_name, u'корпус ')
            housenumber = ' '.join(housenumber.split())        
    return housenumber 

if __name__ == '__main__':
	parser = ET.iterparse(file_path, events = ('start',))
	for event, element in parser:
	    if element.tag == 'way' or element.tag == 'node' or element.tag =='relation':
	        for tag in element.iter():
	            try:
	                if search_for_value (tag, 'addr:housenumber'):
	                    if is_expected_housenumber(tag.attrib['v'])== False:
	                    	print clean_housenumber(tag.attrib['v'])
	            except KeyError:
	                continue        	

       