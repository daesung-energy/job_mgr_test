#DAG에 필요한 함수 구현 코드

import requests
import warnings
warnings.filterwarnings('ignore')

import datetime as dt
import numpy as np
import pandas as pd
import pytz
from datetime import datetime, timedelta, timezone

#Airflow
from airflow.exceptions import AirflowSkipException, AirflowFailException
from airflow.operators.python import get_current_context

#DB
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
import psycopg2

#커스텀 라이브러리
import dbconnect
from config import get_api_config, get_db_config , get_logger
from model import kma_sfcdd

#Logger 생성 Level - main:INFO / subpgm_1:WARNING / subpgm_2 : DEBUG
#Config.json에서 logger 이름 및 레벨 변경 가능
logger = get_logger("subpgm_2")
db_config = get_db_config()
api_config = get_api_config()


#-------------------------------------------------------------

# 실패 혹은 원하는 로직 시 Task를 fail로 만들어주는 함수
def on_failure_callback():
    context = get_current_context()
    task_instance = context.get("task_instance")
    logger.error(f"Task {task_instance.task_id} 실행 중에 예외가 발생했습니다.")
    
    #실패 후 TASK를 FAIL로
    raise AirflowFailException(f"Fail task {task_instance.task_id}")
    
    #raise Exception()

    #실패 후 TASK를 SKIP으로
    #raise AirflowSkipException("Skip the next task because of failure")

#-------------------------------------------------------------


def e01_kma_api_chk():
    logger.info("e01_kma_api_chk 시작")


    key = api_config["key"]            #개인 인증키
    region = api_config['region']      # STN(ID) 대구 지역코드
    url = api_config["url"]

    params ={'stn' : region,                                    
            'authKey' : key}
    
    try:
        response = requests.get(url, params=params, verify=False)
        logger.info("Response Status Code: " + str(response.status_code))
        if response.status_code == 200:
            logger.info("e01_kma_api가 정상적으로 작동 중입니다.")
            logger.debug("Response.text")
            logger.debug(response.text)
        else:
            logger.warning("e01_kma_api가 작동 중이지 않습니다.")
    except Exception as e:
        logger.error("HTTP 요청 중 오류 발생:", e)
        response = None
        on_failure_callback()
        

    logger.info("e01_kma_api_chk 종료")
    return response.status_code if response else None


