import configparser


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

    def read_request_info(self):
        request_info = {
            'URL': '',
            'Port': ''
        }
        try:
            request_info['URL'] = self.config.get('Request_info', 'url')
            request_info['Port'] = self.config.get('Request_info', 'port')
        except Exception as e:
            print('[ConfigParser ERROR]\n' + e)

        return request_info

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

    def read_location_info(self):
        location_range = {
            'x': 0.000400,
            'y': 0.000100
        }
        try:
            location_range['x'] = float(self.config.get('Location_Range', 'x'))
            location_range['y'] = float(self.config.get('Location_Range', 'y'))
        except Exception as e:
            print('[ConfigParser ERROR]\n' + e)

        return location_range
