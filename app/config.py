import os

CONFIG = {
    "type": "service_account",
    "project_id": os.environ.get("project_id"),
    "private_key_id": os.environ.get("private_key_id"),
    "private_key": os.environ.get("private_key"),
    "client_email": os.environ.get("client_email"),
    "client_id": os.environ.get("client_id"),
    "auth_uri": os.environ.get("auth_uri"),
    "token_uri": os.environ.get("token_uri"),
    "auth_provider_x509_cert_url": os.environ.get("auth_provider_x509_cert_url"),
    "client_x509_cert_url": os.environ.get("client_x509_cert_url"),
}

ONEDRIVE_CONFIG = {
    "client_id": os.environ.get("od_client_id"),
    "client_secret": os.environ.get("od_client_secret"),
    "scope": "Files.ReadWrite.All",
    "grant_type": "refresh_token",
    "refresh_token": os.environ.get("od_refresh_token"),
}
