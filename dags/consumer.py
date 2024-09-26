from airflow import DAG, Dataset  # Importa DAG e Dataset do Airflow
from airflow.decorators import task  # Importa o decorator task para definir tarefas
from datetime import datetime  # Importa datetime para definir a data de início

# Define dois datasets que serão utilizados no DAG
my_file = Dataset("/tmp/my_file.txt")  # Dataset para o arquivo my_file.txt
my_file_2 = Dataset("/tmp/my_file_2.txt")  # Dataset para o arquivo my_file_2.txt

# Define o DAG com um ID, agendamento baseado nos datasets, data de início e catchup desativado
with DAG(
    dag_id="consumer",
    schedule=[my_file, my_file_2],  # O DAG será acionado quando os datasets forem atualizados
    start_date=datetime(2024, 1, 1),  # Data de início do DAG
    catchup=False  # Desabilita o catchup, para não executar tarefas pendentes em datas passadas
):

    @task  # Define uma tarefa chamada read_dataset
    def read_dataset():
        # Abre o arquivo associado ao dataset my_file em modo de leitura e escrita
        with open(my_file.uri, "a+") as f:
            f.seek(0)  # Move o ponteiro do arquivo para o início para ler o conteúdo
            print(f.read())  # Lê e imprime o conteúdo do arquivo

    read_dataset()  # Executa a tarefa read_dataset
