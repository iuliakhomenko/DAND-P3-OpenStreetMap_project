#To check the postcodes we need to define a standard. We will use the list of postcodes for 
#Lviv city and region  provided by Ukrainian National Postal Service as our 'golden standard'.
#As there is no downloadable list, we would need to scrape it from UNPS web-site.

from modules import *

#this function extracts postcodes from downloaded html files and returns them in a list
#we first download the pages we need to scrape information from: one separate file for Lviv city postcodes 
# and one file for Lviv region 

file_path_oblast = '/Users/iulia/Documents/Docs/StudyMaterials/Udacity/DAND/P3/P3_final_project/postal_codes_html/post_codes_ua.htm'
file_path_lviv = '/Users/iulia/Documents/Docs/StudyMaterials/Udacity/DAND/P3/P3_final_project/postal_codes_html/post_codes_lviv.htm'

def extract_postal_codes (f_path):
    post_codes = []
    soup = BeautifulSoup(open(f_path), 'lxml')
    post_codes_table = soup.find_all("table", {"class":"grid"})
    #We iterate through search results looking for rows, each rows starts with <tr> tag
    for element in post_codes_table:
        table_rows = element.find_all('tr')
        #Skip first row with column names  
        for data_point in table_rows[1:]:
            #Look for the elements of the row that start with <td> tag and select first element 
            #with actual postcodes
            one_city_data = data_point.find_all('td')
            post_codes.append(one_city_data[0].text)
    return post_codes    

postal_codes = extract_postal_codes(file_path_oblast) + extract_postal_codes(file_path_lviv)


#function that audit postcodes found in a file and outputs the dictionary with 
#encountered problems and their count
def audit_postcodes(osm_file):
    unexpected_postcodes = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events = ('start',)):
        if elem.tag == "node" or elem.tag == "way" or elem.tag == "relation":
            for tag in elem.iter("tag"):
                if search_for_value(tag, 'addr:postcode'):
                    postcode = tag.attrib['v']
                    if postcode not in postal_codes:
                        if postcode not in unexpected_postcodes.keys():
                            unexpected_postcodes[postcode] = 1
                        else:
                            unexpected_postcodes[postcode]+=1
    return unexpected_postcodes 

unexpected_postcodes = audit_postcodes(file_path)
'''
Problems encountered in postcodes audit :
- not valid postcodes (less than 5-digits length) or containing problematic characters;
- outdated postcodes (postcodes that are valid but have been changed)
- non-existent postcodes (postcodes that never existed for Lviv city and region)

Cleaning strategy:
- if the postcode contains problematic characters or it's length less than 5, remove it;
- if the postcode contains 5-digits and like typical Lviv postcodes starts with digits 79, 
   80, 81 or 82,  ignore it;
- if the postcode contains 5-digits but do not start with 79, 80, 81 or 82, remove it.
'''
#function for cleaning problematic postcodes 

problemchars = re.compile(r'[\-=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

def clean_postcodes(postcode):
	if re.match(problemchars,postcode) or len(postcode) !=5:
		postcode = ''
	elif re.match(r'^79|80|81|82', postcode) and len(postcode) == 5:
		pass
	else: 
		postcode = ''	
	return postcode	

if __name__ == '__main__':
    for event, elem in ET.iterparse(file_path, events = ('start',)):
        if elem.tag == "node" or elem.tag == "way" or elem.tag == "relation":
            for tag in elem.iter("tag"):
                if search_for_value(tag, 'addr:postcode'):
                    postcode = tag.attrib['v']
                    if postcode not in postal_codes:
                        print clean_postcodes(postcode)

