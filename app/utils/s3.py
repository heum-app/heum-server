import boto3
import os
from fastapi import UploadFile
import uuid

# .env에서 설정값 읽기
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
BUCKET_NAME = os.getenv("AWS_S3_BUCKET_NAME")
REGION = os.getenv("AWS_REGION")

s3_client = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=REGION
)

def upload_image_to_s3(file: UploadFile):
    """S3에 이미지를 업로드하고 URL을 반환합니다."""
    # 파일명 중복 방지를 위한 랜덤 이름 생성
    ext = file.filename.split(".")[-1]
    filename = f"profiles/{uuid.uuid4()}.{ext}"
    
    try:
        s3_client.upload_fileobj(
            file.file,
            BUCKET_NAME,
            filename,
            ExtraArgs={
                "ContentType": file.content_type  # 이미지로 바로 인식되게 설정
            }
        )
        # 업로드된 파일의 퍼블릭 URL 반환
        return f"https://{BUCKET_NAME}.s3.{REGION}.amazonaws.com/{filename}"
    except Exception as e:
        print(f"S3 업로드 에러: {e}")
        raise Exception(f"S3 업로드 에러: {str(e)}")

def delete_image_from_s3(image_url: str):
    """S3에서 이미지를 삭제합니다."""
    try:
        # URL에서 버킷명과 파일 키 추출
        # URL 형식: https://{BUCKET_NAME}.s3.{REGION}.amazonaws.com/{filename}
        if not image_url.startswith(f"https://{BUCKET_NAME}.s3.{REGION}.amazonaws.com/"):
            return False
        
        key = image_url.replace(f"https://{BUCKET_NAME}.s3.{REGION}.amazonaws.com/", "")
        
        s3_client.delete_object(
            Bucket=BUCKET_NAME,
            Key=key
        )
        return True
    except Exception as e:
        print(f"S3 삭제 에러: {e}")
        return False