#-------------------------------------------------------------
def e01_kma_run():
    logger.info("e01_kma_run 시작")

    dbname = db_config["dbname"]
    logger.debug(f"선택된 DB 이름: {dbname}")

    #[[마지막 일자 가져오기]]
    last_date = None

    '''
    # 방법1 : psycopg2
    try:
        conn = dbconnect.db_connect(dbname)

        if conn is None:
            raise Exception("데이터베이스 연결 실패")

        cur = conn.cursor()
        query = f'SELECT tm FROM kma_sfcdd ORDER BY tm DESC LIMIT 1'
        cur.execute(query)

        row = cur.fetchone()
        last_date = row[0] if row else None
        logger.info(f"마지막으로 저장된 날짜: {last_date if last_date else '없음'}")

    except Exception as e:
        logger.error(f"데이터베이스 작업 중 오류 발생: {e}")
        on_failure_callback()
    finally:
        # 커서와 연결이 열려 있으면 닫기
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()
    '''


    #방법2 : sqlalchemy
    try:
        session = dbconnect.db_session(dbname)
        if session is None:
            raise Exception("세션 연결 실패")
        
        # 마지막 일자 가져오기
        query = select([kma_sfcdd.TM]).order_by(kma_sfcdd.TM.desc()).limit(1)
        result = session.execute(query).scalar()
        
        last_date = result if result else None
        logger.info(f"마지막으로 저장된 날짜: {last_date if last_date else '없음'}")
        
    except Exception as e:
        logger.error(f"데이터베이스 작업 중 오류 발생: {e}")
        on_failure_callback()
    finally:
        # 세션 종료
        session.close()

        
    url = api_config["url"]
    key = api_config["key"]   #개인 인증키
    region = api_config["region"]      # STN(ID) 대구 지역코드
    col_name = api_config["col_name"]
    start_date = api_config["default_start_date"] #시작 날짜(기본값) 

    if last_date is None:
        last_date = start_date
        logger.info("마지막으로 저장된 날짜가 없습니다.")
    else:
        logger.info("마지막 저장 날짜 : " + last_date)



    #[[어제 시간 가져오기]]

    # 현재 시간을 가져옴
    now_utc = datetime.now()
    # 한국 시간대로 변환
    seoul_timezone = pytz.timezone('Asia/Seoul')
    now_seoul = now_utc.astimezone(seoul_timezone)
    # 하루 전의 시간을 계산
    seoul_time_yesterday = now_seoul - timedelta(days=1)
    # 변환된 시간을 문자열로 변환하여 로그에 출력
    logger.info("현재 시간: " + now_seoul.strftime('%Y-%m-%d %H:%M:%S'))
    logger.info("하루 전 시간: " + seoul_time_yesterday.strftime('%Y-%m-%d %H:%M:%S'))
    seoul_time_yesterday = seoul_time_yesterday.strftime('%Y%m%d')
    

    if last_date == seoul_time_yesterday:
        logger.info("이미 어제까지의 정보가 업데이트 되어있습니다.")
        on_failure_callback()



    #[[데이터 가져오기]]
        
    logger.info("데이터 수집 기간 : " + str(last_date) + " ~ " + str(seoul_time_yesterday)) 
    params ={'tm1' : last_date,     # 시작 날짜
            'tm2' : seoul_time_yesterday ,       # 끝 날짜
            'stn' : region,    # 지역번호
            'help' : 0,        # 0: 설명이 안나옴, 1: 설명이 나옴 
            'authKey' : key}
    

    response = requests.get(url, params=params, verify=False)
    logger.info("Response Status Code: " + str(response.status_code))
    
    text = response.text.split("\n")[5:-2] #앞의 필요없는  5줄 부분과 뒤의 필요없는 2줄 부분을 제거
    
    df_e01_kma = pd.DataFrame(text)[0].str.split(expand=True) #데이터프레임 컬럼으로 변경
    df_e01_kma.columns = col_name # 컬럼 설정: 해당 API 특성 상 사용할 컬럼명을 미리 지정해줘야 사용가능
    logger.debug("df_e01_kma: " + str(df_e01_kma))
    



    #[[데이터 전처리]]

    # 음수값이나 문자를 null 값으로 대체하는 함수
    # 모든 열을 숫자로 변환하고, 변환이 안 되거나 음수인 경우 none으로 대체
    def replace_invalid_values(df):
        logger.info('replace_invalid_values 시작')
        df = df.apply(pd.to_numeric, errors='coerce')
        for index, row in df.iterrows():
            for col in df.columns:
                if col == 'TM':
                    df[col] = df[col].astype(str).apply(lambda x: str(int(x)).zfill(8))
                elif col in ['WS_MAX_TM', 'WS_INS_TM', 'TA_MAX_TM', 'TA_MIN_TM']:
                    df[col] = df[col].astype(str).apply(lambda x: str(int(x)).zfill(4) if int(x) >= 0 else None)
                elif col in ['WS_MAX', 'WS_INS', 'TA_AVG', 'TA_MAX', 'TA_MIN']:
                    df[col] = df[col].astype(float)
        
        logger.info('replace_invalid_values 종료')
        return df
        

    #필요한 부분만 추출>|관측일|평균기온|최고기온|최고기온시각|최저기온|최저기온시각|평균풍속|최대풍속|최대풍속시각|최대순간풍속|최대순간풍속시각
    df_e01_kma= df_e01_kma[['TM','TA_AVG','TA_MAX','TA_MAX_TM','TA_MIN','TA_MIN_TM','WS_AVG','WS_MAX', 'WS_MAX_TM', 'WS_INS', 'WS_INS_TM']]

    #필요시 컬럼명 변경 (현재는 그대로 사용 중)
    #df_e01_kma.columns = ['TM','TA_AVG','TA_MAX','TA_MAX_TM','TA_MIN','TA_MIN_TM','WS_AVG','WS_MAX', 'WS_MAX_TM', 'WS_INS', 'WS_INS_TM']

    preprocessed_df_e01_kma = replace_invalid_values(df_e01_kma)
    logger.debug('preprocessed_df_e01_kma : ' + str(preprocessed_df_e01_kma))

    logger.info("e01_kma_run 종료")
    return preprocessed_df_e01_kma


