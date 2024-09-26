from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.utils.task_group import TaskGroup
from datetime import datetime

# Função que empurra um valor para o XCom
def _t1(ti):
    ti.xcom_push(key='my_key', value=42)  # Armazena o valor 42 com a chave 'my_key'

# Função que puxa um valor do XCom
def _t2(ti):
    ti.xcom_pull(key='my_key', task_ids='t1')  # Puxa o valor armazenado por 't1'

# Função de ramificação que decide qual tarefa executar a seguir
def _branch(ti):
    value = ti.xcom_pull(key='my_key', task_ids='t1')  # Obtém o valor armazenado de 't1'
    if (value == 42):
        return 't2'  # Se o valor for 42, retorna a tarefa 't2'
    return 't3'  # Caso contrário, retorna a tarefa 't3'

# Definição do DAG
with DAG("xcom_dag", start_date=datetime(2024, 1, 1),
         schedule='@daily', catchup=False) as dag:
         
    # Tarefa que executa a função _t1
    t1 = PythonOperator(
        task_id='t1',
        python_callable=_t1
    )

    # Tarefa de ramificação que decide entre 't2' e 't3'
    branch = BranchPythonOperator(
        task_id='branch',
        python_callable=_branch
    )

    # Tarefa que executa a função _t2
    t2 = PythonOperator(
        task_id='t2',
        python_callable=_t2
    )

    # Tarefa Bash que executa um comando vazio (placeholder)
    t3 = BashOperator(
        task_id='t3',
        bash_command="echo ''"
    )

    # Outra tarefa Bash que executa um comando vazio (placeholder)
    t4 = BashOperator(
        task_id='t4',
        bash_command="echo ''"
    )

# Define a ordem de execução das tarefas
t1 >> branch >> [t2, t3] >> t4  # t1 -> branch -> (t2 ou t3) -> t4
