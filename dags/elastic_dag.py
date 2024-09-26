from airflow import DAG
from airflow.operators.python import PythonOperator
from hooks.elastic.elastic_hook import ElasticHook  # Importa o hook para interação com o Elasticsearch

from datetime import datetime

# Define a função que será executada pelo PythonOperator
def _print_es_info():
    hook = ElasticHook()  # Cria uma instância do ElasticHook
    print(hook.info())  # Imprime informações do Elasticsearch usando o hook

# Criação do DAG com um ID único, data de início, agendamento diário e sem catchup
with DAG('elastic_dag', start_date=datetime(2024, 1, 1), schedule_interval='@daily', catchup=False) as dag:

    # Define uma tarefa que executa a função _print_es_info
    print_es_info = PythonOperator(
        task_id='print_es_info',
        python_callable=_print_es_info  # A função a ser chamada pela tarefa
    )
