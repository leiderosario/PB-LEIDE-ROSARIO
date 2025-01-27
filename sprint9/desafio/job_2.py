# JOB para Processamento de Dados de Filmes TMDB

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

# Função para limpar e filtrar os dados
def limpar_e_filtrar(df):
    return (df.replace(["\\n", ""], None)
              .dropna(how="any")
              .filter((col("anoLancamento") >= 2010) & (col("anoLancamento") <= 2023)))

# Caminhos no S3
CAMINHO_BRUTO = "s3://sprint9-leide/Raw/TMDB/JSON/2025/01/13/"
CAMINHO_CONFIAVEL = "s3://sprint9-leide/Trusted/Parquet/Movies/"

# Ler e processar arquivos JSON de filmes
df_filmes = (spark.read.json(CAMINHO_BRUTO)
                  .withColumn("anoLancamento", col("release_date").substr(1, 4).cast(IntegerType()))
                  .withColumn("popularity", col("popularity").cast("double"))
                  .withColumn("vote_average", col("vote_average").cast("double"))
                  .withColumn("processed_date", current_date()))

# Limpar e filtrar os dados
df_filmes_limpo = limpar_e_filtrar(df_filmes)

# Escrever os dados no formato Parquet particionado por data de processamento
df_filmes_limpo.write.mode("overwrite").partitionBy("processed_date").parquet(CAMINHO_CONFIAVEL)
print("Dados de Filmes TMDB processados e salvos.")

# Finalizar Job
print("Processamento concluído.")
job.commit()
