import logging
import boto3
import sqlalchemy
import pandas as pd
from io import BytesIO

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def read_csv_from_s3(s3_client, bucket_input, file_input):
    obj = s3_client.get_object(Bucket=bucket_input, Key=file_input)
    df = pd.read_csv(obj['Body'], sep=',')
    logger.info(f"Read {file_input}")
    return df

def filter_df(df):
    logger.info("Filtering df")
    return df.head()


def write_df_to_s3(s3_client, bucket_output, df, file_input_name):
    try:
        file = BytesIO()
        df.to_parquet(file)
        file.seek(0)
    except Exception:
        logger.info(f"Couldn't convert {file_input_name} to parquet")

    try:
        s3_client.put_object(Bucket=bucket_output, Body=file.read(), Key=file_input_name+'.parquet')
    except Exception:
        logger.info(f"Could write {file_input_name} to {bucket_output}")

    logger.info(f"{file_input_name} is written to {bucket_output}")


def write_df_to_db(df, file_input_name, rds_username, rds_host, rds_user_pwd, rds_db_name):
    try:
        engine = sqlalchemy.create_engine('postgresql+psycopg2://{0}:{1}@{2}/{3}'
                                      .format(rds_username, rds_user_pwd, rds_host, rds_db_name)).connect()
    except Exception:
        logger.info(f"Couldn't connect to {rds_db_name}")

    try:
        df.to_sql('iris', con=engine)
    except Exception:
        logger.info(f"Couldn't create table {file_input_name} in {rds_db_name}")

    logger.info(f"{file_input_name} is written to {rds_db_name}")
