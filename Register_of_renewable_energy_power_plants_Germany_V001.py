
# coding: utf-8

# # Register of renewable energy power plants in Germany
# 
# This is a Jupyter Notebook that downloads and cleans up the data from the project [EnergyMap.info](http://www.energymap.info/) and  the German Federal Network Agency for Electricity, Gas, Telecommunications, Posts and Railway [BNetzA](http://www.bundesnetzagentur.de/). EnergyMap.info provides a register of all renewable energy power plants in Germany.
# 
# Since 2014 the BNetzA is responsible to publish the register of renewable power plants due to the [EEG 2014 (German)](http://www.gesetze-im-internet.de/eeg_2014/) [(English)](http://www.res-legal.eu/search-by-country/germany/single/s/res-e/t/promotion/aid/feed-in-tariff-eeg-feed-in-tariff/lastp/135/). Note: From June 2014 on all power plants are published in two seperated MS Excel-files for roof mounted PV systems and all other renewable power plants.
# 
# The register includes all RE power plants which are eligible for the German feed-in tariff (according to the EEG law). EnergyMap.info collects all data which is mandatorily reported from the four German TSO's to the BNetzA and merges it. Additionally EnergyMap.info validates and converts the data to a standard format.
# 
# 

# # License
# 
# * This notebook is published under the GNU GPL v3 license. http://www.gnu.org/licenses/gpl-3.0.en.html.
# * This notebook is developed by Wolf-Dieter Bunke [(E-Mail)](mailto:wolf-dieter.bunke@uni-flensburg.de)

# # Table of contents 
# 
# * [Register of renewable energy power plants in Germany](#Register-of-renewable-energy-power-plants-in-Germany)
# * [License](#Licence)
# * [1. Import python modules](#1.-Import-python-modules)
#      * [1.1 First Data overview of EnergyMap.info](#1.1-First-Data-overview-of-EnergyMap.info)
# * ...
# * [7 Documenting the data package in a JSON object](#7-Documenting-the-data-package-in-a-JSON-object)
# * [8 Write Data Package to disk](#8-Write-Data-Package-to-disk)
# 

# # 1. Import Python modules

# In[1]:

import pandas as pd
import numpy as np
import zipfile
import requests
import io

# Matplotlib
get_ipython().magic('matplotlib inline')


# 
# ## 1.1 Data overview from EnergyMap.info
# 
# * Data discription from source: http://www.energymap.info/download/
# * Download from: http://www.energymap.info/download/eeg_anlagenregister_2015.08.utf8.csv.zip
#     * Last Dataset: 08.2015
#     * Number of entries: 1.565.438 
#     * File sides: 363,9 MB

# ##### Please note: Since the last change in the EEG law in 2014, three out of four German transmission network operators (TSO) stopped reporting
# 
# * **Report status by TSO:**
#     * TenneT TSO GmbH:           still reporting, last reported entries 2015-08-17
#     * 50Hertz Transmission GmbH: last report 2014-11-26
#     * Amprion GmbH:              last report 2014-10-09
#     * TransnetBW GmbH:           last report 2014-11-24
# 
# * **###### Concequence:** ???

# ## 1.2 Data overview from other data sources
# 
# German Federal Network Agency for Electricity, Gas, Telecommunications, Posts and Railway (BNetzA) renewable Power plant register ("Anlagenregister"): [PV](http://www.bundesnetzagentur.de/SharedDocs/Downloads/DE/Sachgebiete/Energie/Unternehmen_Institutionen/ErneuerbareEnergien/Photovoltaik/Datenmeldungen/Meldungen_Aug-Juni2015.xls?__blob=publicationFile&v=1) and [other renewables](http://www.bundesnetzagentur.de/SharedDocs/Downloads/DE/Sachgebiete/Energie/Unternehmen_Institutionen/ErneuerbareEnergien/Anlagenregister/VOeFF_Anlagenregister/2015-07_Veroeff_AnlReg.xls?__blob=publicationFile&v=1) renewable energy power plants, provided by the BNetzA.
# 
# * EUROSTAT
# * [Netztransparenz](https://www.netztransparenz.de/de/Anlagenstammdaten.htm), Download: [zip-File](https://www.netztransparenz.de/de/file/UeNB-EEG-Anlagenstammdaten_2013.zip)
# * German TSO's
#     * 50Hertz
#     * Amprion
#     * TenneT
#     * TransnetBW

