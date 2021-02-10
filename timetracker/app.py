#-----------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See LICENSE in the project root for license information.
#-----------------------------------------------------------------------------------------

from flask import Flask
from os import getenv
import logging
from gwu import timedb, ldc
from datetime import datetime, time, timedelta

import json
import yaml
import logging.config
import logging

with open('logging.yaml','rt') as f:
        config=yaml.safe_load(f.read())
        f.close()
logging.config.dictConfig(config)
logger=logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.error("Contest is starting")

app = Flask(__name__)
boxid = '2306ddb0-67d6-40d7-8099-17190977f6f0'
filterdict = {'messagetype': 'Badge_Event'}
tdb = timedb()
ldc = ldc()
@app.route("/")
def hello():
    return app.send_static_file("index.html")

@app.route("/timetracker")
def timeentry():
    dt_to = datetime.utcnow()
    dt_from = datetime.combine(dt_to.date(),time.min) - timedelta(days=1)
    data=ldc.get_sensor_range(boxid, filterdict, dt_from, dt_to)
    for entry in data[0]['series'][0]['values']:
        if (tdb.insertTimeTrackEntry(entry[2], entry[9], entry[4], entry[0])):
            logger.info(f'successfully insertied new entry : ts {entry[0]}, uuid: {entry[9]}, inout: {entry[4]}')
        else:
           logger.info(f'entry already exists - skipping.  ts {entry[0]}, uuid: {entry[9]}, inout: {entry[4]}') 
    return tdb.getTimeTrackEntries()

@app.route("/listtimedb")
def listtimedb():
    return tdb.getTimeTrackEntries()

@app.route("/listldc")
def listldc():
    dt_to = datetime.utcnow()
    dt_from = datetime.combine(dt_to.date(),time.min)
    data=ldc.getSensorData(boxid, filterdict, dt_from, dt_to)
    logger.info(f'data from ldc: {data}')
    res = '<pre>'
    res += json.dumps(data, sort_keys=True, indent=4 )
    res += '</pre>'
    return res