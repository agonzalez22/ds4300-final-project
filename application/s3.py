import boto3
from dotenv import load_dotenv
import os 

load_dotenv()

def ingest_to_s3(filename, f, bucketname="ds4300-raw-slicedbread"): 
    """ passes a file into the bucket"""
    s3 = boto3.client(
    's3',
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_DEFAULT_REGION")
    )

    s3.upload_fileobj(
    Fileobj=f,
    Bucket=bucketname,
    Key=filename
    )
