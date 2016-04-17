# Copyright (C) 2016 Ross D Milligan
# GNU GENERAL PUBLIC LICENSE Version 3 (full notice can be found at https://github.com/rdmilligan/ArkwoodAR)

import ConfigParser

class ConfigProvider:

    def __init__(self):
        self.config = ConfigParser.ConfigParser()
        self.config.read('appsettings.ini')

    @property 
    def media_cube(self):
        return self.config.getboolean('Features', 'MediaCube')

    @property 
    def secret_item(self):
        return self.config.getboolean('Features', 'SecretItem')


