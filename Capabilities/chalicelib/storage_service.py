import boto3


class StorageService:
    def __init__(self, storage_location, config):
        self.client = boto3.client(
            's3',
            aws_access_key_id=config['ACCESS_KEY'],
            aws_secret_access_key=config['SECRET_KEY'],
            config=config['boto3_config']
        )
        self.bucket_name = storage_location

    def upload_file(self, file_bytes, file_name):
        self.client.put_object(
            Bucket=self.bucket_name,
            Body=file_bytes,
            Key=file_name
        )

        return {
            'fileId': file_name,
            'fileUrl': "http://" + self.bucket_name + ".s3.amazonaws.com/" + file_name
        }
