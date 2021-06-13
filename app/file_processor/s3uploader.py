"""AWS S3 image uploader library."""
import boto3
from botocore.exceptions import ClientError
import logging
import uuid


def CreateBucket(bucket_prefix: str, s3_connection: object) -> (str, str):
    """Creates S3 Bucket.

    Example call:
        s3_connection = boto3.resource('s3')  # or boto3.client('s3')
        CreateBucket('MyBukect', s3_connection)

    Args:
        bucket_prefix: Bucket name prefix.
        s3_connection: Either boto3 resource or client object.__base__

    Returns:
        Tuple - created bucket name and location.
    """
    session = boto3.session.Session()
    current_region = session.region_name
    bucket_name = ''.join([bucket_prefix, str(uuid.uuid4())])
    s3_connection.create_bucket(
        Bucket=bucket_name,
        CreateBucketConfiguration={'LocationConstraint': current_region})

    return bucket_name, current_region


def UploadFile(filename: str, bucket: str, object_name: str=None) -> bool:
    """Uploads file to S3 Bucket.

    Args:
        filename: File to upload
        bucket: Bucket to upload to.
        object_name: S3 object name. If not specified then filename.

    Returns:
        True if file was uploaded, else False.
    """

    if object_name is None:
        object_name = filename

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(filename, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False

    return True
