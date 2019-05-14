import boto3


# Create an S3 client
s3 = boto3.client('s3')

filename = '/Users/rvvittal/workspace/reinforce/data/patient_simple.json'
bucket_name = 'reinforce-2019-datalake-medical-patient'

# Uploads the given file using a managed uploader, which will split up large
# files automatically and upload parts in parallel.
s3.upload_file(filename, bucket_name, 'raw/patient.json')