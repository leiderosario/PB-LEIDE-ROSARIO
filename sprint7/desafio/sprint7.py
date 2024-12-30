import os
import boto3
import json
from datetime import datetime
from tmdbv3api import TMDb, Discover

# Variáveis globais
TMDB_API_KEY = os.getenv('TMDB_API_KEY', 'chave_api')
LANGUAGE = 'pt-BR'
DEBUG_MODE = True
BUCKET_NAME = 'datalake-leiderosario'
GENRES = {"Drama": 18, "Romance": 10749}
YEARS = [2022, 2023]
PAGE_LIMIT = 5
BATCH_SIZE = 100

# Configuração da API TMDB
tmdb = TMDb()
tmdb.api_key = TMDB_API_KEY
tmdb.language = LANGUAGE
tmdb.debug = DEBUG_MODE

discover = Discover()
s3_client = boto3.client('s3')

def lambda_handler(event, context):
    """
    Função principal do Lambda para extração e envio de dados ao S3.
    """
    for year in YEARS:
        for genre, genre_id in GENRES.items():
            print(f"Iniciando a extração de dados para {genre} no ano de {year}.")

            # Extrair dados de filmes
            movies = fetch_data(discover, year, genre_id, media_type='movie')
            save_to_s3(movies, BUCKET_NAME, year, genre, 'movie')

            # Extrair dados de séries
            series = fetch_data(discover, year, genre_id, media_type='tv')
            save_to_s3(series, BUCKET_NAME, year, genre, 'series')

def fetch_data(discover_api, year, genre_id, media_type):
    """
    Busca dados na API do TMDb.
    """
    results = []
    page = 1
    while True:
        print(f"Fazendo requisição para {media_type} do gênero {genre_id} no ano {year}, página {page}.")
        try:
            if media_type == 'movie':
                response = discover_api.discover_movies({
                    'with_genres': genre_id,
                    'primary_release_year': year,
                    'page': page
                })
            elif media_type == 'tv':
                response = discover_api.discover_tv_shows({
                    'with_genres': genre_id,
                    'first_air_date_year': year,
                    'page': page
                })
            else:
                print(f"Tipo de mídia inválido: {media_type}.")
                break

            if not response:
                print(f"Nenhum dado encontrado para {media_type} ({genre_id}, {year}).")
                break

            results.extend(response)
            page += 1

            if page > PAGE_LIMIT:
                print("Limite de páginas atingido.")
                break
        except Exception as e:
            print(f"Erro ao buscar dados: {e}")
            break

    print(f"Coletados {len(results)} registros para {media_type} ({genre_id}, {year}).")
    return results

def save_to_s3(data, bucket, year, genre, media_type):
    """
    Salva os dados em lotes no bucket S3.
    """
    if not data:
        print(f"Nenhum dado para salvar no S3 ({media_type}, {genre}, {year}).")
        return

    chunks = [data[i:i + BATCH_SIZE] for i in range(0, len(data), BATCH_SIZE)]
    for idx, chunk in enumerate(chunks):
        now = datetime.utcnow()
        date_path = now.strftime("%Y/%m/%d")
        file_name = f"{media_type}-{genre}-{year}-{idx + 1}-{now.strftime('%H%M%S')}.json"
        path = f"Raw/TMDB/JSON/{date_path}/{file_name}"

        try:
            json_data = json.dumps(chunk, default=str)
            s3_client.put_object(
                Bucket=bucket,
                Key=path,
                Body=json_data,
                ContentType='application/json'
            )
            print(f"Arquivo salvo: {path} ({len(chunk)} registros).")
        except Exception as e:
            print(f"Erro ao salvar no S3: {e}")
