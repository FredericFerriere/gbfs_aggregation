# Description

This project allows regular imports from a gbfs dataset, stores the data in a SQLite db and allows historical retrieval with FastAPI.
Dataset URL can be defined in constants.py, as well as the refresh frequencey.
API endpoints allow retrieval of hourly windowed data or hourly aggregated data over a 24 hour period.


# Installation

use pip install requirements.txt

# Running

cmd lines: 
1) cd api
2) fastapi dev main.py

This will launch data update (scheduled process retrieving gbfs files and storing results into the database located at ./sql_db/gbfs.db)
It will also launch the api
API can be tested with the following station_id: stn_92GiBpSzCHLu9M3v4dmFCo

# Implementing a new version (Vx.y)

This implies updating the model schema and the api endpoints.
* in models, add new directory and implement appropriate classes as per gbfs specs
* in gbfs_importer, create a new importer for that version (this should reference the matching model version)
* in api, add new directory and implement appropriate functions, adding a new routing. Reference that routing in api/main.py

