#!/usr/bin/python
#import requests
from os import getenv
import logging
from timetracker import ldc, timedb
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
logger.error("Import is starting")

boxid = '2306ddb0-67d6-40d7-8099-17190977f6f0'
tagfilter = 'messagetype,Badge_Event'

ldc = ldc.ldc()
tdb = timedb.timedb()

def main():
    dt_to = datetime.utcnow()
    dt_from = datetime.combine(dt_to.date(), time.min) - timedelta(days=1)
    data=ldc.get_all_sensors(boxid, dt_from, dt_to, tagfilter)
    for entry in data[0]['series'][0]['values']:
        if (tdb.insertTimeTrackEntry(entry[2], entry[9], entry[4], entry[0])):
            logger.info(f'successfully inserted new entry : ts {entry[0]}, uuid: {entry[9]}, inout: {entry[4]}')
        else:
            logger.info(f'entry already exists - skipping.  ts {entry[0]}, uuid: {entry[9]}, inout: {entry[4]}') 


if __name__ == "__main__":
    main()