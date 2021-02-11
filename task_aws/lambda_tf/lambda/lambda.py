import logging
import boto3
import os
from clib import read_csv_from_s3, filter_df, write_df_to_s3, write_df_to_db


logger = logging.getLogger()
logger.setLevel(logging.INFO)


INPUT_BUCKET_NAME = os.environ['INPUT_BUCKET_NAME']
OUTPUT_BUCKET_NAME = os.environ['OUTPUT_BUCKET_NAME']
DB_HOST = os.environ['DB_HOST']
DB_NAME = os.environ['DB_NAME']
DB_USERNAME = os.environ['DB_USERNAME']
DB_PASSWORD = os.environ['DB_PASSWORD']


def lambda_handler(event, context):
    try:
        try:
            for record in event['Records']:
                bucket_input = record['s3']['bucket']['name']
                file_input = record['s3']['object']['key']
                file_input_name = file_input.split('.csv')[0]
                logger.info(f'Handling {file_input}')
        except Exception:
            logger.info("Couldn't collect file")

            s3_client = boto3.client('s3')
            df = read_csv_from_s3(s3_client, bucket_input, file_input)
            filtered_df = filter_df(df)
            write_df_to_s3(s3_client, OUTPUT_BUCKET_NAME, filtered_df, file_input_name)
            write_df_to_db(filtered_df, file_input_name, DB_NAME, DB_HOST, DB_PASSWORD, DB_USERNAME)
            logger.info(f"Finished with {file_input_name}")

    except Exception:
        logger.info("Couldn't perform lambda")
