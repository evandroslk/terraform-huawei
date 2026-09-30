from huaweicloudsdkcore.auth.provider import PodIdentityCredentialProvider
from obs import ObsClient

BUCKET = "veritas-files"
OBJECT_KEY = "license.json"
OBS_ENDPOINT = "https://obs.sa-brazil-1.myhuaweicloud.com"

provider = PodIdentityCredentialProvider.get_basic()
credentials = provider.get_credentials()

print("Credenciais temporárias obtidas!")

client = ObsClient(
    access_key_id=credentials.ak,
    secret_access_key=credentials.sk,
    security_token=credentials.security_token,
    server=OBS_ENDPOINT,
)

try:
    response = client.getObject(BUCKET, OBJECT_KEY)

    print("HTTP status:", response.status)

    if response.status < 300:
        data = response.body.response.read()
        print("Conteúdo:")
        print(data.decode("utf-8"))
    else:
        print("Erro:", response.errorCode)
        print(response.errorMessage)

finally:
    client.close()
