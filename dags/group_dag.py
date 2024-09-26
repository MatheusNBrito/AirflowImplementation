from airflow import DAG
from airflow.operators.bash import BashOperator
from groups.group_downloads import download_tasks  # Importa as tarefas de download de um módulo de grupo
from groups.group_transform import transform_tasks  # Importa as tarefas de transformação de um módulo de grupo

from datetime import datetime

# Criação do DAG com um ID único, data de início, agendamento diário e sem catchup
with DAG('group_dag', start_date=datetime(2022, 1, 1), 
         schedule_interval='@daily', catchup=False) as dag:

    # Argumentos que podem ser utilizados nas tarefas
    args = {'start_date': dag.start_date, 'schedule_interval': dag.schedule_interval, 'catchup': dag.catchup}

    # Chama a função para criar tarefas de download
    downloads = download_tasks()  

    # Tarefa para verificar se os arquivos foram baixados, simulando uma operação que leva 10 segundos
    check_files = BashOperator(
        task_id='check_files',
        bash_command='sleep 10'  # Simula a verificação dos arquivos baixados
    )

    # Chama a função para criar tarefas de transformação
    transforms = transform_tasks()  

    # Define a ordem de execução das tarefas:
    # As tarefas de download devem ser concluídas antes de verificar os arquivos,
    # e a verificação deve ser concluída antes das tarefas de transformação.
    downloads >> check_files >> transforms
