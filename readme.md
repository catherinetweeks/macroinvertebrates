# Macroinvertebrate Database
For CSC 230 Databases Final Project Spring 2026

Created by:
Catherine Weeks, Danielle Justo, Grace Cordova, Zoe Plumridge 

Source Data: 
https://github.com/marneypratt/macroS26/tree/main

Data collected by Marney Pratt and students from Mill River, Smith College, Northampton, MA. Supplemental data from NOAA and USGS. 

## Files:
.csv files provided by Marney Pratt
macroinvertebrates.db file (database file) 
.ipynb to generate .db from .csv
queryNOAA.py and queryUSGS.py are called by .ipynb to access APIs for up-to-date data. 

## How to run:
In terminal: 
```
pip install python
pip install pandas
pip install requests
pip install datasette

```

### Run website locally
In terminal: 
```
datasette macroinvertebrates.db 
```
> returns a link to open in browser
Ctrl+C in terminal to close website

### Run website locally on root account 
root account has permission to make edits and view more information than non-root 

In terminal: 
```
datasette macroinvertebrates.db --root
```
> returns a link to open in browser

## Updating information
To access updated information from NOAA and USGS, run queryNOAA.py  and queryUSGS.py from .ipynb

To update .csv files, drag new .csv files with the same formatting and titles into the file save space. Replace. All previously updated information is saved in the .db file. Any duplicates rows will not be added. 
