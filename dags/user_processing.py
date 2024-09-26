from airflow import DAG
from datetime import datetime
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.providers.http.sensors.http import HttpSensor
from airflow.operators.python import PythonOperator
import json
from pandas import json_normalize
from airflow.providers.postgres.hooks.postgres import PostgresHook

# Função para processar os dados do usuário
def _process_user(ti):
    # Puxa os dados do usuário da tarefa 'extract_user'
    user = ti.xcom_pull(task_ids="extract_user")
    user = user['results'][0]  # Seleciona o primeiro usuário
    # Normaliza os dados do usuário e transforma em DataFrame
    process_user = json_normalize({
        'firstname': user['name']['first'],
        'lastname': user['name']['last'],
        'country': user['location']['country'],
        'username': user['login']['username'],
        'password': user['login']['password'],
        'email': user['email']
    })
    # Salva os dados processados em um arquivo CSV
    process_user.to_csv('/tmp/processed_user.csv', index=None, header=False)

# Função para armazenar os dados do usuário no banco de dados
def _store_user():
    hook = PostgresHook(postgres_conn_id='postgres')  # Cria um hook para se conectar ao PostgreSQL
    # Copia os dados do CSV para a tabela 'users' no banco de dados
    hook.copy_expert(
        sql="COPY users FROM stdin WITH DELIMITER ','",
        filename='/tmp/processed_user.csv'
)

# Definição do DAG
with DAG('user_processing', start_date=datetime(2024, 1, 1),
         schedule_interval='@daily', catchup=False) as dag:

    # Tarefa que cria a tabela 'users' no banco de dados, se não existir
    create_table = PostgresOperator(
        task_id='create_table',
        postgres_conn_id='postgres',
        sql='''        
            CREATE TABLE IF NOT EXISTS users (
                firstname TEXT NOT NULL,
                lastname TEXT NOT NULL,
                country TEXT NOT NULL,
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                email TEXT NOT NULL
            );
        '''
    )

    # Sensor que verifica se a API está disponível
    is_api_available = HttpSensor(
        task_id='is_api_available',
        http_conn_id='user_api',
        endpoint='api/'
    )

    # Tarefa que extrai dados do usuário da API
    extract_user = SimpleHttpOperator(
        task_id='extract_user',
        http_conn_id='user_api',
        endpoint='api/', 
        method='GET',
        response_filter=lambda response: json.loads(response.text),  # Converte a resposta JSON
        log_response=True  # Registra a resposta da API
    )

    # Tarefa que processa os dados do usuário
    process_user = PythonOperator(
        task_id='process_user',
        python_callable=_process_user
    )
    
    # Tarefa que armazena os dados processados no banco de dados
    store_user = PythonOperator(
        task_id='store_user',
        python_callable=_store_user
    )

    # Define a ordem de execução das tarefas
    create_table >> is_api_available >> extract_user >> process_user >> store_user
