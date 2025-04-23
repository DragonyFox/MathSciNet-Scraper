python-selenium, python-webdriver-manager and python-pandas need to be installed

In names.txt, enter the names to search for line by line.
The results will be saved in mathscinet-output.csv

Changelog:

Error fixed: When an entry is at 0 it has different formatting. Added lots of try & except for now since I couldn't think of anything better
Changed how multiple results are handled: will now fetch all data that single results also fetch
