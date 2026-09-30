from huaweicloudsdkcore.auth.provider import PodIdentityCredentialProvider
from obs import ObsClient

BUCKET = "veritas-files"
OBJECT = "license.json"
OUTPUT = "/shared/license.json"

provider = PodIdentityCredentialProvider.get_basic()
credentials = provider.get_credentials()

client = ObsClient(
    access_key_id=credentials.ak,
    secret_access_key=credentials.sk,
    security_token=credentials.security_token,
    server="https://obs.sa-brazil-1.myhuaweicloud.com",
)

try:
    response = client.getObject(
        BUCKET,
        OBJECT,
        downloadPath=OUTPUT
    )

    if response.status != 200:
        raise RuntimeError(f"OBS HTTP {response.status}")

finally:
    client.close()
