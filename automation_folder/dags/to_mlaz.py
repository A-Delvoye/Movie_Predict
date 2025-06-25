from airflow import DAG
from airflow.operators.python import PythonOperator
from azure.ai.ml.entities import Data
from azure.ai.ml.constants import AssetTypes
from datetime import datetime, timedelta
from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential



default_args = {
    "owner": "gauthier",
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}

def transfer_to_mlaz():
    ml_client = MLClient(
        credential=DefaultAzureCredential(),
        subscription_id="72eb7803-e874-44cb-b6d9-33f2fa3eb88c",
        resource_group_name="adelvoyerg",
        workspace_name="mlstudio-groupe3"
    )

# data_asset = ml_client.data.get("actors_2010_2019", version="1")

# df = pd.read_parquet(data_asset.path)
# df.head()


    path = '/opt/airflow/Movie_Predict/moviescraper/moviescraper/weekly_spider_2025.csv'
    file_name= "movie_tesdataasset2" # Le même nom qu'à la step d'avant
    version = "1"
    description = "movies of the week"


    new_data_asset = Data(
        path=path,
        type=AssetTypes.URI_FILE,
        name=file_name, 
        version=version,           
        description=description
    )

    ml_client.data.create_or_update(new_data_asset)


with DAG(
    dag_id="transfer_to_ml",
    default_args=default_args,
    start_date=datetime(2024, 4, 15),
    schedule_interval="@daily",
    catchup=False,
) as dag:

    t1 = PythonOperator(
        task_id="transfer_to_ml",
        python_callable=transfer_to_mlaz,
    )