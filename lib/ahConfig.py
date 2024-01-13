import configparser
import logging
from lib import logs

class ahConfig:
#Reads in config file info

    def __init__(self):
        self.configParser = configparser.RawConfigParser()
        configFilePath = r'config.txt'
        #configFilePath = r'E:\Scripts\PharmacyReportPressGaney\version1\config.txt'
        self.configParser.read(configFilePath)
        self.log = logging.getLogger('lib.logs.' + __name__)
        self.log.info("==== INITIATE ahConfig ====")
        
    def get_config_section(self, section_name):
        dict1 = dict(self.configParser.items(section_name))
        return dict1