# # 2. Extracting data from EnergyMap.info
# 
# In the beginning we using EnergyMap.info for all historical data.

# ## 2.1 Download, unzip and load EnergyMap.info-CSV as data frame
# 
# We are creating a [pandas DataFrame](http://pandas.pydata.org/pandas-docs/stable/dsintro.html#dataframe) in order to handle our data.
# 
# --> Time for loading data: approx. 5-10 min.

# In[2]:

# Definint URL to energymap.info
url_energymap = 'http://www.energymap.info/download/eeg_anlagenregister_2015.08.utf8.csv.zip'
r = requests.get(url_energymap)
z = zipfile.ZipFile(io.BytesIO(r.content))


# In[3]:

# Creating data frame from energyMap.info data
# time: approx. 5-10 min
eeg_data = pd.read_csv(z.open('eeg_anlagenregister_2015.08.utf8.csv'),
                           sep=';',
                           header=None,
                           names=None,
                           parse_dates=[0],
                           dayfirst=True,
                           comment='#',
                           low_memory = False)


# ## 2.2 Definition of column names
# 
# Here we translate the original column names from EnergyMap.info from German to English. The new English column names are assigned to our data frame.
# 
# Original Name|Translation|column name
# -|-|-
# Inbetriebnahmedatum|start-up date|start_up_date
# GeoDBID| Geometry id | gid 
# PLZ | post code or ZIP|postcode
# Ort| name od city, vilage, municipality|	city
# Strasse| street name and hous number|street_address
# Anlagenschluessel| power plant indificator number|power_plant_id
# Anlagentyp| Type of generation|	type_of_generation
# Anlagenuntertyp| Sub type of generation|subtype
# Nennleistung(kWp_el)| rated power |	rated_power
# Einspeisespannungsebene| Type of grid connection, voltage level|voltage_level
# DSO-EIC| Energy Identification Code (EIC) for distribution system operator (DSO) accounting area  |dso_eic
# DSO| Name of distribution system operator|dso
# TSO-EIC| Energy Identification Code (EIC) for transmission system operator (TSO)| tso_eic
# TSO	| Name of TSO|tso
# kWh(2013)| Annual power production of the year 2013| kwh2013
# kWh(average)|Average power production|	kwh_avg
# kWh/kW| Own calculation of EnergyMap of full-load hours |kwh_per_kw
# EEG-Verguetungsschluessel|German EEG renumeration code	|eeg_renumeration_code
# Gemeindeschluessel|	Municipality code of Germany | municipality_id
# GPS-Lat| GPS Latetude coordinats| gps_lon
# GPS-Lon| GPS Longetude coordinats|gps_lat
# GPS-Genauigkeit(dm)| GPS accuracy of coordinats| gps_accuracy
# Validierung| Data validation| validation

# In[4]:

# set new column names 
eeg_data.columns = ['start_up_date', 'gid', 'postcode', 'city','street_address','power_plant_id',
                        'type_of_generation','subtype','rated_power','voltage_level','dso_eic','dso','tso_eic',
                        'tso','kwh2013','kwh_avg','kwh_per_kw','eeg_renumeration_code','municipality_id',
                        'gps_lon','gps_lat','gps_accuracy','validation']


# ## 2.3  First look at the data frame (structure and format)
# 
# Here we look at the created data frame and the data formats of the different columns:

# In[5]:

eeg_data.dtypes


# Since "object"-types cannot be calculated they have to be converted to "float"-types.

# ### 2.3.1 Data type adjustment and first validation
# 
# We need to change the data type from "object" to "float" for the following columns:
# * rated_power
# * kwh2013
# * kwh_avg
# * gps_lon
# * gps_lat

# '#### Erklärender Satz zu Komma -> Punkt

# In[7]:

# replace comma with dots for gps_lon and lat
eeg_data['gps_lon'] = eeg_data['gps_lon'].str.replace(',', '.')
eeg_data['gps_lat'] = eeg_data['gps_lat'].str.replace(',', '.')


# In[8]:

# change data type from object to float 
eeg_data['gps_lon'] = eeg_data['gps_lon'].astype('float64')
eeg_data['gps_lat'] = eeg_data['gps_lat'].astype('float64')


# Convert the record_id field from an integer to a float
# 
# ```python
# eeg_data['rated_power']  = eeg_data['rated_power'].astype('float64')
# ...
# ValueError: could not convert string to float: '349,005'
# # 1565437
# ```

