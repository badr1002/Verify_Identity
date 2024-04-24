from flask import request
import boto3
import botocore.exceptions
from decouple import config


S3_ENDPOINT_URL = config("S3_ENDPOINT_URL")
S3_BUCKET_NAME = config("S3_BUCKET_NAME")
S3_ACCESS_KEY_ID = config("S3_ACCESS_KEY_ID")
S3_SECRET_ACCESS_KEY = config("S3_SECRET_ACCESS_KEY")

 
def upload_file(file):
    try:
        # Check if the request contains the file part
        if file is None:
            return 'No file part'

        # If the user does not select a file, the browser submits an empty file without a filename
        if file.filename == '':
            return 'No selected file'

        # Create an S3 client
        s3 = boto3.client('s3', endpoint_url=S3_ENDPOINT_URL, aws_access_key_id=S3_ACCESS_KEY_ID,
                          aws_secret_access_key=S3_SECRET_ACCESS_KEY)

        # Upload file to S3 bucket
        s3.upload_fileobj(file, S3_BUCKET_NAME, 'verification/'+file.filename)
        # return url
        return f'{'https://provider.mypractice.clinic'}/{S3_BUCKET_NAME}/verification/{file.filename}'

    except botocore.exceptions.ClientError as e:
         return False
    
    
    


# handle delete file
def delete_file(file_name):
    try:
        # Create an S3 client
        s3 = boto3.client('s3', endpoint_url=S3_ENDPOINT_URL, aws_access_key_id=S3_ACCESS_KEY_ID,
                          aws_secret_access_key=S3_SECRET_ACCESS_KEY)

        # Delete file from S3 bucket
        s3.delete_object(Bucket=S3_BUCKET_NAME, Key="verification/"+file_name)
        return 'File deleted successfully'

    except botocore.exceptions.ClientError as e:
        return f'Error deleting file from S3 bucket: {e.response["Error"]["Code"]} - {e.response["Error"]["Message"]}'
    