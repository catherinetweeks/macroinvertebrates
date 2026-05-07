import pandas as pd
import requests
import json
import sqlite3
import queryUSGS as q
import queryNOAA as n
import time

DB_PATH = "macroinvertebrates.db"

conn = sqlite3.connect(DB_PATH)
conn.execute("PRAGMA foreign_keys = ON")

""""
Recreates database tables.
"""
def create_tables(conn):
    
    cur = conn.cursor()

    # DELETE LATER: USED FOR DEBUGGING
    # cur.executescript("""
    # DROP TABLE IF EXISTS Year;
    # DROP TABLE IF EXISTS Date;
    # DROP TABLE IF EXISTS Sample;
    # DROP TABLE IF EXISTS Macroinvertebrate;
    # DROP TABLE IF EXISTS Taxonomy;
    # """)

    cur.executescript("""

    CREATE TABLE Year (
        year INT CHECK(year >= 2019),
        winterSediment REAL,
        PRIMARY KEY(year)
    );
        
    CREATE TABLE Date (
        date VARCHAR(5),   
        startTime TEXT,
        year INT,
        monthlyAveragePrecipitation REAL,
        maxDischarge REAL,
        medianDischarge REAL,
        discharge REAL,
        gageHeight REAL,
        aggregatedDegreeDays REAL,
        maxTurb REAL,
        medianTurb REAL,
        maxWaterTemp REAL,
        medWaterTemp REAL,
        season TEXT CHECK(season=='Spring' OR season=='Fall' OR season=='Summer' OR season==NULL),
        PRIMARY KEY(date, startTime),
        FOREIGN KEY(startTime) REFERENCES Sample(startTime),
        FOREIGN KEY(year) REFERENCES Year(year)
    );

        
    CREATE TABLE Sample (
        sampleID VARCHAR(12),  
        date VARCHAR(5), 
        year INT,
        startTime TEXT, 
        sampleMethod TEXT,
        quadrat REAL,
        location TEXT CHECK(location=='Upstream' OR location =='Downstream'),
        microhabitat TEXT CHECK(microhabitat == 'DSR' OR microhabitat == 'DSP' OR microhabitat == 'DFR' OR microhabitat == 'DM' OR microhabitat ==  'DSH' OR microhabitat == 'USR' OR microhabitat == 'UFR' OR microhabitat == 'UM' OR  microhabitat == 'USH' OR microhabitat == 'USU' OR microhabitat == NULL),
        waterDepth REAL,
        percentSediment REAL,
        percentRock REAL CHECK (percentRock >= 0 AND percentRock <= 100),
        percentOrganic REAL CHECK (percentOrganic>=0 AND percentOrganic <= 100),
        pH REAL CHECK (pH >= 0 AND pH <= 14),
        waterTemp REAL,
        dissolvedO2 REAL,
        light REAL,
        flow REAL,
        turb REAL, 
        conductivity REAL, 
        nitrate REAL,
        alkalinity INT,
        PRIMARY KEY(sampleID, startTime, quadrat),
        FOREIGN KEY(date) REFERENCES Date(date)
    );

    CREATE TABLE Macroinvertebrate (
        scientificName TEXT,  
        sampleID VARCHAR(12),
        quadrat REAL,
        stage REAL CHECK(stage == 'larva' OR stage == 'pupa' OR stage == 'adult'),
        numOrganismsFound INT CHECK (numOrganismsFound >= 0),
        benthicArea REAL,
        invertebrateDensity REAL,
        PRIMARY KEY(scientificName, sampleID, quadrat),
        FOREIGN KEY(sampleID) REFERENCES Sample(sampleID)
        FOREIGN KEY(quadrat) REFERENCES Sample(quadrat)
    );

    CREATE TABLE Taxonomy (
        taxonID VARCHAR(6) UNIQUE,      
        scientificName TEXT UNIQUE,
        taxonRank TEXT,
        taxgroup TEXT,
        phylum TEXT,
        subphylum TEXT,
        class TEXT,
        taxOrder TEXT,
        family TEXT,
        subfamily TEXT,
        tribe TEXT,
        genus TEXT,
        taxaNotes TEXT, 
        tolerance INT,
        ffg VARCHAR(3) CHECK(ffg == 'cf' OR ffg == 'cg' or ffg =='om' OR ffg == 'prc' OR ffg == 'prd' OR ffg == 'scr' OR ffg == 'sh'), 
        ffg2 VARCHAR(3) CHECK(ffg2 == 'cf' OR ffg2 == 'cg' or ffg2 =='om' OR ffg2 == 'prc' OR ffg2 == 'prd' OR ffg2 == 'scr' OR ffg2 == 'sh' OR ffg2 == NULL),
        PRIMARY KEY(taxonID),
        FOREIGN KEY(scientificName) REFERENCES Macroinvertebrate(scientificName)
    );
 """)

    conn.commit()


