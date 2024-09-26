from airflow import DAG
from airflow.operators.bash import BashOperator

from datetime import datetime

# Definição do DAG com um ID único, data de início, agendamento diário e sem catchup
with DAG('parallel_dag', start_date=datetime(2022, 1, 1), 
         schedule_interval='@daily', catchup=False) as dag:

    # Tarefa para extrair dados A, que simula uma operação que leva 10 segundos
    extract_a = BashOperator(
        task_id='extract_a',
        bash_command='sleep 10'  # Simula uma tarefa de extração
    )

    # Tarefa para extrair dados B, também simulando uma operação de 10 segundos
    extract_b = BashOperator(
        task_id='extract_b',
        bash_command='sleep 10'  # Simula uma tarefa de extração
    )

    # Tarefa para carregar dados A, com uma simulação de 10 segundos
    load_a = BashOperator(
        task_id='load_a',
        bash_command='sleep 10'  # Simula uma tarefa de carregamento
    )

    # Tarefa para carregar dados B, igualmente simulando uma operação de 10 segundos
    load_b = BashOperator(
        task_id='load_b',
        bash_command='sleep 10'  # Simula uma tarefa de carregamento
    )

    # Tarefa de transformação, que simula uma operação mais demorada de 30 segundos
    transform = BashOperator(
        task_id='transform',
        queue='high_cpu',  # Especifica a fila de alta CPU para esta tarefa
        bash_command='sleep 30'  # Simula uma tarefa de transformação
    )

    # Define a ordem de execução:
    # 'extract_a' deve ser concluída antes de 'load_a'
    extract_a >> load_a
    
    # 'extract_b' deve ser concluída antes de 'load_b'
    extract_b >> load_b
    
    # 'transform' deve ser executada após a conclusão de 'load_a' e 'load_b'
    [load_a, load_b] >> transform
