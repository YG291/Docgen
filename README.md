# STANDARD INCORPORATION DOCUMENT GENERATOR

Instructions for usage:

1) Clone the repository

2) Modify the two files located in input for the specific client's information. 

Note that the information must be written in the exact same format as the example provided in the input folder.

2.1) For the global_data.csv file, replace the entries with the client's information. **DO NOT add any new rows or columns to global_data.csv.

2.2) For the people.csv file, under the 'Type' Column, there are four possible options. Any given person may be a part of one or more of the following groups:
- directors, shareholders, officers, ip
    - note that ip means intellectual property assignors
- You must exactly write the categories that the person belongs to. It must be written in comma separated format, as written above, with the exact same capitalization.

2.3) For the people.csv file, the following columns do not need to be filled: [COUNT],[PRICE],[BEMAIL],item_list

2.4) if the item_list field is applicable (that is, the person is assigning intellectual property), write it out in semicolon-separated format, in the exact same manner as provided in the example file.

2.5) if more than one person is a member of the company, enter the other members' information immediately under the information of the first row in the same manner described above. DO NOT add new columns.

3) Run genfunctions.py -> an output folder will appear with the specific corporation's details. This folder will contain all the generated documents for this particular company.

(i.e. output Big Corp Inc.)

4) Special notes:
4.1) re-generating a company's documents will replace the previous generated documentation with documentation for your new inputs.
4.2) certain elements are hardcoded to the templates. if you wish to include new placeholders to the templates, you need to simply include a new field in one of the input data files, depending on which is more appropriate. Specifically, if the new information is 'corporate' information, that is, general information describing the company (such as who the CEO is), then it is more appropriate to add such placeholders to global_data. The converse is true for people.csv. 
4.3) I have also included a custom settings dictionary as part of the Doc class, if future extensions require use of attribute dictionaries.
