### Overview

This project is focused on understanding the processes of collecting, auditing and cleaning data as well as storing and 
quering the data from noSQL database (MongoDB).

The dataset used in this project was downloaded in XML format from [OpenStreetMap](https://www.openstreetmap.org) and includes 
information about various geographical objects of Lviv city and region. 

The project involves auditing and cleaning downloaded dataset, loading it in MongoDB and quering information from 
the database. 

### Project Workflow

The workflow of this project is as following :
 1. parse XML document to understand its general structure (counting unqiue tags, defininng attributes for each tag etc.)
 2. folowing [OpenStreetMap documentation guidelines](http://wiki.openstreetmap.org/wiki/Map_Features), analyse which attributes 
 information was manually entered by OSM users i.e. which information is most likely to require auditing and cleaning. Based on 
 this analysis three attributes were selected for further processing
 3. audit and clean the information in selected attributes, using various data wrangling techniques (validation of the data, 
 filling missing information, defining outdated info and finally data cleaning (creating the cleaning strategy based on the results of 
 our audit and validation) etc)
 4. preparing cleaned data to be inserted in MongoDB by converting it to JSON format
 5. making queries from the data loaded into the database 
 
 ### Python libraries used in the project 
 
- ElementTree
- pprint
- re
- BeautifulSoup
- collections

### Project Structure

[sample_k10.osm](https://github.com/iuliakhomenko/DAND-P3-OpenStreetMap_project/blob/master/sample_k10.osm) - sample XML file taken from the dataset processed in the project 

[P3_DataWrangling_MongoDB.html](https://github.com/iuliakhomenko/DAND-P3-OpenStreetMap_project/blob/master/P3_DataWrangling_MongoDB.html) - report that contains detailed description of data auditing and cleaning performed, discusses
various problems encountered during data processing phase as well as gives an overview of the data based on queries made on
loaded data into MongoDB.

[P3_scripts](https://github.com/iuliakhomenko/DAND-P3-OpenStreetMap_project/tree/master/P3_scripts) - folder containing Python scripts for parsing, auditing and cleaning data and prepearing it for MongoDB.
For the detailed description of each script, check out [README](https://github.com/iuliakhomenko/DAND-P3-OpenStreetMap_project/blob/master/P3_scripts/README.txt) note in the folder. 

[postal_codes_html](https://github.com/iuliakhomenko/DAND-P3-OpenStreetMap_project/tree/master/postal_codes_html) - folder necessary to audit one of the attributes from the dataset. 

