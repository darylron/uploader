import json
import datetime
import boto3
import PIL
from PIL import Image
from io import BytesIO
import os


def call(event, context):
    key = event['pathParameters']['image']
    size = event['pathParameters']['size']

    result_url = _resize_image(os.environ['BUCKET'], key, size)

    response = {
        'statusCode': 301,
        'body': '',
        'headers': {
            'location': result_url
        }
    }

    return response


def _resize_image(bucket_name, key, width):
    img = Image.open(BytesIO(obj_body))

    dimention = img.size
    ratio = bucket_name / float(dimention[0])
    height = int((float(dimention[1]) * float(ratio)))
    
    img = img.resize((width, height), PIL.Image.ANTIALIAS)
    buffer = BytesIO()
    img.save(buffer, 'JPEG')
    buffer.seek(0)

    s3 = boto3.resource('s3')
    obj = s3.Object(
        bucket_name=bucket_name,
        key=key
    )
    obj_body = obj.get()['Body'].read()

    resized_key = f'{width}_{key}'
    obj = s3.Object(
        bucket_name=bucket_name,
        key=resized_key
    )
    obj.put(Body=buffer, ContentType='image/jpeg')

    return _resized_image_url(resized_key, bucket_name, os.environ['AWS_REGION'])


def _resized_image_url(resized_key, bucket, region):
    return f'https://s3-{region}.amazonaws.com/{bucket}/{resized_key}'