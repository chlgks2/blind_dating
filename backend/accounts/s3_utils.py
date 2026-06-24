import boto3
import uuid
from django.conf import settings

s3_client = boto3.client(
    's3',
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.AWS_S3_REGION,
)

BUCKET = settings.AWS_S3_BUCKET


def upload_fileobj(file_obj, folder='originals'):
    """파일 객체를 S3에 업로드하고 공개 URL 반환"""
    ext = file_obj.name.split('.')[-1] if hasattr(file_obj, 'name') else 'jpg'
    key = f'{folder}/{uuid.uuid4()}.{ext}'

    s3_client.upload_fileobj(file_obj, BUCKET, key)

    url = f'https://{BUCKET}.s3.{settings.AWS_S3_REGION}.amazonaws.com/{key}'
    return url, key


def upload_bytes(data_bytes, folder='generated', ext='png'):
    """바이트 데이터를 S3에 업로드 (워커가 결과 올릴 때 사용)"""
    key = f'{folder}/{uuid.uuid4()}.{ext}'
    s3_client.put_object(Bucket=BUCKET, Key=key, Body=data_bytes,
                         ContentType=f'image/{ext}')
    url = f'https://{BUCKET}.s3.{settings.AWS_S3_REGION}.amazonaws.com/{key}'
    return url, key