''' 
Searches for files by the names of env.csv, macros.csv, master.taxa.csv, and waterQ.csv. Inserts data into database. 
'''
def add_data(conn, cur):
    print('Reading in .csv files...')

    try:
        env_df = pd.read_csv("env.csv")
        print('read in env.csv')
    except:
        print("env.csv not found") 

    try:
        macro_df = pd.read_csv("macros.csv")
        print('read in macros.csv')
    except:
        print("macros.csv not found") 

    try:
        taxa_df = pd.read_csv("master.taxa.csv")
        print('read in master.taxa.csv')
    except:
        print("master.taxa.csv not found") 

    try:
        water_quality_df = pd.read_csv("waterQ.csv")
        print('read in waterQ.csv')
    except:
        print("waterQ.csv not found") 
    
    env_df = pd.DataFrame(env_df)
    env_df.rename(columns = {
        'mon.precip' : 'monthlyAveragePrecipitation',
        'mon.ADD' : 'aggregatedDegreeDays',
        'mon.max.discharge' : 'maxDischarge',
        'mon.median.discharge' : 'medianDischarge',
        'mon.max.turb' : 'maxTurb',
        'mon.median.turb' : 'medianTurb',
        'mon.max.wTemp' : 'maxWaterTemp',
        'mon.median.wTemp' : 'medWaterTemp',
        'per_sediment' : 'percentSediment',
        'winter.sediment' : 'winterSediment',
        'per_rock' : 'percentRock',
        'per_organic' : 'percentOrganic',
        'wTemp': 'waterTemp',
        'DO' : 'dissolvedO2',
        'cond' : 'conductivity',
        'depth' : 'waterDepth'
    }, inplace = True)

    macro_df = pd.DataFrame(macro_df)
    macro_df.rename(columns = {
        'number' :'numOrganismsFound',
        'invDens' : 'invertebrateDensity'
    }, inplace = True)


    taxa_df = pd.DataFrame(taxa_df)
    taxa_df.rename(columns = {
        'taxon_group' :'taxgroup',
        'acceptedTaxonID' : 'taxonID',
        'taxa.notes' : 'taxaNotes',
        'order' : 'taxOrder',
        'FFG' : 'ffg',
        'FFG2' : 'ffg2'
    }, inplace = True)
    

    water_quality_df = pd.DataFrame(water_quality_df)
    water_quality_df.rename(columns = {
        'depth' : 'waterDepth',
        'wTemp' : 'waterTemp',
        'DO': 'dissolvedO2',
        'cond': 'conductivity'
    }, inplace = True)

    year_subtable = env_df[['year','winterSediment']].sort_values(by='winterSediment').drop_duplicates().loc[(env_df != 0).all(1)]

    taxa_subtable = taxa_df[['taxonID', 'scientificName', 'taxonRank','taxgroup','phylum', 'subphylum','class','taxOrder', 'family','subfamily','tribe', 'genus','taxaNotes', 'tolerance', 'ffg', 'ffg2']]

    # date_subtable = env_df[['date','year','monthlyAveragePrecipitation','maxDischarge','medianDischarge','aggregatedDegreeDays','maxTurb','medianTurb','maxWaterTemp', 'medWaterTemp','season']].drop_duplicates()
   
    # # Add discharge and gageHeight to date
    # discharge = []
    # for i, row in date_subtable.iterrows():
    #     date = row['date']
    #     print(date)
    #     value = q.get_discharge(date) 
    #     print(value)  
    #     discharge.append(value)
    
    # print('exiting discharge for loop')
    # date_subtable['discharge'] = discharge
    # print('added discharge to date subtable.')

    # gageHeight = []
    # for i, row in date_subtable.iterrows():
    #     date = row['date']
    #     print(date)
    #     value = q.get_gage_Height(date)
    #     print(value)
    #     gageHeight.append(value)

    # print('exiting gageHeight for loop')
    # date_subtable['gageHeight'] = gageHeight
    # print('added gageHeight date subtable.')


    # #Add monthly precipitation and monthly aggregrated degree days from NOAA
    # mon_prcp = []
    # for i, row in date_subtable.iterrows():
    #     if i % 5 == 0: # Every 5 calls take break
    #         time.sleep(3)
    #     date = row['date']
    #     print(date)
    #     value = n.get_mon_prcp(date)
    #     print(value)
    #     mon_prcp.append(value)

    # print('exiting mon_prcp for loop')
    # date_subtable['monthlyAveragePrecipitation'] = mon_prcp
    # print('added mon_prcp date subtable.')

    # mon_ADD = []
    # for i, row in date_subtable.iterrows():
    #     if i % 5 == 0: # Every 5 calls take break
    #         time.sleep(3)
    #     date = row['date']
    #     print(date)
    #     value = n.get_mon_add(date)
    #     print(value)
    #     mon_ADD.append(value)
    
    # print('exiting mon_add for loop')
    # date_subtable['aggregatedDegreeDays'] = mon_ADD
    # print('added mon_add date subtable. ')

    # date_subtable.to_csv("date_subtable.csv")

    merged_df = water_quality_df.join(env_df.set_index('sampleID'), on='sampleID', how='outer', lsuffix='_wq', rsuffix='_env')
    merged_df.reset_index(inplace = True)
    
    sample_subtable = merged_df[['sampleID', 'year_wq', 'startTime', 'location_wq','microhabitat_wq','waterDepth_wq', 'percentSediment','percentRock','percentOrganic','pH_wq','waterTemp_wq','dissolvedO2_wq', 'light_wq', 'flow_wq', 'turb_wq','conductivity_wq','nitrate_wq','alkalinity_wq', 'quadrat']]

    macros_subtable = macro_df[['scientificName', 'sampleID', 'stage', 'numOrganismsFound', 'benthicArea','invertebrateDensity']]

    try:
        cur.executemany(
                'INSERT INTO "Macroinvertebrate" ("scientificName", "sampleID","stage", "numOrganismsFound","benthicArea","invertebrateDensity") VALUES (?, ?, ?, ?, ?, ?);', macros_subtable.values.tolist()
        )
    except:
        print('Issue inserting into Macroinvertebrate table.')
    try:
        cur.executemany(
                'INSERT INTO "Taxonomy" ("taxonID", "scientificName", "taxonRank","taxgroup","phylum", "subphylum","class","taxOrder", "family","subfamily","tribe", "genus","taxaNotes", "tolerance", "ffg", "ffg2") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);', taxa_subtable.values.tolist()
        )
    except:
        print('Issue inserting into Taxonomy table.')

    try:
        cur.executemany(
                'INSERT INTO "Sample" ("sampleID", "startTime", "year", "location","microhabitat","waterDepth", "percentSediment","percentRock","percentOrganic","pH","waterTemp","dissolvedO2", "light", "flow", "turb","conductivity","nitrate","alkalinity", "quadrat") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);', sample_subtable.values.tolist()
        )
    except:
        print('Issue inserting into Sample table.')

    try:
        cur.executemany(
                'INSERT INTO "Date" ("date","year","monthlyAveragePrecipitation","maxDischarge","medianDischarge","discharge", "gageHeight","aggregatedDegreeDays","maxTurb","medianTurb","maxWaterTemp", "medWaterTemp","season") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);', date_subtable.values.tolist()
        )
    except:
        print('Issue inserting into Date table.')

    try:
        cur.executemany(
            'INSERT INTO "Year" ("year", "winterSediment") VALUES (?, ?);', year_subtable.values.tolist()
        )
    except:
         print('Issue inserting into Year table.')
    print('Committing changes to database.')

    conn.commit()

