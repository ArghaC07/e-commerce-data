import boto3
import json
import os
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

 # get the bucket name from environment variable
bucket_name = os.environ['BUCKET_NAME']
input_prefix = os.environ['INPUT_PREFIX']

def lambda_handler(event, context):
    # interact with S3 and Glue
    s3 = boto3.client('s3')
    glue = boto3.client('glue')

    # get the bucket name from environment variable
    bucket_name = os.environ['BUCKET_NAME']
    input_prefix = os.environ['INPUT_PREFIX']
    
    # list objects in the S3 bucket
    try:
        response = s3.list_objects_v2(Bucket=bucket_name, 
                                  Prefix=input_prefix)
        if 'Contents' not in response:

            # how to check the file extension
            for obj in response['Contents']:
                if obj['Key'].endswith('.csv') and obj['Key'].contains('sales'):
                    logger.info('CSV File found in source bucket')
                    
                    # Extract file name without extension
                    file_name = os.path.splitext(obj['Key'])[0]
                    logger.info(f'File name without extension: {file_name}')

                    # starting the glue job
                    glue_job_name = os.environ['GLUE_JOB_NAME']
                    glue_job_run = glue.start_job_run(JobName=glue_job_name)
                    logger.info(f'Glue job started: {glue_job_run}')
                else:
                    logger.error('No CSV file found in source bucket')

    except Exception as e:
        logger.error(f'Unable to start Glue job: {e}')