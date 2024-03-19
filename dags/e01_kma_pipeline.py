#기상청 API로 지상관측 일자료(기간) 데이터를 받아오는 (DAG)코드
#시작 일자 : 2024-03-07
#최근 업데이트 일자 : 2024-03-18
#khj



from datetime import datetime
from airflow import DAG
import pendulum


# 사용할 Operator Import
from airflow.operators.python import PythonOperator # 파이썬 코드를 돌릴 때 사용 #ti 객체사용가능

from airflow.providers.http.sensors.http import HttpSensor # 응답(response)하는지 확인할 때 사용
from airflow.providers.http.operators.http import SimpleHttpOperator # HTTP 요청(request)을 보내고 응답(response) 텍스트를 받는 작업
from airflow.operators.bash import BashOperator # bash 명령어를 실행시키는 작업
from airflow.operators.python_operator import BranchPythonOperator
from airflow.operators.dummy_operator import DummyOperator

from e01_kma import e01_kma_api_chk, e01_kma_run, e01_kma_save


local_tz = pendulum.timezone("Asia/Seoul") #한국 시간으로 설정

# DAG 디폴트 설정
default_args = {
    "start_date": datetime(2024, 3, 4, tzinfo=local_tz), # 2024년 3월 4일부터 DAG 시작 실행 시간 (데이터 받아오는 시간 x)
    'depends_on_past': False,    # 이전 dag run에서 현재 task가 실패했으면 실행하지 않음
    'wait_for_downstream': False, # 이전 dag run에서 현재 task의 downstream이 실패했으면 실행하지 않음
    "retries": 0                # 실패시 재시도 횟수
}

with DAG(
    default_args=default_args,
    dag_id="e01_kma_pipeline",
    #schedule_interval="@daily",            #매일 하는 걸 원하면 이걸 실행
    schedule_interval="0 5 * * *",          #어느 시간에 돌릴 것인지 / 분,시간,일,월,요일 (현재 매일 05시 실행)
    # 태그는 원하는대로
    tags=["E01", "kma", "pipeline", "khj"], #Airflow UI에서 보이는 태그 (적어도 1개 이상 필요)
    catchup=False                           #catchup을 True로 하면, start_date 부터 누락된 실행을 채움
) as dag:
    
    #데이터 전처리
    task_e01_kma_api_chk = PythonOperator(
        task_id="e01_kma_api_chk",
        provide_context=True,
        python_callable= e01_kma_api_chk  # 실행할 파이썬 함수
    )

    #데이터 전처리
    task_e01_kma_run = PythonOperator(
        task_id="e01_kma_run",
        provide_context=True,
        python_callable= e01_kma_run  # 실행할 파이썬 함수
    )
    #DB 저장
    task_e01_kma_save = PythonOperator(
        task_id="e01_kma_save",
        provide_context=True,
        python_callable= e01_kma_save, # 실행할 파이썬 함수
    )


    # 파이프라인 구성하기
    task_e01_kma_api_chk >> task_e01_kma_run >> task_e01_kma_save
    