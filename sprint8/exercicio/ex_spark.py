import random
from pyspark.sql import SparkSession
from pyspark.sql.functions import lit, when, col, expr

# Criar SparkSession
spark = SparkSession \
    .builder \
    .master("local[*]") \
    .appName("exercicio_spark.py") \
    .getOrCreate()

# Caminho do arquivo com nomes
import os
caminho_arquivo = os.path.join("C:", "Users", "Leide", "OneDrive", "Área de Trabalho", "PB-LEIDE-ROSARIO", "sprint8", "exercícios", "massa_de_dados")
df_dados = spark.read.csv(caminho_arquivo, header=True, inferSchema=True)

# Mostrar algumas linhas do DataFrame
df_dados.show(5)

# Etapa 2: Renomear coluna para "Nomes" e exibir esquema
df_dados = df_dados.withColumnRenamed(df_dados.columns[0], "Nomes")
df_dados.printSchema()
df_dados.show(10)

# Etapa 3: Adicionar coluna "Escolaridade"
opcoes_escolaridade = ["Fundamental", "Medio", "Superior"]
df_dados = df_dados.withColumn(
    "Escolaridade",
    expr(f"array({','.join([f'\'{e}\'' for e in opcoes_escolaridade])})[int(rand()*3)]")
)

# Etapa 4: Adicionar coluna "Pais"
opcoes_paises = [
    "Brasil", "Argentina", "Chile", "Colômbia", "Uruguai", "Paraguai",
    "Bolívia", "Peru", "Equador", "Venezuela", "Guiana", "Suriname", "Guiana Francesa"
]
df_dados = df_dados.withColumn(
    "Pais",
    expr(f"array({','.join([f'\'{p}\'' for p in opcoes_paises])})[int(rand()*13)]")
)

# Etapa 5: Adicionar coluna "AnoNascimento"
df_dados = df_dados.withColumn(
    "AnoNascimento",
    expr("1945 + int(rand()*66)")
)

# Mostrar 5 linhas após modificações
df_dados.show(5)

# Etapa 6: Selecionar pessoas nascidas neste século (2000+)
df_seculo_21 = df_dados.filter(col("AnoNascimento") >= 2000)
df_seculo_21.show(10)

# Etapa 7: Usando Spark SQL
df_dados.createOrReplaceTempView("pessoas")
df_seculo_21_sql = spark.sql("SELECT * FROM pessoas WHERE AnoNascimento >= 2000")
df_seculo_21_sql.show(10)

# Etapa 8: Contar pessoas da geração Millennials
df_millennials = df_dados.filter((col("AnoNascimento") >= 1980) & (col("AnoNascimento") <= 1994))
print(f"Millennials: {df_millennials.count()}")

# Etapa 9: Usando Spark SQL para Millennials
millennials_count = spark.sql("SELECT COUNT(*) as total FROM pessoas WHERE AnoNascimento BETWEEN 1980 AND 1994")
millennials_count.show()

# Etapa 10: Pessoas por País e Geração
df_dados = df_dados.withColumn(
    "Geracao",
    when(col("AnoNascimento").between(1944, 1964), "Baby Boomers")
    .when(col("AnoNascimento").between(1965, 1979), "Geração X")
    .when(col("AnoNascimento").between(1980, 1994), "Millennials")
    .when(col("AnoNascimento").between(1995, 2015), "Geração Z")
)

df_geracoes = df_dados.groupBy("Pais", "Geracao").count().orderBy("Pais", "Geracao")
df_geracoes.show()

# Encerra
spark.stop()
