'''
Helpful functions to facilitate data auditing and cleaning process
'''

#this function checks if input element has particular ['v'] attribute and returns it's value
def search_for_value(element, v_value):
    return element.attrib['k'] == v_value

#this function prints first a rows of sorted dictionary with values in descending order 
def sorted_dictionary(dictionary, a):
	for key, value in sorted(dictionary.iteritems(), key=lambda (key,value): (value,key), reverse = True):
		if value > a:
			print "%s: %s" % (key, value)

