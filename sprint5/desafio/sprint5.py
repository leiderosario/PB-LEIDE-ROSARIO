import pandas as pd
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
localizacao = r"C:\Users\Leide\OneDrive\Área de Trabalho\PB-LEIDE-ROSARIO\Sprint5\Desafio"
nome_objeto = "ingressantes_grad.csv"
nome_bucket = 'sprint5-leide'
dado = os.path.join(localizacao, nome_objeto)

# Criação do bucket e envio do arquivo
criar_bucket(nome_bucket)
upload_arquivo(dado, nome_bucket, nome_objeto)
