import os
import logging
from datetime import datetime

def init_logger():
    """
    Creates and configures a logger instance from the standard logging library
    """
    path_to_log = handle_log_path()
    
    # logger = logging.getLogger('logger')
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    
    file_handler = logging.FileHandler(path_to_log)
    file_handler.setLevel(logging.DEBUG)
    
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    return logger

def handle_log_path():
    """
    Generates path to log directory,
    if the log directory does not exist yet, it will be created
    returns absolute path of log file to write 
    """
    # defining an absolute path of project folder
    bot_dir = os.getcwd()
    # adding relative path to log
    relative_log_path = 'log'
    log_directory_path = os.path.join(bot_dir, 
                                      relative_log_path)
    
    # if the log directory does not exist yet, it will be created
    if not os.path.exists(log_directory_path):
        os.makedirs(log_directory_path)
    
    log_filename = f'{datetime.today().date().isoformat()}.log'
    log_path = os.path.join(log_directory_path,
                            log_filename)
    
    return log_path
    
