import sys
from datetime import datetime

# Add the elt directory to Python path before importing elt modules
sys.path.append("/opt/airflow/elt")
sys.path.append("/opt/airflow")

from airflow.providers.standard.operators.python import PythonOperator
from airflow.sdk.definitions.param import ParamsDict, Param

from airflow import DAG

from elt.configs.config import Config
from elt.configs.mapper import Mapper
from elt.configs.repository import Repository
from elt.extract import Extract
from elt.configs.yahoo_finance_client import YahooFinanceClient
from elt.load import Load
from elt.transform import Transform

config = Config()
client = YahooFinanceClient(config)
repository = Repository(config)
mapper = Mapper()

extract = Extract(client)
load = Load(repository)
transform = Transform(mapper)

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
}

def extract_ticker_info(ticker_symbol):
    try:
        print(f"Extracting ticker: {ticker_symbol}")
        ticker = extract.extract_ticker(ticker_symbol)
        ticker_info = transform.transform_ticker_to_ticker_info(ticker)
        load.load_ticker_info(ticker_info)
        print(f"Successfully extracted ticker info for {ticker_symbol}")
        
    except Exception as e:
        print(f"Error when extracting ticker info: {ticker_symbol}", e)
        raise e

def fail_task():
    sys.exit(1)

dag = DAG(
    'ELT_stock_market',
    default_args=default_args,
    params=ParamsDict({
        "ticker": Param("AAPL", type="string", description="Ticker name")
    }),
    description='An ELT workflow',
    start_date=datetime.now(),
    catchup=False,
)

t1 = PythonOperator(
    task_id='extract_ticker',
    python_callable=extract_ticker_info,
    op_kwargs={"ticker_symbol": "{{ params.ticker }}"},
    dag=dag,
)