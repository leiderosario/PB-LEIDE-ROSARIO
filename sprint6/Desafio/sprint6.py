
import boto3
from botocore.exceptions import ClientError
import os

# Função para criar bucket
def criar_bucket(nome_bucket, region="us-east-1"):
    s3_criacao = boto3.client('s3', region_name=region)
    try:
        s3_criacao.head_bucket(Bucket=nome_bucket)
    except ClientError:
        s3_criacao.create_bucket(Bucket=nome_bucket)


# Função para fazer upload de arquivo
def upload_arquivo(file_path, nome_bucket, nome_objeto):
    s3_criacao = boto3.client('s3')
    try:
        s3_criacao.upload_file(file_path, nome_bucket, nome_objeto)
    except ClientError as e:
        print(f"Erro ao enviar o arquivo: {e}")

# Localização do arquivo e configurações
localizacao = r"/data/"
nome_objeto_filmes = "Raw/Local/CSV/Movies/2024/12/16/movies.csv"
nome_objeto_series = "Raw/Local/CSV/Series/2024/12/16/series.csv"
nome_bucket = 'datalake-leiderosario'
dado_filmes = '/data/movies.csv'
dado_series = '/data/series.csv'

# função para a criação do bucket e envio do arquivo
criar_bucket(nome_bucket)
upload_arquivo(dado_filmes, nome_bucket, nome_objeto_filmes)
upload_arquivo(dado_series, nome_bucket, nome_objeto_series)