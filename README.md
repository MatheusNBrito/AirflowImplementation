# Passo a Passo para Rodar um Projeto Airflow

## 1. Instalação do Apache Airflow

### Pré-requisitos:
- Tenha Python (3.6 ou superior) e pip instalados em sua máquina.
- Instale o Docker (veja a seção abaixo).

### Criar um ambiente virtual (opcional, mas recomendado):
``bash
python -m venv airflow_venv
source airflow_venv/bin/activate  # No Windows use: airflow_venv\Scripts\activate
Instalar o Docker:
No Linux:
Atualize o índice de pacotes:

bash
Copiar código
sudo apt-get update
Instale os pacotes necessários:

bash
Copiar código
sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    software-properties-common
Adicione a chave GPG do Docker:

bash
Copiar código
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
Adicione o repositório do Docker:

bash
Copiar código
sudo add-apt-repository \
    "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
    $(lsb_release -cs) \
    stable"
Instale o Docker:

bash
Copiar código
sudo apt-get update
sudo apt-get install docker-ce
Verifique se o Docker está instalado corretamente:

bash
Copiar código
sudo docker run hello-world
No Windows:
Baixe e instale o Docker Desktop.
Siga as instruções de instalação do assistente.
Verifique se o Docker está instalado corretamente executando o seguinte comando no PowerShell:
bash
Copiar código
docker run hello-world
Instalar o Apache Airflow:
Use a seguinte linha de comando para instalar o Airflow. Ajuste a versão conforme necessário:

bash
Copiar código
export AIRFLOW_VERSION=2.7.0
export PYTHON_VERSION="$(python --version | cut -d ' ' -f 2 | cut -d '.' -f 1-2)"
export CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"

pip install "apache-airflow==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"


# Tópicos Abordados
1. XCom DAG
Objetivo: Transferir dados entre tarefas usando XCom.
Descrição: Implementei um DAG que utiliza Python e Bash para empurrar e puxar dados entre tarefas, permitindo um fluxo de trabalho dinâmico e baseado em condições.

2. User Processing
Objetivo: Processar e armazenar informações de usuários.
Descrição: Criei um DAG que extrai dados de uma API, processa essas informações e armazena em um banco de dados PostgreSQL. Utilizei operadores como PostgresOperator e HttpSensor para garantir a disponibilidade da API antes de realizar a extração.

3. Parallel Processing DAG
Objetivo: Executar tarefas em paralelo para otimização de tempo.
Descrição: Estruturei um DAG que permite a execução simultânea de tarefas de extração e carregamento, utilizando o BashOperator para simular processos que podem ser realizados em paralelo.

4. Dockerized Tasks
Objetivo: Executar comandos em containers Docker.
Descrição: Integrei o DockerOperator para executar comandos dentro de containers, demonstrando minha capacidade de trabalhar em ambientes isolados e escaláveis.

5. Dataset Management
Objetivo: Gerenciar e atualizar datasets utilizando Airflow.
Descrição: Utilizei o conceito de Dataset do Airflow para atualizar e ler arquivos em um fluxo de trabalho, mostrando a capacidade de manipular dados de forma eficiente e organizada.

Tecnologias Utilizadas
Apache Airflow: Para orquestração de workflows.
Python: Para tarefas de processamento e integração.
Bash: Para execução de comandos do sistema.
PostgreSQL: Para armazenamento de dados.
Docker: Para execução de tarefas em ambientes isolados.
Conclusão
Esses projetos me permitiram aprofundar meus conhecimentos em orquestração de workflows, manipulação de dados e automação de processos.
