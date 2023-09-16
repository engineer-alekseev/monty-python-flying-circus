import configparser
import os.path
import sys
from logging import getLogger

logger = getLogger('logger')

def read_conf_file(path: str) -> configparser.ConfigParser:
    if os.path.exists(path):
        conf = configparser.ConfigParser()
        conf.read(path, encoding='utf-8')
        logger.info(f"conf file readed from {path}")
        return conf
    else:
        logger.critical(f"conf file not found in {path}")
        sys.exit()

def generate_conf_path():
    project_root_dir = os.getcwd()
    conf_directory = 'conf'
    conf_file = 'tg.conf'

    conf_path = os.path.join(project_root_dir, 
                             conf_directory,
                             conf_file)
    
    return conf_path