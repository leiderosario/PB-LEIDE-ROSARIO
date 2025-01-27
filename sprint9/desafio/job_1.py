# JOB Simplificado para Processamento de Filmes

import sys
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.utils import getResolvedOptions
from pyspark.sql.functions import col, current_date
from pyspark.sql.types import IntegerType

# Obter argumentos do Glue
args = getResolvedOptions(sys.argv, ['JOB_NAME'])

# Inicializar Spark e Glue Context
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Carregar os dados do CSV
caminho_csv = "C:\Users\Leide\OneDrive\Área de Trabalho\PB-LEIDE-ROSARIO\sprint9\movies.csv"
movies_df = spark.read.csv(caminho_csv, header=True, inferSchema=True)


# Função para limpar e filtrar os dados
def limpar_e_filtrar(df):
    return (df.replace(["\\n", ""], None)
              .dropna(how="any")
              .filter((col("anoLancamento") >= 2010) & (col("anoLancamento") <= 2023)))

# Caminhos no S3
CAMINHO_BASE = "s3://sprint9-leide"
CAMINHO_BRUTO = f"{CAMINHO_BASE}/Raw/Local/CSV/movies.csv"
CAMINHO_CONFIAVEL = f"{CAMINHO_BASE}/Trusted/Parquet/movies"

# Caminho do arquivo de entrada para filmes
caminho_filmes = f"{CAMINHO_BRUTO}/Users\Leide\OneDrive\Área de Trabalho\PB-LEIDE-ROSARIO\sprint9\movies.csv"

# Ler e processar arquivo CSV de filmes
df_filmes = (spark.read.csv(caminho_filmes, header=True, inferSchema=True, sep="|")
                  .withColumn("anoLancamento", col("anoLancamento").cast(IntegerType()))
                  .withColumn("tempoMinutos", col("tempoMinutos").cast(IntegerType()))
                  .withColumn("numeroVotos", col("numeroVotos").cast(IntegerType()))
                  .withColumn("notaMedia", col("notaMedia").cast("double"))
                  .withColumn("processed_date", current_date()))

# Limpar e filtrar os dados
df_filmes_limpo = limpar_e_filtrar(df_filmes)

# Filtrar por gênero (Romance e Drama)
df_filmes_filtrado = df_filmes[(df_filmes['genero'] == 'Romance') | (df_filmes['genero'] == 'Drama')]

# Filtrar filmes da década de 90 e 2000
movies_filtered = movies_df.filter(
    (col("release_year").between(1990, 1999)) | (col("release_year").between(2000, 2009))
)

# Selecionar os 10 maiores campeões de bilheteria por década
top_movies_90 = (
    movies_filtered.filter(col("release_year").between(1990, 1999))
    .orderBy(desc("revenue"))
    .limit(10)
)
top_movies_2000 = (
    movies_filtered.filter(col("release_year").between(2000, 2009))
    .orderBy(desc("revenue"))
    .limit(10)
)

# Combinar os dois dataframes
top_movies = top_movies_90.union(top_movies_2000)

# Análise dos gêneros Drama e Romance
genres_analysis = (
    top_movies.withColumn("genres", explode(split(col("genres"), "\\|")))  # Separar gêneros
    .filter((col("genres") == "Drama") | (col("genres") == "Romance"))
)

# Comparar quantidade de filmes por gênero
genre_count = genres_analysis.groupBy("genres").count()

# Tendência de popularidade e avaliação por gênero
popularity_rating = genres_analysis.groupBy("genres").agg(
    avg("popularity").alias("avg_popularity"),
    avg("vote_average").alias("avg_rating"),
)

# Comparar idade dos atores
actors_analysis = (
    genres_analysis.withColumn("actor_age", col("release_year") - col("actor_birth_year"))
    .groupBy("genres")
    .agg(avg("actor_age").alias("avg_actor_age"))
)

# Mostrar os resultados
print("Quantidade de filmes por gênero:")
genre_count.show()

print("Popularidade e avaliação por gênero:")
popularity_rating.show()

print("Idade média dos atores por gênero:")
actors_analysis.show()

# Escrever em formato Parquet
df_filmes_limpo.write.mode("overwrite").parquet(f"{CAMINHO_CONFIAVEL}/Movies")
print("Dados de Filmes processados e salvos.")

# Finalizar Job
print("Processamento concluído.")
job.commit()
