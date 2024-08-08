import json
import psycopg2
import os.path
defaultDBPath = "./config/defaultDB.json"

class Smasher:
    def __init__(self):

        if os.path.isfile(defaultDBPath):
            with open(defaultDBPath, "r") as defaultFile:
                defaultData = json.load(defaultFile)
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

            defaultJson = {
                    "host" : self.host,
                    "db"   : self.db,
                    "user" : self.user,
                    "port" : self.port,
                    "table": self.table,
                    "path" : self.path
            }

            with open (defaultDBPath, "w") as defaultFile:
                json.dump(defaultJson, defaultFile)

def load_json_data(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def insert_data_to_db(data, conn):
    with conn.cursor() as cursor:
        insert_query = """
        INSERT INTO files (fileName, fileHash)
        VALUES (%s, %s)
        """
        for entry in data:
            cursor.execute(insert_query, (entry['fileName'], entry['fileHash']))
        conn.commit()

def main():
    mySmasher = Smasher()
    pwd = input("password:").strip()

    conn = psycopg2.connect(
        host=mySmasher.host,
        dbname=mySmasher.db,
        password=pwd,
        user=mySmasher.user,
        port=mySmasher.port
    )
    
    data = load_json_data(mySmasher.path)
    try:
        # Insert data into the database
        insert_data_to_db(data, conn)
        print("Data imported successfully.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        # Close the database connection
        conn.close()

if __name__ == "__main__":
    main()
