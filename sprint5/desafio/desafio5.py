import pandas as pd
import boto3
from botocore.exceptions import ClientError
import os
import tempfile
from datetime import datetime

# Configurações do cliente S3
s3_dowload = boto3.client('s3')
nome_bucket = 'sprint5-leide'
nome_objeto = "ingressantes_grad.csv"

# Caminho temporário para o arquivo
pasta_dowload = os.path.join(tempfile.gettempdir(), "ingressantes_grad.csv")

# Função para fazer download do arquivo do S3
def download_arquivo(nome_bucket, nome_objeto, caminho_destino):
    try:
        s3_dowload.download_file(nome_bucket, nome_objeto, caminho_destino)
        print(f"Arquivo {nome_objeto} baixado com sucesso.")
    except ClientError as e:
        print(f"Erro ao baixar o arquivo: {e}")

# Baixar o arquivo do S3 para a pasta temporária
download_arquivo(nome_bucket, nome_objeto, pasta_dowload)

# Agora podemos ler o arquivo CSV baixado
df = pd.read_csv(pasta_dowload, encoding='latin1', delimiter=';')

# 4.1. Cláusula com dois operadores lógicos
filtered_df = df[(df["CURSO"].str.contains("CIÊNCIAS BIOLÓGICAS")) & (df["ANO"] >= 2012)]

# 4.2. Funções de Agregação
agg_total = df.groupby("TURNO")["QUANTIDADE"].sum()
agg_mean = df.groupby("ANO")["QUANTIDADE"].mean()

# 4.3. Função Condicional
df["CATEGORIA_TURNO"] = df["TURNO"].apply(lambda x: "DIURNO" if x == "DIURNO" else "OUTRO")

# 4.4. Função de Conversão
df["ANO_STR"] = df["ANO"].astype(str).apply(lambda x: f"Ano-{x}")

# 4.5. Função de Data (corrigida)
df["DATA"] = df.apply(lambda row: datetime.strptime(f"{row['ANO']}-{6 * (row['SEM'] - 1) + 1}-01", "%Y-%m-%d") if row['SEM'] in [1, 2] else None, axis=1)

# 4.6. Função de String
df["SIGLA_CURSO"] = df["CURSO"].apply(lambda x: x.split("-")[0])

# Salvar o DataFrame modificado em um arquivo CSV chamado 'estudantes.csv'
df.to_csv("estudantes.csv", index=False)

# Função para fazer upload de arquivo
def upload_arquivo(file_path, nome_bucket, nome_arquivo):
    s3_criacao = boto3.client('s3')
    try:
        s3_criacao.upload_file(file_path, nome_bucket, nome_arquivo)
        print(f"Arquivo {file_path} enviado com sucesso para o S3.")
    except ClientError as e:
        print(f"Erro ao enviar o arquivo: {e}")

# Enviar o arquivo 'estudantes.csv' para o S3
upload_arquivo("estudantes.csv", nome_bucket, "estudantes.csv")