# In[9]:

# take a look 
eeg_data.head()


# In[10]:

eeg_data.tail()


# ### 2.3.2 Delete data entires which are not part of the register
#     (i.e. obviously wrong)

# In[11]:

# delete rows where postcode is like 99999
eeg_data = eeg_data.drop(eeg_data[eeg_data['postcode'].str.contains("99999")].index)


# In[12]:

# replace dots and change comma into dots
eeg_data['rated_power'] = eeg_data['rated_power'].str.replace('.', '')
eeg_data['rated_power'] = eeg_data['rated_power'].str.replace(',', '.')


# In[13]:

# change type
eeg_data['rated_power'] = eeg_data['rated_power'].astype('float64')


# In[14]:

# sum in Gigawatt 
eeg_data['rated_power'].sum()/1000000


# In[15]:

# sum in Gigawatt with validation OK
eeg_data[eeg_data['validation']=='OK'].sum()['rated_power']/1000000


# In[16]:

eeg_data['rated_power'].describe()


# In[17]:

# group by type in MW
eeg_data.groupby(['type_of_generation'])['rated_power'].sum()/1000


# In[18]:

eeg_data.groupby(['start_up_date'])['rated_power'].sum()/1000


# In[19]:

# remove dots
eeg_data['kwh_avg'] = eeg_data['kwh_avg'].str.replace('.', '')
eeg_data['kwh2013'] = eeg_data['kwh2013'].str.replace('.', '')


# In[20]:

# remove comma with dots
eeg_data['kwh_avg'] = eeg_data['kwh_avg'].str.replace(',', '.')
eeg_data['kwh2013'] = eeg_data['kwh2013'].str.replace(',', '.')


# In[21]:

# change type
eeg_data['kwh_avg'] = eeg_data['kwh_avg'].astype('float64')
eeg_data['kwh2013'] = eeg_data['kwh2013'].astype('float64')


# ### 2.3.3 Strange date
# 
# * ToDo:
#      * e.g. 2046-09-27, 1895-11-16 
#      * ...
# 

# ##  2.4 Translation of type and subtype
# 
# ### 2.4.1 types
# 
# type_of_generation| OPSD naming
# -|-
# Gas | gas
# Erdwärme| geothermal
# Wasserkraft| hydro
# Windkraft|wind 
# Biomasse|biomass 
# Solarstrom| solar

# In[22]:

# replace names
eeg_data['type_of_generation'] = eeg_data['type_of_generation'].str.replace('Gas', 'gas').replace('Erdwärme', 'geothermal').replace('Wasserkraft', 'hydro').replace('Windkraft', 'wind').replace('Biomasse', 'biomass').replace('Solarstrom', 'solar')
# get an overview
eeg_data.groupby(['type_of_generation'])['rated_power'].agg(['sum', 'count'])


# ### 2.4.2 Subtypes
# 
# subtype| OPSD naming
# -|-
# Altholz|waste_wood 
# Biogas|biogas 
# Biogas (Gasnetzentnahme)|biogas_gas_grid 
# Biogas (Trockenfermentation)|biogas_dry_fermentation
# Biotreibstoffe|biofuel 
# Deponiegas|landfill_gas 
# Freifläche|ground_mounted 
# Gebäude|roof_mounted 
# Grubengas|mine_gas 
# Holz| wood
# Klärgas| sewage_gas
# Offshore|offshore 
# Onshore|onshore

# In[23]:

# replace names
eeg_data['subtype'] = eeg_data['subtype'].str.replace('Onshore', 'onshore').replace('Offshore', 'offshore').replace('Klärgas', 'sewage_gas').replace('Holz', 'wood').replace('Grubengas', 'mine_gas').replace('Gebäude', 'roof_mounted').replace('Freifläche', 'ground_mounted').replace('Deponiegas', 'landfill_gas').replace('Biotreibstoffe', 'biofuel').replace('Biogas (Trockenfermentation)', 'biogas_dry_fermentation').replace('Altholz', 'waste_wood ').replace('Biogas (Gasnetzentnahme)', 'biogas_gas_grid').replace('Biogas', 'biogas')
# get an overview
eeg_data.groupby(['subtype'])['rated_power'].agg(['sum', 'count'])


# ## 2.5  Overview of the first result

# In[24]:

