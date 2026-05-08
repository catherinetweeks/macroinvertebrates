# Macroinvertebrate Database
For CSC 230 Databases Final Project Spring 2026

Created by:
Catherine Weeks, Danielle Justo, Grace Cordova, Zoe Plumridge 

Here is [a link to the source data](https://github.com/marneypratt/macroS26/tree/main). 

Data collected by Marney Pratt and students from Mill River, Smith College, Northampton, MA. Supplemental data from NOAA and USGS. 

## Files:
.csv files provided by Marney Pratt
macroinvertebrates.db file (database file) 
.ipynb to generate .db from .csv
queryNOAA.py and queryUSGS.py are called by .ipynb to access APIs for up-to-date data. 

## How to run:
In terminal: 
```
pip install -r requirements.txt
```

### Run website locally
In terminal: 
```
datasette macroinvertebrates.db 
```
> returns a link to open in browser

Ctrl+C in terminal to open website

### Run website locally on root account 
root account has permission to make edits and view more information than non-root 

In terminal: 
```
datasette macroinvertebrates.db --root
```
> returns a link to open in browser

## Updating information
To access updated information from NOAA and USGS, run queryNOAA.py  and queryUSGS.py from .ipynb

To update .csv files, drag new .csv files with the same formatting and titles into the file save space. Replace. All previously updated information is saved in the .db file. Any duplicate rows will not be added. 

## Variables

### Environmental Data 

[Variable descriptions on GitHub](https://github.com/marneypratt/macroS26/blob/main/data/env_metadata.txt)


- Year
- Season
- Location
- sampleID
- Microhabitat
- Mon.precip
- mon.ADD
- Mon.max.discharge
- Mon.median.discharge
- Mon.max.turb 
- Mon.median.turb 
- mon.max.wTemp
- mon.median.wTemp
- Depth
- Per_sediment 
- Per_rock
- Per_organic
- pH
- wTemp
- DO
- Light
- Flow
- Turb
- Cond
- Nitrate
- Alkalinity
- winter.sediment

### Macroinvertebrate Data

[Variable descriptions on GitHub](https://github.com/marneypratt/macroS26/blob/main/data/macros_metadata.txt )


- date
- year
- season
- location
- sampleID
- microhabitat
- ScientificName
- stage
- number
- benthicArea
- invDens


### Master Taxa Information (information on the taxonomy of each species)

[Variable descriptions on GitHub](https://github.com/marneypratt/macroS26/blob/main/data/master.taxa_metadata.txt)


- acceptedTaxonID
- taxonRank
- scientificName
- taxon_group
- phylum
- species
- taxa.notes
- tolerance
- FFG
- FFG2


### Water Quality Data

[Variable descriptions on GitHub](https://github.com/marneypratt/macroS26/blob/main/data/waterQ_metadata.txt)

- Date
- Year
- Season
- Location
- sampleID
- startTime
- dateTime.utc
- Microhabitat
- Quadrat
- Depth
- pH
- Wtemp
- DO (dissolved oxygen)
- Light
- Flow
- Turb
- Cond
- Nitrate
- Alkalinity

## USGS Data 

[Data from USGS](https://waterdata.usgs.gov/monitoring-location/USGS-01171500/#dataTypeId=continuous-00060-0&period=P7D&showFieldMeasurements=true)


- Gage height
- Discharge

## NOAA Data

[Monthly total precipitation](https://www.ncdc.noaa.gov/data-access/land-based-station-data/land-based-datasets/global-historical-climatology-network-ghcn)

[Monthly aggregated degree days](https://www.ncdc.noaa.gov/data-access/land-based-station-data/land-based-datasets/global-historical-climatology-network-ghcn)



For more information on the methods, please refer to [Marney’s original documentation](https://github.com/marneypratt/macroS26/blob/main/data/env_metadata.txt).


## Demo
[Here is a link to our demo](https://drive.google.com/drive/u/0/folders/1mwbfIHmfpJzZUxMPEK6IgFEVvnkpq9iM).

## Reflection

Our project processes macroinvertebrate and environmental data collected by Professor Marney Pratt. It uses Python to query and collect data from USGS and NOAA to facilitate the addition of environmental data to the database. It additionally uses a SQLite schema to store, organie, and verify the data. We additionally used Datasette to present the data and facilitate the downloading of CSVs for Biology and Statistics students. 

A key challenge for us was creating a schema that not only represented the existing data, but that will be able to represent future data collection methods and seasons. This required us to be very careful and intentional about the data and the stakeholders' future plans and goals. Another challenge was implementing APIs that fetch data from other sources to add to the data collected by Marney Pratt and students. By using `requests`, we overcame this challenge and are able to pull data from USGS and NOAA.
