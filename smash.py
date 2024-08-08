import json
import psycopg2
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
    hostname = "localhost"
    database = "smashed"
    username = "dekoding"
    pwd = "admin"
    port_id = 5432

    table_name = "files"
    json_file_path = "/home/kali/hashnsmash/logs/hashes.json"

    conn = psycopg2.connect(
        host=hostname,
        dbname=database,
        password=pwd,
        user=username,
        port=port_id
    )
    
    data = load_json_data(json_file_path)
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
