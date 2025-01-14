import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

# Configuração do job do AWS Glue
args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Lendo o arquivo JSON do Amazon S3
datasource = glueContext.create_dynamic_frame.from_options(
    connection_type="s3",
    connection_options={"paths": ["s3://your-bucket-name/movies.json"]},
    format="json"
)

# Filtrando filmes da década de 90 a 2000 e do gênero Drama
filtered_df = Filter.apply(
    frame=datasource,
    f=lambda x: int(x["anoLancamento"]) >= 1990 and int(x["anoLancamento"]) <= 2000 and "Drama" in x["genero"]
)

# Gravando o resultado em outro formato
glueContext.write_dynamic_frame.from_options(
    frame=filtered_df,
    connection_type="s3",
    connection_options={"path": "s3://your-bucket-name/output/"},
    format="parquet"
)

job.commit()
