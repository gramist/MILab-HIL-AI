import logging
import configparser
import os


class FileIO:
    # Read properties file
    config = configparser.RawConfigParser()

    def __init__(self):
        try:
            self.config.read('conf/server.properties')
        except Exception as e:
            print('[ConfigParser ERROR]\n' + e)

    def read_server_info(self):
        server_info = {
            'IP': '',
            'Port': ''
        }
        try:
            server_info['IP'] = self.config.get('Server_Info', 'ip')
            server_info['Port'] = self.config.get('Server_Info', 'port')
        except Exception as e:
            print('[ConfigParser ERROR]\n' + e)

        return server_info

    def read_client_info(self):
        client_info = {
            'IP': '',
            'Port': ''
        }
        try:
            client_info['IP'] = self.config.get('Client_Info', 'ip')
            client_info['Port'] = self.config.get('Client_Info', 'port')
        except Exception as e:
            print('[ConfigParser ERROR]\n' + e)

        return client_info

    def read_db_info(self, path):
        db_info = {
            'host': '',
            'port': 0,
            'user': '',
            'password': '',
            'db': '',
            'charset': ''
        }
        try:
            self.config.read(path)
            db_info['host'] = self.config.get('Database_Info', 'host')
            db_info['port'] = self.config.get('Database_Info', 'port')
            db_info['user'] = self.config.get('Database_Info', 'user')
            db_info['password'] = self.config.get('Database_Info', 'password')
            db_info['db'] = self.config.get('Database_Info', 'db')
            db_info['charset'] = self.config.get('Database_Info', 'charset')
        except Exception as e:
            print('[ConfigParser ERROR]\n' + e)

        return db_info
