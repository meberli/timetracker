#!/usr/bin/python
#import requests
from os import getenv
import logging
from timetracker.ldc import ldc
from timetracker.timedb import timedb
from datetime import datetime, time, timedelta

import json
import yaml
import logging.config
import logging
from jsonpath_ng import jsonpath, parse

with open('logging.yaml','rt') as f:
        config=yaml.safe_load(f.read())
        f.close()
logging.config.dictConfig(config)
logger=logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.error("Import is starting")

boxid = getenv('boxid')
tagfilter = getenv('tagfilter','messagetype,badge_event')
db_server=getenv('db_server')
db_user=getenv('db_user')
db_password=getenv('db_password')
db_dbname=getenv('db_dbname')
db_tablename=getenv('db_tablename')
sync_hours=int(getenv('sync_hours'))

ldc = ldc()
tdb = timedb(
    server=db_server,
    db=db_dbname,
    uid=db_user,
    pwd=db_password,
    table=db_tablename)

def main():
    dt_to = datetime.utcnow()
    dt_from = datetime.combine(dt_to.date(), time.min) - timedelta(hours=sync_hours)
    json_data=ldc.get_all_sensors(boxid, dt_from, dt_to, tagfilter)
    jsonpath_columns = parse('[0].series[0].columns')
    jsonpath_values = parse('[0].series[0].values')
    columns_match = jsonpath_columns.find(json_data)
    values_match = jsonpath_values.find(json_data)
    if columns_match:
        columns = columns_match[0].value
        for values in values_match[0].value:
            dictionary = dict(zip(columns, values))            
            logger.debug(
                f'insertTimeTrackEntry('
                f'uuid: {dictionary["uuid"]}, '
                f'inout: {dictionary["inout"]}, '
                f'device: {dictionary["deviceid"]}, '
                f'ts: {dictionary["time"]})')
            
            if (tdb.insertTimeTrackEntry(
                    {dictionary["deviceid"]}, 
                    {dictionary["uuid"]},
                    {dictionary["inout"]},
                    {dictionary["time"]})):
                logger.info(
                    f'successfully inserted new entry : '
                    f'ts {dictionary["time"]}, '
                    f'uuid: {dictionary["uuid"]}, '
                    f'inout: {dictionary["inout"]}')
            else:
                logger.info(
                    f'entry already exists - skipping.  '
                    f'ts {dictionary["time"]}, '
                    f'uuid: {dictionary["uuid"]}, '
                    f'inout: {dictionary["inout"]}') 


if __name__ == "__main__":
    main()