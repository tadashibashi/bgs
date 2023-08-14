import os
import boto3
from botocore.client import BaseClient

from mypy_boto3_s3 import Client

def boto3_client(service_name: str) -> BaseClient | Client:
    """
        Get boto3 client with keys from the environment automatically added
    """
    return boto3.client(service_name,
                        aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
                        aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"])

def s3_client() -> Client:
    return boto3_client("s3")

_base_url: str = ""

def get_base_url() -> str:
    global _base_url
    if not _base_url:
        _base_url = os.environ["S3_BASE_URL"]
    return _base_url

_bucket: str = ""

def get_bucket_name() -> str:
    global _bucket
    if not _bucket:
        _bucket = os.environ["S3_BUCKET"]
    return _bucket