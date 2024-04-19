from azure.keyvault.secrets import SecretClient
from azure.identity import ClientSecretCredential
from airflow.models import Variable


class key_vault_utils:
    def __init__(self, tenant_id, key_vault_name):
        self.tenant_id = tenant_id
        self.key_vault_name = key_vault_name
        self.client_id = Variable.get("client_id")
        self.client_secret = Variable.get("client_secret")
        self.client = self.__create_client()

    def __create_client(self):
        key_vault_uri = f"https://{self.key_vault_name}.vault.azure.net"
        credential = ClientSecretCredential(self.tenant_id, self.client_id, self.client_secret)
        client = SecretClient(vault_url=key_vault_uri, credential=credential)
        return client

    def retrieve_secret_key(self, secret_key):
        retrieved_secret = self.client.get_secret(secret_key)
        return retrieved_secret.value