#-------------------------------------------------------------
def e01_kma_save(**context):
    logger.info("e01_kma_save 시작")

    text = context['task_instance'].xcom_pull(task_ids='e01_kma_run')   #데이터 받아오기
    df_e01_kma =pd.DataFrame(text)      #데이터프레임 컬럼으로 변경
    logger.debug(df_e01_kma)


    dbname = db_config["dbname"]
    username = db_config['user']

    
    conn = dbconnect.db_connect(dbname)
    #DB 연결 성공 확인
    if conn is not None:
        logger.info("데이터베이스 연결에 성공했습니다.")
    else:
        logger.error("데이터베이스 연결에 실패했습니다.")
        on_failure_callback()
        return
    cur = conn.cursor()


    session = dbconnect.db_session(dbname)
    session.close()


    # 현재 날짜 및 시간 가져오기
    current_datetime = dt.datetime.now()
    CR_TM = current_datetime
    CR_ID = username


    '''
    #방법1 : psycopg2
    try:
        for row in df_e01_kma.itertuples():
            if row.TM is not None:
                logger.debug("데이터 삽입 시도")
                sql = """
                    INSERT INTO kma_sfcdd (
                        TM, TA_AVG, TA_MAX, TA_MAX_TM, TA_MIN, TA_MIN_TM, WS_AVG, WS_MAX, WS_MAX_TM, WS_INS, WS_INS_TM, CR_TM, CR_ID
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (TM) DO NOTHING
                """
                cur.execute(sql, (
                    row.TM, row.TA_AVG, row.TA_MAX, row.TA_MAX_TM, row.TA_MIN, row.TA_MIN_TM,
                    row.WS_AVG, row.WS_MAX, row.WS_MAX_TM, row.WS_INS, row.WS_INS_TM, CR_TM, CR_ID
                ))
                #cur.execute(sql, (row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], CR_TM, CR_ID))

                # 데이터베이스에서 실제로 삽입이 수행되었는지 확인합니다.
                if cur.rowcount == 0:
                    logger.warning(f"Record for TM={row.TM} 데이터가 이미 존재합니다.")
                else:
                    logger.debug("데이터 삽입 성공") 
        conn.commit()
    except Exception as e:
        # 예외 발생 시 트랜잭션 롤백
        conn.rollback()
        logger.error(f"레코드 삽입 중 오류 발생: {e}")
        on_failure_callback()
    finally:
        # 커서와 연결 닫기
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()

    '''

    #방법2 : sqlalchemy
    try:
        for row in df_e01_kma.itertuples():
            if row.TM is not None:
                # 데이터베이스에 이미 해당 TM이 존재하는지 확인합니다.
                existing_record = session.query(kma_sfcdd).filter_by(TM=row.TM).first()
                if not existing_record:
                    record = kma_sfcdd(
                        TM=row.TM,
                        TA_AVG=row.TA_AVG,
                        TA_MAX=row.TA_MAX,
                        TA_MAX_TM=row.TA_MAX_TM,
                        TA_MIN=row.TA_MIN,
                        TA_MIN_TM=row.TA_MIN_TM,
                        WS_AVG=row.WS_AVG,
                        WS_MAX=row.WS_MAX,
                        WS_MAX_TM=row.WS_MAX_TM,
                        WS_INS=row.WS_INS,
                        WS_INS_TM=row.WS_INS_TM,
                        CR_TM=CR_TM,                # 정의된 TIMESTAMP 객체
                        CR_ID=CR_ID                 # 정의된 사용자 ID
                    )
                    session.add(record)
                else:
                    logger.info(f"TM={row.TM}에 대한 레코드가 이미 존재합니다.")
        session.commit()
        logger.info("데이터 삽입 완료")
    except IntegrityError as e:
        session.rollback()
        logger.warning(f"데이터베이스 무결성 오류 발생: {e}")
    except Exception as e:
        session.rollback()
        logger.error(f"레코드 삽입에 실패했습니다.: {e}")
    finally: 
        session.close()

    logger.info("e01_kma_save 종료")