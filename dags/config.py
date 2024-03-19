#CONFIG 설정들을 불러오는 코드


import os
import json
import logging
import logging.config
import time
import pendulum


#변수명은 같고 환경 변수값을 다르게 설정할 경우
#각각의 환경에 등록 되어있는 값을 반환
current_directory = os.environ.get('CURRENT_PATH')
current_directory = os.path.join(os.getcwd(), "dags")


def get_api_config():
    api_config_path = os.path.join(current_directory, 'api_config.json')
    # API 설정 파일 로드
    with open(api_config_path, 'r') as f:
        api_config = json.load(f)

    return api_config[api_config["SELECT_API"]][api_config["SELECT_DATA"]]


def get_config():
    config_path = os.path.join(current_directory, 'config.json')
    # DB, LOG 설정 파일 로드
    with open(config_path, 'r') as f:
        config = json.load(f)
        
    return config

def get_db_config():
    config = get_config()
    selected_db = config["DB_CONFIG"]["SELECT_DB"]
    db_config = config["DB_CONFIG"][selected_db]
    return db_config

#Logger 생성 Level - main:INFO / subpgm_1:WARNING / subpgm_2 : DEBUG
def get_logger(logger_name):
    config = get_config()
    # 로깅 설정 적용
    logging.config.dictConfig(config["LOG_CONFIG"])
    
    logger = logging.getLogger(logger_name)
    return logger
