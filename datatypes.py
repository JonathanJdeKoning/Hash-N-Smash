from dataclasses import dataclass

@dataclass
class FileData:
    name: str
    name_base64: str
    name_coding: str
    path: str
    path_base64: str
    path_coding: str
    extension: str
    extension_base64: str
    extension_coding: str
    key_hash: str
    recursion_level: int
    bytes: int
    mtime: float

@dataclass
class ManufacturerData:
    name: str
    name_b64: str
    name_coding: str
    address1: str
    address1_b64: str
    address1_coding: str
    address2: str
    address2_b64: str
    address2_coding: str
    city: str
    city_b64: str
    city_coding: str
    stateprov: str
    postal_code: str
    country: str
    telephone: str
    fax: str
    url: str
    url_b64: str
    url_coding: str
    email: str
    creation_date: str
    update_date: str



@dataclass
class ApplicationData:
    name: str
    name_b64: str
    name_coding: str
    version: str
    poe: str
    build: str
    latest_copyright: str
    other: str
    creation_date: str
    update_date: str


@dataclass
class OperatingSytemData:
    name: str
    name_b64: str
    name_coding: str
    version: str
    architecture: str
    creation_date: str
    update_date: str
