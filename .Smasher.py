import os
import json
import psycopg2
from helpers import loadJson, dumpJson

defaultDBPath = "./config/defaultDB.json"
class Smasher:
    def __init__(self):

        if os.path.isfile(defaultDBPath):
            defaultData = loadJson(defaultDBPath)
            
            self.host = defaultData["host"]
            self.db = defaultData["db"]
            self.user = defaultData["user"]
            self.port= defaultData["port"]
            self.table = defaultData["table"]
            self.path = defaultData["path"]
        else:
            print("Default info not found... Asking Manually:")

            self.host = input("hostname: ").strip()
            self.db = input("database name: ").strip()
            self.user = input("username: ").strip()
            self.port = input("port number: ").strip()
            self.table = input("table name: ").strip()
            self.path = input("path to file: ").strip()

            if input("Save as default? (y/n)").lower() == "n": return

            defaultJson = {
                    "host" : self.host,
                    "db"   : self.db,
                    "user" : self.user,
                    "port" : self.port,
                    "table": self.table,
                    "path" : self.path
            }
            dumpJson(defaultJson, defaultDBPath)

        self.pwd = input("password:").strip()


    def insertData(self, data, conn):
        with conn.cursor() as cursor:
            insert_query = f"""
            INSERT INTO {self.table} (
                key_hash, recursion_level, bytes, mtime, path, 
                path_base64, path_coding, name, name_base64, 
                name_coding, extension, extension_base64, extension_coding
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            for entry in data:
                cursor.execute(insert_query, (
                    entry['key_hash'], 
                    entry['recursion_level'], 
                    entry['bytes'], 
                    entry['mtime'], 
                    entry['path'], 
                    entry['path_base64'], 
                    entry['path_coding'], 
                    entry['name'], 
                    entry['name_base64'], 
                    entry['name_coding'], 
                    entry['extension'], 
                    entry['extension_base64'], 
                    entry['extension_coding']
                ))
            conn.commit()

    def connect(self):
        conn = psycopg2.connect(
            host=self.host,
            dbname=self.db,
            user=self.user,
            port=self.port,
            password=self.pwd
        )

        data = loadJson(self.path)
        try:
            self.insertData(data, conn)
            print("Data imported successfully.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")
        finally:
            conn.close()
    

