#!/usr/bin/env python3
import pyodbc
import logging

db_server = "10.100.100.150"
db_user = "piot_user_test"
db_password = "UIRcUQFWfnA8uasI4IGM"
db_dbname = "ocTerminal40_TEST"
db_tablename = "[oc_terminal_user_test].[terminal_entry]"

db_driver = "{ODBC Driver 17 for SQL Server}"
conn_str = (f'Driver={db_driver}; '
            f'Server={db_server}; '
            f'Database={db_dbname}; '
            f'UID={db_user}; '
            f'PWD={db_password}; ')

class timedb:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        self.logger.debug(f'sql connection string: {conn_str}')
        self.logger.debug('{} initialized')

    def insertTimeTrackEntry(self, device_id, badge_id, badge_event, time):
        r = False
        self.conn = pyodbc.connect(conn_str)
        self.cursor = self.conn.cursor()
        if (badge_event == "in"):
            badge_event = "KOMMEN"
        elif (badge_event == "out"):
            badge_event = "GEHEN"
        else:
            msg = (f'unknown value for badge_event: "{badge_event}" '
                   f'valid values are "in" and "out"'
            )
            self.logger.error(msg)
            return False
        try:  
            self.cursor.execute(f'IF NOT EXISTS(select * from {db_tablename} where [timestamp] = ? AND [personal_card_id] = ?) '
                                f'INSERT INTO {db_tablename} '
                                '([guid], '
                                '[timestamp], '
                                '[personal_card_id], '
                                '[entry_type], '
                                '[server_timestamp], '
                                '[client_ident], '
                                'personal_addition) '
                                'VALUES (NEWID(),?,?,?,GETDATE(),?,?)',
                                (time, badge_id, time, badge_id, badge_event, device_id, 'lora'))
            self.cursor.commit()
            ret = self.cursor.rowcount == 1
            
        except pyodbc.Error as ex:
            sqlstate = ex.args[0]
            r = f'fehler. {ex} -- sqlstate = {sqlstate}'
            self.logger.error(r)
        return ret


    def getTimeTrackEntries(self):
        self.conn = pyodbc.connect(conn_str)
        self.cursor = self.conn.cursor()
        sql = f'SELECT * FROM [oc_terminal_user_test].[terminal_entry]'
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