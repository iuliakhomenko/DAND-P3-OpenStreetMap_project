workflow_func.py  - small but helpful functions that facilitate overall audit and clean process.

modules.py - script that imports all libraries used during data auditing and cleaning.
This was created for simplicity: instead of importing all the libraries in each
audit and cleaning script, we simply import modules.py. The modules.py also contains file_path variable, which is the path to osm xml file we are processing. This variable was also included in modules.py to avoid writing it in every audit and clean script.   

parsing_data.py - functions that parse osm xml file, count and print tags and attributes encountered in a file. It also contains a function that defines manually entered data in 
the xml file. 

postcodes_audit_clean.py - functions for auditing and cleaning postal codes data

housenumber_audit_clean.py - functions for auditing and cleaning housenumbers data

web-scraping.py - function that scrapes street names data from a given website and writes it into streetnames.csv file. This was created to speed up the performance of streetnames_audit_clean.py script (instead of scraping the info from 12 web pages online every time you run it, our streetnames_audit_clean.py script works with local csv file)

streetnames_audit_clean.py - functions for auditing and cleaning street names data.

preparing_for_db.py - functions that convert osm xml elements to dictionaries and then create a json document ready to be inserted into database.
 



