from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker, declarative_base
from sqlalchemy import create_engine
from helpers import loadJson

Base = declarative_base()
class ManufacturerData(Base):
    __tablename__ = "manufacturer_data"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    name_b64 = Column(String)
    name_coding = Column(String)
    address1 = Column(String)
    address1_b64 = Column(String)
    address1_coding = Column(String)
    address2 = Column(String)
    address2_b64 = Column(String)
    address2_coding = Column(String)
    city = Column(String)
    city_b64 = Column(String)
    city_coding = Column(String)
    stateprov = Column(String)
    postal_code = Column(String)
    country = Column(String)
    telephone = Column(String)
    fax = Column(String)
    url = Column(String)
    url_b64 = Column(String)
    url_coding = Column(String)
    email = Column(String)
    creation_date = Column(String)
    update_date = Column(String)

class FileData(Base):
    __tablename__ = "file_data"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    name_base64 = Column(String)
    name_coding = Column(String)
    path = Column(String)
    path_base64 = Column(String)
    path_coding = Column(String)
    extension = Column(String)
    extension_base64 = Column(String)
    extension_coding = Column(String)
    key_hash = Column(String)
    recursion_level = Column(Integer)
    bytes = Column(Integer)
    mtime = Column(Float)
    manufacturer_id = Column(Integer, ForeignKey("manufacturer_data.id"))
    manufacturer = relationship("ManufacturerData")

class ApplicationData(Base):
    __tablename__ = "application_data"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    name_b64 = Column(String)
    name_coding = Column(String)
    version = Column(String)
    poe = Column(String)
    build = Column(String)
    latest_copyright = Column(String)
    other = Column(String, nullable=True)
    creation_date = Column(String)
    update_date = Column(String)

class OperatingSystemData(Base):
    __tablename__ = "operating_system_data"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    name_b64 = Column(String)
    name_coding = Column(String)
    version = Column(String)
    architecture = Column(String)
    creation_date = Column(String)
    update_date = Column(String)


# PostgreSQL Connection
def connect():
    config = loadJson("config/defaultDB.json")
    password = input("Password:\n")
    DATABASE_URL = f"postgresql://{config["user"]}:{password}@{config["host"]}:{config["port"]}/{config["db"]}"
    print("You are now connected!")
    print(f"User: {config["user"]}")
    print(f"Port: {config["port"]}")
    print(f"Database: {config["db"]}")
    print(f"Host: {config["host"]}")
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(bind=engine)

    # Create tables
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    return SessionLocal()
