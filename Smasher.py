import os
import json
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
            self.db = input("database name:: ").strip()
            self.user = input("username: ").strip()
            self.port = input("port number: ").strip()
            self.table = input("table name: ").strip()
            self.path = input("path to file: ").strip()

            if input("Save as default? (y/n)").lower() == "n": return

            pwd = input("password:").strip()
            defaultJson = {
                    "host" : self.host,
                    "db"   : self.db,
                    "user" : self.user,
                    "port" : self.port,
                    "table": self.table,
                    "path" : self.path
            }
            dumpJson(defaultJson, defaultFile)

    def connect(self):
        conn = psycopg2.connect(
            host=self.host,
            dbname=self.db,
            user=self.user,
            port=self.port,
            password=pwd
        )

        data = loadJson(self.path)
            try:
                insertData(data, conn)
                print("Data imported successfully.")
            except Exception as e:
                print(f"An error occurred: {str(e)}")
            finally:
                conn.close()
    
    def insertData(data, conn):
        with conn.cursor() as cursor:
            insert_query = f"""
            INSERT INTO {self.table} (fileName, fileHash)
            VALUES (%s, %s)
            """
            for entry in data:
                cursor.execute(insert_query, (entry['fileName'], entry['fileHash']))
            conn.commit()




