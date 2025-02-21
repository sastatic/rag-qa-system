import boto3
from botocore.exceptions import ClientError
from common.config import AWS_REGION, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY


def create_s3_client():
    try:
        s3_client = boto3.client(
            "s3",
            region_name=AWS_REGION,
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        )
        return s3_client
    except ClientError as e:
        print(f"Error creating S3 client: {e}")
        raise
