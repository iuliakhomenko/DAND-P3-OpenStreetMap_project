'''
Doing some simple parsig of the xml doc, to understand it's structure and decide which 
elements to audit and clean
'''

from modules import *

'''
Create a function that parses the file and returns a dictionary, where keys are unique tags 
found in the file and valuesare nested dictionaries, containing count for each tag and a list 
all it's unique attributes
E.g.

{
tag1: {count : int, 
        attributes : [atrib1, attrib2,] },
 tag2: {count : int, 
        attributes : [atrib1, attrib2,] }, 
        ...
}               
'''

def count_tags(filename):
    tags = {}
    parser = ET.iterparse(filename, events=('start',))
    for event, elem in parser:

        if elem.tag not in tags.keys():

            tags[elem.tag] = {}
            tags[elem.tag]['count'] = 1
            tags[elem.tag]['attributes'] = []

            for attribute in elem.attrib.keys():
                if attribute not in tags[elem.tag]['attributes']:
                    tags[elem.tag]['attributes'].append(attribute)
        else:
            tags[elem.tag]['count'] += 1

            for attribute in elem.attrib.keys():
                if attribute not in tags[elem.tag]['attributes']:
                    tags[elem.tag]['attributes'].append(attribute)

    return tags

tags = count_tags(file_path)
pprint.pprint(tags)

'''
The information in the attributes listed above is mostly pre-defined (e.g. 'uid', 'timestamp',
 'user', 'id') and essentially needs no cleaning .

However, part of the information in 'k' and 'v' attributes for <tag> tag is user defined 
(as mentioned by OSM documentation for Map Features) and that's where most of mistakes are 
likely to occur and therefore some cleaning might be required.

So we create a function that will take xml file as an input and return k-attribute values 
which contains user-defined information such as:

- addresses: attributes starting with 'addr:' ;
- names : attributes contain string 'name';
- references : attributes like 'iata', 'icao' and those containing string 'ref';
- contact details for an object (e.g. phone, fax, email address etc)
The function will return k-values that occur in the document more than 100 times.

'''

import re

manually_entered_fields = ['iata', 'icao','phone','fax', 'email', 'website']
element_names = ['node', 'way', 'relation']

def is_manual_entry (file_name): 
    parser = ET.iterparse(file_name, events = ('start',))
    k_dict = {}
    elem_children = {}
    for event, element in parser:
        if element.tag in element_names:
            for child in element.iter(): 
                for key in child.attrib.keys():
                    if key == 'k':
                        if re.match(r'^addr:',child.attrib[key]) or \
                        re.match(r'^(w+)?name(w+)?$', child.attrib[key]) or \
                        child.attrib[key] in manually_entered_fields or \
                        re.match(r'^(w+)?ref(w+)?$', child.attrib[key]):
                            if child.attrib[key] not in k_dict.keys():
                                k_dict[child.attrib[key]] = 1
                            else:
                                k_dict[child.attrib[key]] += 1
             
    print "Attributes with manually entered values and their count:" 
    sorted_dictionary(k_dict, 100)
            
is_manual_entry(file_path)   

'''
We will audit and clean values for the following attributes: 
- 'addr:street';
- 'addr:housenumber';
- 'addr:postcodes';
'''
