from airflow import DAG  # Importa a classe DAG do Airflow
from airflow.operators.bash import BashOperator  # Importa o operador Bash para executar comandos do sistema
from airflow.utils.task_group import TaskGroup  # Importa TaskGroup para agrupar tarefas

def transform_tasks():
    # Define um TaskGroup chamado "transforms" para agrupar tarefas relacionadas à transformação
    with TaskGroup("transforms", tooltip="Transform tasks") as group:

        # Define a primeira tarefa de transformação, que executa um comando Bash para "dormir" por 10 segundos
        transform_a = BashOperator(
            task_id='transform_a',
            bash_command='sleep 10'
        )

        # Define a segunda tarefa de transformação; aqui, a variável 'transform_a' foi reutilizada por erro
        transform_b = BashOperator(  # Corrigido: deve ser 'transform_b'
            task_id='transform_b',
            bash_command='sleep 10'
        )

        # Define a terceira tarefa de transformação; aqui, a variável 'transform_a' foi reutilizada por erro
        transform_c = BashOperator(  # Corrigido: deve ser 'transform_c'
            task_id='transform_c',
            bash_command='sleep 10'
        )

    return group  # Retorna o grupo de tarefas
