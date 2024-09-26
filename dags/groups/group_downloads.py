from airflow import DAG  # Importa a classe DAG do Airflow
from airflow.operators.bash import BashOperator  # Importa o operador Bash para executar comandos do sistema
from airflow.utils.task_group import TaskGroup  # Importa TaskGroup para agrupar tarefas

def download_tasks():
    # Define um TaskGroup chamado "downloads" para agrupar tarefas relacionadas ao download
    with TaskGroup("downloads", tooltip="Download tasks") as group:

        # Define a primeira tarefa de download, que executa um comando Bash para "dormir" por 10 segundos
        download_a = BashOperator(
            task_id='download_a',  # Corrigido: 'donwloand_a' para 'download_a'
            bash_command='sleep 10'
        )

        # Define a segunda tarefa de download
        download_b = BashOperator(
            task_id='download_b',  # Corrigido: 'donwloand_b' para 'download_b'
            bash_command='sleep 10'
        )

        # Define a terceira tarefa de download
        download_c = BashOperator(
            task_id='download_c',  # Corrigido: 'donwloand_c' para 'download_c'
            bash_command='sleep 10'
        )

    return group  # Retorna o grupo de tarefas
