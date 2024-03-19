import psycopg2
from urllib.parse import quote

from config import get_api_config, get_db_config, get_logger



from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

#SQLAlchemy is a ORM
#psycopg2 is a database driver.

#Logger 생성 Level - main:INFO / subpgm_1:WARNING / subpgm_2 : DEBUG
#Config.json에서 logger 이름 및 레벨 변경 가능

logger = get_logger("subpgm_2")
db_config = get_db_config()
api_config = get_api_config()
    

def db_connect(server_db_name):
    logger.info("db_connect 시작")
    conn = None

    # PostgreSQL에 연결
    logger.info("PostgreSQL 연결 시도 중입니다.")
    try:
        conn = psycopg2.connect(host=db_config['host'],
                                    dbname=db_config['dbname'],
                                    user=db_config['user'],
                                    password=db_config['password'],
                                    port=db_config['port'])
                
        logger.info("PostgreSQL 연결에 성공했습니다.")
    except Exception as e:
        logger.error(f"PostgreSQL 연결에 실패했습니다.: {e}")

    logger.info("db_connect 종료")
    return conn


def db_engine(server_db_name):
    logger.info("db_engine 시작")
    engine = None

    logger.info("SQLAlchemy 연결 시도 중입니다.")
    try:
        #db_config = config["DB_CONFIG"][server_db_name]
        db_url = f'postgresql://{db_config["user"]}:{quote(db_config["password"])}@{db_config["host"]}:{db_config["port"]}/{db_config["dbname"]}'
        engine = create_engine(db_url) # 연결
    except  Exception as e:
        logger.error(f"{server_db_name} 데이터베이스 엔진 생성 실패: {e}")

    logger.info("db_engine 종료")
    return engine


#Session : 데이터베이스와의 모든 대화를 중개하며, SQL 작업의 단위(unit of work)를 나타내는 객체
def db_session(server_db_name):
    logger.info("db_session 시작")

    engine = db_engine(server_db_name)
    session = None
    try:
        Session = sessionmaker(bind=engine)
        session = Session()
    except Exception as e:
        logger.error(f"세션 생성 실패: {e}")
    
    if session:
        logger.info("세션 생성 성공")
    else:
        logger.info("세션 생성 실패")

    logger.info("db_session 종료")
    return session
    