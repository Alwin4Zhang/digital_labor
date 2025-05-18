import os
import io
import base64
from minio import Minio
from minio.error import S3Error

minio_client = Minio('localhost:9000',
                    access_key='VZKlM07CpRhJq0ut3kp3',
                    secret_key='1VKG8NWjGBTZJx18H3dJsR32nXQidl5zXBjrtvSl',
                    secure=False
                    )

bucket_name = "digital-labor"
if minio_client.bucket_exists(bucket_name=bucket_name):  # bucket_exists：检查桶是否存在
    print("该存储桶已经存在")
else:
    minio_client.make_bucket(bucket_name=bucket_name)
    print("存储桶创建成功")


def upload_object(file_path,
                  object_name,
                  content_type,
                  bucket_name=bucket_name):
    """上传文件到minio
    file_path: 文件路径
    object_name: 上传后的文件名称
    content_type: 文件类型
    bucket_name: bucket桶名称
    """
    # 上传图片到Minio
    try:
        minio_client.fput_object(
            bucket_name=bucket_name,
            object_name=object_name,
            file_path=file_path,
            content_type=content_type
        )
        print(f"文件 {file_path} 上传成功")
    except Exception as e:
        print(e)

def upload_base64image(base64img,
                  object_name,
                  content_type="image/jpeg",
                  bucket_name=bucket_name):
    """上传文件到minio
    base64img: base64图片
    object_name: 上传后的文件名称
    content_type: 文件类型
    bucket_name: bucket桶名称
    """
    # 上传图片到Minio
    try:
        img_data = base64.b64decode(base64img)
        minio_client.fput_object(
            bucket_name,
            object_name,
            io.BytesIO(img_data),
            length=-1, 
            part_size=10 * 1024 * 1024, 
            content_type=content_type
        )
        print(f"图片上传成功!")
    except Exception as e:
        print(e)

def get_presiged_url(object_name,bucket_name=bucket_name):
    """从bucket桶中获取对象url
    object_name: 对象名称
    bucket_name: 桶名称
    """

    return minio_client.get_presigned_url(
        "GET",
        bucket_name=bucket_name,
        object_name=object_name
    )