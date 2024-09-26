from airflow import DAG, Dataset
from airflow.decorators import task
from datetime import datetime

# Define dois datasets que serão utilizados no DAG
my_file = Dataset("/tmp/my_file.txt")  # Primeiro dataset
my_file_2 = Dataset("/tmp/my_file_2.txt")  # Segundo dataset

# Definição do DAG com um ID único, agendamento diário, data de início e sem catchup
with DAG (
    dag_id="producer",
    schedule="@daily",  # O DAG será executado diariamente
    start_date=datetime(2024, 1, 1),  # Data de início da execução do DAG
    catchup=False  # Não executará tarefas pendentes ao iniciar
):
    
    # Define uma tarefa que atualiza o primeiro dataset
    @task(outlets=[my_file])  # Indica que este task atualizará o dataset my_file
    def update_dataset():
        # Abre o arquivo em modo append e escreve uma linha
        with open(my_file.uri, "a+") as f:
            f.write("producer update\n")  # Adiciona uma nova linha ao arquivo

    update_dataset()  # Chama a função para executar a tarefa

    # Define uma segunda tarefa que atualiza o segundo dataset
    @task(outlets=[my_file_2])  # Indica que este task atualizará o dataset my_file_2
    def update_dataset_2():
        # Abre o segundo arquivo em modo append e escreve uma linha
        with open(my_file_2.uri, "a+") as f:
            f.write("producer update\n")  # Adiciona uma nova linha ao arquivo

    # Define a ordem de execução: update_dataset deve ser executada antes de update_dataset_2
    update_dataset() >> update_dataset_2()  # O operador de deslocamento define a sequência
