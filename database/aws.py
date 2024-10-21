import boto3

s3 = boto3.client('s3')

def upload_to_s3(file_name, bucket, object_name=None):
    if object_name is None:
        object_name = file_name
    s3.upload_file(file_name, bucket, object_name)
