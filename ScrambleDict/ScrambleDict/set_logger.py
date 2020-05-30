import logging
from logging.config import dictConfig
import yaml
import time


def set_config_and_get_logger(logger_name) -> logging.Logger:
    """ 根據 log_config.yaml 設定 logger，並 return 此 logger
    
    Args:
        logger_name: 只能夠是 log_config.yaml 中定義好的 logger_name
        
    Returns:
        logger: 拿來 logging 用
        
    Examples:
        logger = set_config_and_get_logger('BUILD_PHONE_RECORD_INFO_TABLE')
        
    """
    with open('log_config.yaml', 'r', encoding='utf-8') as f:
        log_config = yaml.load(f, Loader=yaml.FullLoader)
    log_config['handlers']['file']['filename'] = get_log_file_name('info')
    log_config['handlers']['error']['filename'] = get_log_file_name('error')
    dictConfig(log_config)
    logger = logging.getLogger(logger_name)
    return logger

def get_log_file_name(log_type: str) -> str:
    """ 以呼叫該 function 時的 datetime 作為 logging file name
    """
    current_time = time.strftime('%Y%m%d%H%M%S')
    log_file_name = f'logs/{current_time}_{log_type}.log'
    return log_file_name