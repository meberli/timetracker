#!/usr/bin/env python3
import pyodbc
import logging

db_driver = "{ODBC Driver 17 for SQL Server}"

class timedb:
    def __init__(self, server=None, db=None, uid=None, pwd=None, table=None):
        self.logger = logging.getLogger(__name__)
        self.conn_str = (f'Driver={db_driver}; '
            f'Server={server}; '
            f'Database={db}; '
            f'UID={uid}; '
            f'PWD={pwd}; ')
        self.table=table
        self.logger.debug(f'db initialized with sql connection string: {self.conn_str}, table: {self.table}')

    def insertTimeTrackEntry(self, device_id, badge_id, badge_event, time):
        r = False
        self.conn = pyodbc.connect(self.conn_str)
        self.cursor = self.conn.cursor()
        if (badge_event == "in"):
            badge_event = "KOMMEN"
        elif (badge_event == "out"):
            badge_event = "GEHEN"
        else:
            msg = (f'unknown value for badge_event: "{badge_event}" '
                   f'valid values are "in" and "out"')
            self.logger.error(msg)
            return False
        try:
            self.cursor.execute(
                'IF NOT EXISTS(select * from '
                f'{self.table} where [timestamp] = ? '
                'AND [personal_card_id] = ?) '
                f'INSERT INTO {self.table} '
                '([guid], '
                '[timestamp], '
                '[personal_card_id], '
                '[entry_type], '
                '[server_timestamp], '
                '[client_ident], '
                'personal_addition) '
                'VALUES (NEWID(),?,?,?,GETDATE(),?,?)',
                (
                    time,
                    badge_id,
                    time,
                    badge_id,
                    badge_event,
                    device_id,
                    'lora'))
            self.cursor.commit()
            ret = self.cursor.rowcount == 1
        except pyodbc.Error as ex:
            sqlstate = ex.args[0]
            r = f'fehler. {ex} -- sqlstate = {sqlstate}'
            self.logger.error(r)
        return ret

    def getTimeTrackEntries(self):
        self.conn = pyodbc.connect(self.conn_str)
        self.cursor = self.conn.cursor()
        sql = f'SELECT * FROM {self.table}'
        self.cursor.execute(sql)
        res = '<table>'
        for row in self.cursor:
            res += '<tr>'
            for field in row:
                res += f'<td><pre>{field}</pre></td>'
            res += '</tr>'
        res += '</table>'
        return res

    def disconnect(self):
        self.conn.close()
