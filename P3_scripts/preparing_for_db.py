from modules import *
from postcodes_audit_clean import clean_postcodes
from streetnames_audit_clean import clean_streetnames
from housenumber_audit_clean import clean_housenumber

problemchars = re.compile(r'[=\+/&<>;"\?%#$@\, \t\r\n]')

CREATED = [ "version", "changeset", "timestamp", "user", "uid"]

#this function is formatting attributes and second level tags of the input element 
#and applying cleaning functions created previously for streetnames, postal 
#codes and housenumbers. 
#The function outputs the dictionary that is ready to be converted to json format.
#This function was adapted from MongoDB casestudy lesson

def shape_element(element):
    node = {}
    node['created'] = {}
    if element.tag == "node" or element.tag == "way" or element.tag == "relation":
        #processing attributes first
        node['type'] = element.tag
        attrib_dict = element.attrib
        for key in attrib_dict.keys():
            #handling special cases
            if key in CREATED:
                node['created'][key] = attrib_dict[key]
            elif key == 'lat':
                # lat and lon values should be in correct order in the array
                try:
                    node['pos'].insert(0, float(attrib_dict[key]))
                except KeyError:
                    node['pos'] = []
                    node['pos'].insert(0, float(attrib_dict[key]))
            elif key == 'lon':
                try:
                    node['pos'].insert(1, float(attrib_dict[key]))
                except KeyError:
                    node['pos'] = []
                    node['pos'].insert(1, float(attrib_dict[key]))
            else: #handling the remaining attributes
                node[key] = attrib_dict[key]
                
        #process second level tags
        for tag in element.iter('tag'):
            k = tag.attrib['k']
            v = tag.attrib['v']
            
            if re.match(problemchars, v) != None:
                continue
            #handling k values that start with 'addr:'
            addr_one_colon = re.match(r'(addr:)(\w+$)',k)
            no_addr_one_colon = re.match(r'(\w+)(\:)(\w+)',k)
            
            if addr_one_colon:
                #do cleaning of housenumbers, streetnames and postal codes first
                if k == 'addr:housenumber':
                    v = clean_housenumber(v)
                elif k == 'addr:postcode':
                    v = clean_postcodes(v)
                    if v == '':
                    	continue
                elif k == 'addr:street':
                    v = clean_streetnames(v)
                try:
                    node['address'][addr_one_colon.group(2)] = v
                except KeyError:
                    node['address'] = {}
                    node['address'][addr_one_colon.group(2)] = v
            
            #handling k values that don't start with 'addr' but have colon
            elif no_addr_one_colon:
                try:
                    node[no_addr_one_colon.group(1)] = no_addr_one_colon.group(3)
                except KeyError:
                    node[no_addr_one_colon.group(1)] = {}
                    node[no_addr_one_colon.group(1)] = no_addr_one_colon.group(3)
            else:
                node[k] = v
        if element.tag == 'way':
            for nd_tag in element.iter('nd'):
                nd_ref = nd_tag.attrib['ref']
                try:
                    node['node_refs'].append(nd_ref)
                except KeyError:
                    node['node_refs'] = []
                    node['node_refs'].append(nd_ref)
                
        return node
    else:
        return None


import codecs
import json

#this function was adapted from MongoDB casestudy lesson
def process_map(file_in, pretty = False):
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data


if __name__ == '__main__':
    process_map(file_path, pretty = True)
