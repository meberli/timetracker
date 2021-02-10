#!/usr/bin/env python3
import pyodbc
import logging
import requests
import functools

def apilogger(func):
    @functools.wraps(func)
    def wrapper(self, *arg, **kw):
        self.logger.debug(f'-- entering {func.__name__}')
        self.logger.debug(f'-- {self.__dict__}')
        res = func(self, *arg, **kw)
        self.logger.debug(f'-- exiting {func.__name__}')
        self.logger.debug(f'-- {self.__dict__}')
        return res
    return wrapper

class ldc:
    def __init__(self, apiURL= "https://apibeta.gateway.uno:443"):
        self.logger = logging.getLogger(__name__)
        self.apiURL = apiURL
        self.logger.debug(f'ldc initialized')

    @apilogger
    def get_boxes(self):
        query = {}
        url = f'{self.apiURL}/boxes'
        response = requests.get(url, params=query)
        return(response.json())
    
    @apilogger
    def get_all_sensors(self, gw_id, datetime_from=None, datetime_to=None, tags={}):
        query = {'from':datetime_from, 'to':datetime_to}
        url = f'{self.apiURL}/box/{gw_id}/sensor'
        response = requests.get(url, params=query)
        return(response.json())

    @apilogger
    def get_sensor_range(self, gw_id, sensor_id, datetime_from=None, datetime_to=None):
        query = {'from':datetime_from, 'to':datetime_to}
        url = f'{self.apiURL}/box/{gw_id}/sensor/{sensor_id}'
        response = requests.get(url, params=query)
        return(response.json())

    @apilogger
    def get_sensor_all(self, gw_id, sensor_id):
        query = {}
        url = f'{self.apiURL}/box/{gw_id}/sensor/{sensor_id}/all'
        response = requests.get(url, params=query)
        return(response.json())

if __name__ == '__main__':
    t = ldc()
    t.logger.setLevel(logging.DEBUG)
    t.logger.b
    print(t.get_all_sensors('2306ddb0-67d6-40d7-8099-17190977f6f0'))