"""
DELETE ADD TO DATE LATER: USED FOR DEBUGGING
"""
# def add_to_date(conn, cur):
#     date_subtable = pd.read_csv("date_subtable.csv")
#     date_subtable = pd.DataFrame(date_subtable)
#     date_subtable = date_subtable.drop('Unnamed: 0', axis=1)
#     # print(date_subtable.columns)
#     cur.executemany(
#             'INSERT INTO "Date" ("date","year","monthlyAveragePrecipitation","maxDischarge","medianDischarge","discharge", "gageHeight","aggregatedDegreeDays","maxTurb","medianTurb","maxWaterTemp", "medWaterTemp","season") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);', date_subtable.values.tolist()
#     )
#     conn.commit()




def run_sql(sql: str):
    try:
        cur = conn.execute(sql)
        if sql.lstrip().upper().startswith(("SELECT", "PRAGMA")):
            rows = cur.fetchall()
            print(rows)
        else:
            conn.commit()
            print("OK")
    except sqlite3.Error as err:
        print(f"SQLite error: {err}")

def main():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    # create_tables(conn)
    # add_data(conn, cur)

    ## DELETE LATER: USED FOR DEBUGGING
    # add_to_date(conn, cur) 

    # run_sql('SELECT * FROM DATE LIMIT 20')
    conn.commit()
    
if __name__ == "__main__":
    main()