# plot 
eeg_data['rated_power'].plot() 


# ## 2.6 Take a look into the statistics of BNetzA

# In[25]:

# get statistics  
url_eeg2013 ='http://www.bundesnetzagentur.de/SharedDocs/Downloads/DE/Sachgebiete/Energie/Unternehmen_Institutionen/ErneuerbareEnergien/ZahlenDatenInformationen/EEGinZahlen_2013.xls;?__blob=publicationFile&v=3'
eeg2013  =pd.ExcelFile(url_eeg2013)
eeg2013.sheet_names


# In[26]:

sta2013 = eeg2013.parse('2.1 Überblick Deutschland', skiprows=3, skip_footer=9)
sta2013


# ### TODO: 
# * sum by year and type
# * calc error of missing rated power e.g.
# * ...

# # 3 Get new data from BNetzA
# 
# * Introduction ...
# 
# 
# ## 3.1 Download BNetzA register #1
# 
# Note: Here dataset without roof-mounted PV systems. (For dataset of roof-mounted PV systems see [3.2](#Download-PV-roof-mounted-master-data-register-from-BNetzA))

# In[27]:

# set URL
url_bna1 ='http://www.bundesnetzagentur.de/SharedDocs/Downloads/DE/Sachgebiete/Energie/Unternehmen_Institutionen/ErneuerbareEnergien/Anlagenregister/VOeFF_Anlagenregister/2015_08_Veroeff_AnlReg.xls?__blob=publicationFile&v=1'
xl  =pd.ExcelFile(url_bna1)
xl.sheet_names


# In[28]:

# create data frame
bnetza1 = xl.parse("Gesamtübersicht")


# In[ ]:

# overview of columns
list(bnetza1.columns)


# In[29]:

# count number of columns
bnetza1.dtypes.count()


# ## 3.2 Download BNetzA register #2: roof-mounted PV

# In[30]:

# get PV data
file_bnetza_pv = '/home/leppi/Dokumente/ZNES/OPSD/JupitaDataExtraxtion/EEG-Anlagen/Rohdaten/DE/Meldungen_Aug-Juni2015.xls'
pv = pd.ExcelFile(file_bnetza_pv)
# overview of excel sheets
pv.sheet_names


# In[31]:

# create one data frame
book = pv.sheet_names
pvdf  = pd.DataFrame()
#
for sheet in book:
    data= pv.parse(sheet, skiprows=10)
    pvdf = pvdf.append(data)
    print(sheet)


# In[32]:

# count total entries
pvdf.count()


# In[33]:

# drop NULL "Unnamed:" column
pvdf= pvdf.drop(pvdf.columns[[7]], axis=1)


# ### 3.2.1 Rename columns of  PV roof mounted data
# 
# Original Name|Translation|column name
# -|-|-
# Anlage \nBundesland|federal state|federal_state
# Anlage \nOrt oder Gemarkung |Place, city  | city
# Anlage \nPLZ | post code or ZIP| postcode
# Anlage \nStraße oder Flurstück *)| street name and hous number|	street_address
# Inbetriebnahmedatum \**)| Start-up date|start_up_date
# Installierte \nNennleistung [kWp] | installed rated power |	rated_power
# Meldungsdatum | notification date | notification_date 
# 
# 

# In[34]:

pvdf.columns = ['federal_state', 'city', 'postcode','street_address', 'start_up_date', 'rated_power', 'notification_date']


# In[35]:

# take a look into the structure and format
pvdf.dtypes


# ## 3.3 Merge data sources
# 
# until August 2014:
# * EnergyMap: data on (all) renewable energy power plants
# 
# since August 2014:
# * BNetzA #1: data on all renewable energa power plants (except roof-mounted PV)
# * BNetzA #2: data on roof-mounted PV only

# In[36]:

#
energymap_pv = eeg_data[eeg_data['subtype'] == 'roof_mounted']
energymap_pv.count()


# ### 3.3.1 Marker for data source

# In[37]:

#
frames = [energymap_pv, pvdf]
# key is an marker x = EnergyMap y = BNetzA
result_pv = pd.concat(frames, keys=['x', 'y'])


# In[38]:

# Overview
result_pv.count()


# In[39]:

# Delete not needed columns
opsd_pv = result_pv.loc[:,['start_up_date','rated_power','federal_state','city','postcode','street_address','gps_lat','gps_lon','gps_accuracy','validation']]
opsd_pv.reset_index(drop=True)


