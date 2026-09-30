import boto3

from botocore.config import Config
from huaweicloudsdkcore.auth.provider import PodIdentityCredentialProvider


BUCKET = "veritas-files"
OBJECT_KEY = "license.json"

ENDPOINT = "https://obs.sa-brazil-1.myhuaweicloud.com"
REGION = "ap-southeast-1"

# CCE Pod Identity
provider = PodIdentityCredentialProvider.get_basic()
credentials = provider.get_credentials()

# Credenciais temporárias → boto3
session = boto3.Session(
    aws_access_key_id=credentials.ak,
    aws_secret_access_key=credentials.sk,
    aws_session_token=credentials.security_token,
    region_name=REGION,
)


# Huawei OBS através da API S3
s3 = session.client(
    "s3",
    endpoint_url=ENDPOINT,
    config=Config(
        signature_version="s3v4",
        request_checksum_calculation="WHEN_REQUIRED",
        response_checksum_validation="WHEN_REQUIRED",
        s3={
            "addressing_style": "virtual",
        },
    ),
)

response = s3.get_object(
    Bucket=BUCKET,
    Key=OBJECT_KEY,
)

data = response["Body"].read()

print(f"HTTP status: {response['ResponseMetadata']['HTTPStatusCode']}")
print(f"Tamanho: {len(data)} bytes")
print()
print(data.decode("utf-8"))
