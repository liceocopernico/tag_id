import os
import configparser
from enum import Enum

class TagColor(Enum):
    BACKGROUND = "#F2F2F2"
    UPPER_BAR = "#8C8C8C"
    LOWER_BAR= "#342E59"
    BUTTON = "#404040"
    TEXT_DARK = "#0D0D0D"
    TEXT_LIGHT = "#F2F2F2"



class genConfig:
    def __init__(self): 
        if os.path.exists("/opt/tag_reader/config.ini"):
            base_path="/opt/tag_reader/"
        else:
            base_path=os.path.dirname(os.path.realpath(__file__))+"/assets/"
        
        config = configparser.ConfigParser()
        
        config.read(base_path+"config.ini")
        self.DB_TYPE=config['database']['db_type']
        self.DB_PATH=config['database']['db_path']
        self.DB_NAME=config['database']['db_name']
        self.DB_USER=config['database']['db_user']
        self.DB_PWD=config['database']['db_pwd']
        self.DB_PORT=int(config['database']['db_port'])
        self.DB_HOST=config['database']['db_host']
        self.CLASSROOMGRID=(10,8)
        
        self.DEFAULT_READER=config['reader']['default_reader']

