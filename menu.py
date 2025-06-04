from Hasher import Hasher
from Smasher import FileData, ApplicationData, ManufacturerData, OperatingSystemData, connect 
from math import inf
from helpers import b64, loadJson, dumpJson, print_header
from dataclasses import asdict
DASH_COUNT = 20

class Menu:
    def __init__(self, session):
        print_header("CONFIG")
        self.in_dir = input("Input Directory: ")
        self.out_dir = input("Output Directory: ")
        self.session = session




    def main_menu(self):
        print_header("OPTIONS")
        print("( 0 ) | Get all file metadata")
        print("( 1 ) | Export Data to postgreSQL ")
        print("( 2 ) | Enter Manual Data")
        print("( 3 ) | Quit")
        print("> ",end="")
        
        while True:
            option = int(input())
            if option in [0, 1, 2, 3]:
                break
            
            print("Invalid option, try again")
            print("> ", end="")
        
        if option == 0:
            self.hasher_menu()
        elif option == 1:
            self.smasher_menu() 
        elif option == 2:
            self.manual_menu()
        elif option == 3:
            return
        self.main_menu()
    
    def hasher_menu(self):
        print_header("HASHER")
        size_min = int(input("Minimum size to hash? (in bytes): "))
        size_max = input("Maximum? (leave blank for None): ")
        if size_max == "": size_max = inf
        else: size_max = int(size_max)

        myHasher = Hasher(size_min, size_max, self.in_dir, self.out_dir)
        myHasher.getHashes()
        myHasher.writeHashes()

    def smasher_menu(self):
        fileJson = loadJson(f"{self.out_dir}/metadata.json")
        for fileObj in fileJson:
            fileData = FileData(**fileObj)
            self.session.add(fileData)
        print("Added Metadata")



    def manual_menu(self):
        print_header("MANUAL")
        print("( 0 ) | Manufacturer Data")
        print("( 1 ) | Application Data")
        print("( 2 ) | Operating System Data")
        print("( 3 ) | Return to Main Menu")
        print("> ", end="")
        
        while True:
            option = int(input())
            if option in [0, 1, 2, 3]:
                break
            
            print("Invalid option, try again")
            print("> ", end="")
        
        if option == 0:
            self.manufacturer_menu()           
        elif option == 1:
            self.application_menu()
        elif option == 2:
            self.operating_system_menu()
        elif option == 3:
            return

        self.manual_menu()

    def manufacturer_menu(self):
        print_header("MANUFACTURER")
        name = input("Name: ") or None
        name_b64 = b64(name)  or None
        name_coding = "ascii" or None
        address1 = input("Address Line 1: ") or None
        address1_b64 = b64(address1) or None
        address1_coding = "ascii" or None
        address2 = input("Address Line 2: ") or None
        address2_b64 = b64(address2) or None
        address2_coding = "ascii" or None
        city = input("City: ") or None
        city_b64 = b64(city) or None
        city_coding = "ascii" or None
        stateprov = input("State / Providence: ") or None
        postal_code = input("Postal Code: ") or None
        country = input("Country: ") or None
        telephone = input("Telephone: ") or None
        fax = input("Fax: ") or None
        url = input("URL: ") or None
        url_b64 = b64(url)  or None
        url_coding = "ascii" or None
        email = input("Email: ") or None
        creation_date = input("Creation Date: ") or None
        update_date = input("Update Date: ") or None

        manufacturer_data = ManufacturerData(
            name=name,
            name_b64=name_b64,
            name_coding=name_coding,
            address1=address1,
            address1_b64=address1_b64,
            address1_coding=address1_coding,
            address2=address2,
            address2_b64=address2_b64,
            address2_coding=address2_coding,
            city=city,
            city_b64=city_b64,
            city_coding=city_coding,
            stateprov=stateprov,
            postal_code=postal_code,
            country=country,
            telephone=telephone,
            fax=fax,
            url=url,
            url_b64=url_b64,
            url_coding=url_coding,
            email=email,
            creation_date=creation_date,
            update_date=update_date, 
        )
        if input("Add to PostgreSQL? (y/n)\n>").lower() == "y":
            self.session.add(manufacturer_data)
            print("Added Manufacturer Data")
    
    
    def application_menu(self):
        print_header("APPLICATION")

        name = input("Name: ") or None
        name_b64 = b64(name)  or None
        name_coding = "ascii" or None
        version = input("Version: ") or None
        poe = input("POE: ") or None
        build = input("Build: ") or None
        latest_copyright = input("Latest Copyright: ") or None
        other = input("Other: ") or None
        creation_date = input("Creation Date: ") or None
        update_date = input("Update Date: ") or None
        
        app_data = ApplicationData(
            name=name,
            name_b64=name_b64,
            name_coding=name_coding,
            version=version,
            poe=poe,
            build=build,
            latest_copyright=latest_copyright,
            other=other,
            creation_date=creation_date,
            update_date=update_date,
        )
        if input("Add to PostgreSQL? (y/n)\n>").lower() == "y":
            self.session.add(app_data)
            print("Added Application Data")


    
    def operating_system_menu(self):
        print_header("OPERATING SYSTEM")
        name = input("Name: ") or None 
        name_b64 = b64(name)  or None
        name_coding = "ascii" or None
        version = input("Version: ") or None
        architecture = input("Architecture: ") or None
        creation_date = input("Creation Date: ") or None
        update_date = input("Update Date: ") or None
        operating_system_data = OperatingSystemData(
            name=name,
            name_b64=name_b64,
            name_coding=name_coding,
            version=version,
            architecture=architecture,
            creation_date=creation_date,
            update_date=update_date,
        )

        if input("Add to PostgreSQL? (y/n)\n>").lower() == "y":
            self.session.add(operating_system_data)
            print("Added OS Data")