# In[40]:

# PV roof mounted systems in GW
opsd_pv.rated_power.sum()/1000000


# # 4 Geoplot testing
# 
# 

# In[41]:

import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
# Function to map Germany
def draw_DE():
    """initialize a basemap centered on Germany"""
    plt.figure(figsize=(14, 10))
    return Basemap(projection='lcc', resolution='l',
                   llcrnrlon= 5.87, urcrnrlon=16.04,
                   llcrnrlat= 47, urcrnrlat= 55.1,
                   lat_1=47.26, lat_2=56, lon_0=6,
                   area_thresh=10000)


# In[42]:

# Create map
m = draw_DE()
# Draw map background
m.fillcontinents(color='white', lake_color='#eeeeee')
m.drawstates(color='lightgray')
m.drawcoastlines(color='lightgray')
m.drawcountries(color='lightgray')
m.drawmapboundary(fill_color='#eeeeee')

# get gps data
lon = np.array(opsd_pv.gps_lon)
lat = np.array(opsd_pv.gps_lat)

# Plot PV systems entries
style = dict(s=5, marker='o', alpha=0.5, zorder=2)
m.scatter(lat,lon, latlon=True, label='PV roof mounted systems', color='#00592D', **style)

plt.legend(loc='lower left', frameon=False)


# # 5 Georeferencing of missing GPS lon and lat
# 
# 
# -- http://wiki.openstreetmap.org/wiki/Nominatim 
# 
# -- https://github.com/damianbraun/nominatim
# 
# -- https://pypi.python.org/pypi/geopy

# In[43]:

# count missing geo data
opsd_pv.gps_lon.isnull().sum()


# ## Evaluation of our data
#  
# For our evaluation of the data set we use different methods. 
# 
# 1. count entries
# 2. sum the installed capacity by generation type
# 3. check date, Types, adresses, lon lat
# 4. ...
# 

# # 6 Validation column 
# 
# List of methods. Each Method error get one number e.g. 
# 
# Number | Method
# -|-
# 1 | state_up_date < 1900
# ...| ...

# # ...

# # 7 Documenting the data package (meta data)
# 
# We document the data packages meta data in the specific format JSON as proposed by the Open Knowledge Foundation. See the Frictionless Data project by OKFN (http://data.okfn.org/) and the Data Package specifications (http://dataprotocols.org/data-packages/) for more details.

# In[44]:

from collections import OrderedDict
import json

