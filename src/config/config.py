from typing import Any, Dict
from google.cloud import secretmanager

import yaml
import os


class App:
    port: int
    name: str
    environment: str

    def __init__(self, **data: Any):
        self.__dict__.update(**data)


class Database:
    host: str
    port: int
    name: str
    username: str
    password: str

    def __init__(self, **data: Any):
        self.__dict__.update(**data)
        
class Outbound:
    base_url: str
    api_key: str | None

    def __init__(self, **data: Any):
        self.__dict__.update(**data)
        
class Sharepoint:
    client_id: str
    client_secret: str
    base_url: str
    site_name: str
    document_library: str
    dealer_document_folder: str
    dealer_download_folder: str
    allocation_document_folder: str
    allocation_download_folder: str
    allocation_site: str
    dealer_final_folder: str
    dealer_final_document_folder: str
    
    def __init__(self, **data: Any):
        self.__dict__.update(**data)
    
class Config:
    app: App
    database: Dict[str, Database]
    outbound: Dict[str, Outbound]
    sharepoint: Dict[str, Sharepoint]

    def __init__(self, data: Dict[str, Any]):
        self.app = App(**data["app"])
        self.database = dict((k, Database(**v)) for k, v in data["database"].items())
        self.outbound = dict((k, Outbound(**v)) for k, v in data["outbound"].items())
        


_config: Config | None = None


def load_config() -> None:
    global _config
    if os.getenv("ENVIRONMENT") in ["local", "production"]:
        path = os.path.dirname(os.path.abspath(__file__))
        with open(
            "{}/config-{}.yaml".format(path, os.getenv("ENVIRONMENT")), "r"
        ) as stream:
            data = yaml.safe_load(stream)
            _config = Config(data)
    else:
        client = secretmanager.SecretManagerServiceClient()
        google_project_id = os.getenv("GCLOUD_PROJECT")
        environment = os.getenv("ENVIRONMENT")
        response = client.access_secret_version(
            request={
                "name": f"projects/{google_project_id}/secrets/his-sharepoint-backend-config-{environment}/versions/latest"
            }
        )
        payload = response.payload.data.decode("UTF-8")
        data = yaml.safe_load(payload)
        _config = Config(data)


def get_config() -> Config:
    global _config
    if _config is None:
        load_config()
        if _config is None:
            raise RuntimeError("Configuration could not be loaded")
    return _config