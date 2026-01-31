import boto3
from app.config import settings
from botocore.config import Config

get_settings = settings()
s3_client = boto3.client(
    's3',
    aws_access_key_id=get_settings.AWS_ACCESS_KEY,
    aws_secret_access_key=get_settings.AWS_SECRET_ACCESS_KEY,
    region_name=get_settings.AWS_REGION,
    config=Config(
        signature_version='s3v4',
        retries={'max_attempts': 5},
        s3={'addressing_style': 'virtual'}
    )
)