# Here we define meta data of the resulting data package.
# The meta data follows the specification at:
# http://dataprotocols.org/data-packages/
dataPackageSpec = {
    "name": "opsd-renewable-master-register-germany",
    "title": "Test data for master data register of roof mounted pv stystem in Germany.",
    "description": "This dataset is just for OPSD testing and contains the master data of Germany. For the beginning we are using the EnergyMap.info data set and BNetzA publications of pv master data.",
    "version": "0.0.1",
    "keywords": ["master data register","power plants","solar","roof mounted PV stystem","renewables","germany"],
    "resources": [
        {
            "path": "register_data_roof_mounted_pv_germany.csv",
#            "url": "online url",
            "format": "csv",
            "mediatype": "text/csv",
            "schema": {
                # Schema according to: http://dataprotocols.org/json-table-schema/
                "fields": [
                    {
                        "name": "start_up_date",
                        "description": "Date of start up.",
                        "type": "datetime",
                        "format": "YYYY-MM-DDThh:mm:ssZ" # This MUST be in ISO 8601 format of YYYY-MM-DDThh:mm:ssZ in UTC time according to http://dataprotocols.org/json-table-schema/ 
                    },
                    {
                        "name": "rated_power",
                        "description": "Rated power of the roof mounted PV stystem in kW",
                        "type": "number"
                    },
                    {
                        "name": "federal_state",
                        "description": "Name of federal state of PV system location",
                        "type": "number"
                    },
                    {
                        "name": "city",
                        "description": "Name of city of PV system location",
                        "type": "text"
                    },
                    {
                        "name": "postcode",
                        "description": "Post code of PV system location",
                        "type": "number"
                    },
                    {
                        "name": "street_address",
                        "description": "Name of street and house number of PV system location",
                        "type": "text"
                    },
                    {
                        "name": "gps_lat",
                        "description": "GPS Latitude coordinates of PV system location",
                        "type": "number"
                    },
                    {
                        "name": "gps_lon",
                        "description": "GPS Longitude coordinates of PV system location",
                        "type": "number"
                    },
                    {
                        "name": "gps_accuracy",
                        "description": "GPS accuracy in meters",
                        "type": "number"
                    },
                    {
                        "name": "validation",
                        "description": "Validation OK or comment for validation error. From EnergyMap.info",
                        "type": "text"
                    }                    
                  # add more  columns
                ]
            }
        }
    ],
    "licenses": [
        {
            "url": "http://example.com/license/url/here",
            "name": "License Name Here",
            "version": "1.0",
            "id": "license-id-from-open"
        }
        
    ],
    "sources": [
        {
            "name": "EnergyMap.info",
            "web": "http://www.energymap.info/download.html"
        },
        {
            "name": "Bundesnetzagentur - Veröffentlichung von im Anlagenregister registrierten Daten",
            "web": "http://www.bundesnetzagentur.de/cln_1422/DE/Sachgebiete/ElektrizitaetundGas/Unternehmen_Institutionen/ErneuerbareEnergien/Anlagenregister/Anlagenregister_Veroeffentlichung/Anlagenregister_Veroeffentlichungen_node.html"
        },
        {
            "name": "Bundesnetzagentur - Datenmeldungen und EEG-Vergütungssätze für Photovoltaikanlagen",
            "web": "http://www.bundesnetzagentur.de/cln_1431/DE/Sachgebiete/ElektrizitaetundGas/Unternehmen_Institutionen/ErneuerbareEnergien/Photovoltaik/DatenMeldgn_EEG-VergSaetze/DatenMeldgn_EEG-VergSaetze_node.html"
        }
        
        # Hier weitere Quellen
    ],
    "maintainers": [
        {
            "name": "Wolf-Dieter Bunke",
            "email": "wolf-dieter.bunke@uni-flensburg.de",
            "web": "http://open-power-system-data.org/"
        }
    ],
    "views": [
        {
            # You can put hints here which kind of graphs or maps make sense to display your data. This makes the 
            # Data Package Viewer at http://data.okfn.org/tools/view automatically display visualazations of your data.
            # See http://data.okfn.org/doc/data-package#views for more details.
        }
    ],
    # extend your datapackage.json with attributes that are not
    # part of the data package spec
    # you can add your own attributes to a datapackage.json, too
    "openpowersystemdata-enable-listing": True # This is just an example we don't actually make use of yet.
}

# Re-order the json before printing, since Python otherwise forgets the definition order above
sort_order = ['name', 'title', 'description', 'version', 'keywords', 'resources']

# Not nice working 
# key=lambda k: sort_order.index(k) if k in sort_order else 1000)
dataPackageSpec = OrderedDict(sorted(dataPackageSpec.items(), key=lambda t: t[0]))

jsonString = json.dumps(dataPackageSpec, indent=4, separators=(',', ': '))


# # 8 Write Data Package to disk
# 
# Again, we follow the Frictionless Data project's suggestions (see http://data.okfn.org/) to write a data package.
# 
# The data package consists of:
#  * **datapackage.json** A file containing meta data of the data package
#  * **data_renewables.csv** The file containing the actual data in CSV format
#  * **README.md** A readme which is essentially just a copy of this Jupyter Notebook converted to Markdown format
# 
# Following this file structure allows to use a number of tools (http://data.okfn.org/tools) designed specifically for data packages.

# In[ ]:

import os
# dataPackagePath = "output/datapackage_testpackage/"
dataPackagePath = '/home/leppi/output/'

if not os.path.exists(dataPackagePath):
    os.makedirs(dataPackagePath)
    
opsd_pv.to_csv(dataPackagePath+'register_data_roof_mounted_pv_germany.csv')

with open(dataPackagePath+"datapackage.json", "w") as json_file:
    json_file.write(jsonString)

# Now convert this iPython Notebook to Markdown format and use it as README.md for the data package:
import subprocess

# !!! not working for me
catchResult = subprocess.call(['ipython', 'nbconvert', '--to', 'markdown', currentFileName+'.ipynb'])
readmeFilePath = dataPackagePath+'README.md'
if os.path.exists(readmeFilePath): os.remove(readmeFilePath)
os.rename(currentFileName+'.md', readmeFilePath)


# In[46]:

#
opsd_pv.head()


# In[ ]:



