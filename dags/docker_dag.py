from airflow.decorators import task, dag  # Importa decorators para definir tarefas e DAGs
from datetime import datetime  # Importa datetime para definir datas
from airflow.providers.docker.operators.docker import DockerOperator  # Importa o operador Docker

# Define o DAG usando o decorator @dag com data de início, agendamento diário e sem catchup
@dag(start_date=datetime(2024, 1, 1), schedule_interval='@daily', catchup=False)
def docker_dag():

    @task()  # Define uma tarefa chamada t1
    def t1():
        pass  # A tarefa não realiza nenhuma operação, serve como um placeholder

    # Define a tarefa t2 que executa um comando em um contêiner Docker
    t2 = DockerOperator(
        task_id='t2',  # ID da tarefa
        image='python:3.8-slim-buster',  # Imagem Docker a ser utilizada
        command='echo "command running in the docker container"',  # Comando a ser executado dentro do contêiner
        docker_url='unix://var/run/docker.sock',  # URL do Docker
        network_mode='bridge'  # Modo de rede a ser utilizado pelo contêiner
    )

    # Define a ordem de execução das tarefas: t1 deve ser executada antes de t2
    t1() >> t2

# Invocação do DAG (não está explícita no seu código, mas é importante em um contexto real)
docker_dag()  # Chama a função para criar o DAG
