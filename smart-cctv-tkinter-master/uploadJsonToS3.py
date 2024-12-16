import boto3
from botocore.exceptions import NoCredentialsError

def upload():
    def upload_to_s3(file_name, bucket_name, object_name=None):
        """
        Upload a file to an S3 bucket.

        :param file_name: File to upload
        :param bucket_name: Bucket to upload to
        :param object_name: S3 object name. If not specified, file_name is used
        :return: True if file was uploaded, else False
        """
        # If S3 object_name is not specified, use file_name
        if object_name is None:
            object_name = file_name

        session = boto3.Session(
            aws_access_key_id='',
            aws_secret_access_key='',
            region_name='ap-southeast-1'
        )

        # Initialize an S3 client
        s3_client = session.client('s3')

        try:
            # Upload the file
            s3_client.upload_file(file_name, bucket_name, object_name)
            print(f"File '{file_name}' uploaded successfully to '{bucket_name}/{object_name}'")
            return True
        except FileNotFoundError:
            print(f"The file '{file_name}' was not found.")
            return False
        except NoCredentialsError:
            print("Credentials not available.")
            return False

    # Example usage
    file_name = r"zonejson/easymoneyzone.json"  # File you want to upload_
    bucket_name = "databucketfor"  # Your S3 bucket
    object_name = "easymoneyzone.json"    # Optional: S3 object name (default is the file name)

    # Call the function to upload
    upload_to_s3(file_name, bucket_name, object_name)