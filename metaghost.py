# MetaGhost
# Copyright (c) 2024 69KaPuChiNo
# Licensed under the MIT License

# Author - 69KaPuChiNo
# github - https://github.com/69KaPuChiNo

import os
import sys
import json
from PIL import Image
import exifread
import webbrowser

class MetaDataFinder:
    def __init__(self):
        self.R = '\033[91m'  
        self.Y = '\033[93m'  
        self.G = '\033[92m'  
        self.CY = '\033[96m'  
        self.W = '\033[97m'  

        self.image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
        self.common_paths = ['~/Downloads', '~/Desktop', '~/Pictures', '~/Videos', '~/Documents', '~/Music']

    def start(self):
        os.system('clear')
        print(self.CY + """
███╗   ███╗███████╗████████╗ █████╗      ██████╗ ██╗  ██╗ ██████╗ ███████╗████████╗
████╗ ████║██╔════╝╚══██╔══╝██╔══██╗    ██╔════╝ ██║  ██║██╔═══██╗██╔════╝╚══██╔══╝
██╔████╔██║█████╗     ██║   ███████║    ██║  ███╗███████║██║   ██║███████╗   ██║   
██║╚██╔╝██║██╔══╝     ██║   ██╔══██║    ██║   ██║██╔══██║██║   ██║╚════██║   ██║   
██║ ╚═╝ ██║███████╗   ██║   ██║  ██║    ╚██████╔╝██║  ██║╚██████╔╝███████║   ██║   
╚═╝     ╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝     ╚═════╝ ╚═╝  ██╔╝╚═════╝ ╚══════╝   ╚═╝                                                                                   
""" + self.Y + """ v1.0""" + self.G + """
        
         Comprehensive Image Metadata Finder 
        
        """ + self.R + """>>""" + self.Y + """----""" + self.CY + """ Author - 69KaPuChiNo """ + self.Y + """----""" + self.R + """<<""")

    def menu(self):
        try:
            print(self.R + """\n
    #""" + self.Y + """ Select option""" + self.G + """ >>""" + self.Y + """
    
    1)""" + self.G + """ Check metadata of an image""" + self.Y + """
    2)""" + self.G + """ Remove metadata from an image""" + self.Y + """
    3)""" + self.G + """ Exit
    """)
            choice = int(input(self.CY + "Enter Your choice: " + self.W))
            if choice == 1:
                self.check_image_metadata()
            elif choice == 2:
                self.remove_metadata()
            elif choice == 3:
                self.handle_exit_choice()
            else:
                print(self.R + "\nInvalid choice! Please try again\n")
                self.menu()
        except ValueError:
            print(self.R + "\nInvalid choice! Please try again\n")
            self.menu()

    def get_exif_data(self, image_path):
        with open(image_path, 'rb') as image_file:
            tags = exifread.process_file(image_file)
            return tags

    def format_metadata(self, exif_data):
        metadata = {}
        metadata['Date and Time'] = exif_data.get('EXIF DateTimeOriginal', 'Not Available')
        metadata['Camera Model'] = exif_data.get('Image Model', 'Not Available')
        metadata['Device Name'] = exif_data.get('Image Make', 'Not Available')
        metadata['Software'] = exif_data.get('Image Software', 'Not Available')
        metadata['Software Version'] = exif_data.get('EXIF ExifImageLength', 'Not Available')
        metadata['GPS Coordinates'] = self.get_gps_coordinates(exif_data)

        return metadata

    def display_metadata(self, metadata):
        print(self.R + "\n==============================================================")
        print(self.Y + '\n>>> ' + self.CY + 'Image Metadata\n')
        for key, value in metadata.items():
            if key == 'GPS Coordinates':
                if value:
                    print(self.G + f"{key} : " + self.Y + f"https://www.google.com/maps?q={value[0]},{value[1]}")
                else:
                    print(self.G + f"{key} : " + self.Y + "Not Found")
            else:
                print(self.G + f"{key} : " + self.Y + str(value))
        print(self.R + "\n==============================================================")

    def save_metadata(self, metadata):
        print(self.R + """\n
    #""" + self.Y + """ Select action""" + self.G + """ >>""" + self.Y + """
    
    1)""" + self.G + """ Save as Text""" + self.Y + """
    2)""" + self.G + """ Save as JSON""" + self.Y + """
    3)""" + self.G + """ Don't Save""" + self.Y + """
    """)
        try:
            choice = int(input(self.CY + "Enter Your choice: " + self.W))
            if choice == 1:
                self.save_as_text(metadata)
            elif choice == 2:
                self.save_as_json(metadata)
            elif choice == 3:
                self.handle_no_save_choice()
            else:
                print(self.R + "\nInvalid choice! Please try again\n")
                self.save_metadata(metadata)
        except ValueError:
            print(self.R + "\nInvalid choice! Please try again\n")
            self.save_metadata(metadata)

    def save_as_text(self, metadata):
        file_name = input(self.G + "\n>>> " + self.Y + "Enter file name to save as text (without extension):" + self.W + " ")
        with open(file_name + '.txt', 'w') as file:
            for key, value in metadata.items():
                if key == 'GPS Coordinates' and value:
                    file.write(f"{key}: https://www.google.com/maps?q={value[0]},{value[1]}\n")
                else:
                    file.write(f"{key}: {value}\n")
        print(self.G + "Metadata saved as text file." + self.W)

    def save_as_json(self, metadata):
        file_name = input(self.G + "\n>>> " + self.Y + "Enter file name to save as JSON (without extension):" + self.W + " ")
        with open(file_name + '.json', 'w') as file:
            json.dump(metadata, file, indent=4)
        print(self.G + "Metadata saved as JSON file." + self.W)

    def check_image_metadata(self):
        self.list_common_paths()
        try:
            path_choice = int(input(self.CY + "\nEnter the number of the path (0 to enter custom path): " + self.W))
            if path_choice == 0:
                custom_path = input(self.CY + "Enter the custom path: " + self.W)
                self.list_photos(custom_path)
            else:
                selected_path = self.select_path(path_choice)
                if selected_path:
                    self.list_photos(selected_path)
                else:
                    print(self.R + "\nInvalid choice! Please try again.\n")
                    self.check_image_metadata()
            choice = int(input(self.CY + "\nEnter the number of the image to view metadata (0 to cancel): " + self.W))
            if choice == 0:
                return
            else:
                selected_image = self.select_image(choice)
                if selected_image:
                    exif_data = self.get_exif_data(selected_image)
                    if not exif_data:
                        print(self.R + "No EXIF data found")
                        return

                    metadata = self.format_metadata(exif_data)
                    self.display_metadata(metadata)
                    self.save_metadata(metadata)

                    self.show_location_on_maps(exif_data)
                else:
                    print(self.R + "\nInvalid choice! Please try again.\n")
                    self.check_image_metadata()
        except ValueError:
            print(self.R + "\nInvalid input! Please enter a number.\n")
            self.check_image_metadata()

    def select_image(self, choice):
        if 1 <= choice <= len(self.image_files):
            return self.image_files[choice - 1]
        else:
            return None

    def show_location_on_maps(self, exif_data):
        gps_coordinates = self.get_gps_coordinates(exif_data)
        if gps_coordinates:
            lat, lon = gps_coordinates
            google_maps_url = f"https://www.google.com/maps?q={lat},{lon}"
            print(self.G + f"GPS Coordinates : {lat}, {lon}")
            print(self.Y + f"Google Maps Link : {google_maps_url}")
        else:
            print(self.R + "No GPS coordinates found in metadata")

    def get_gps_coordinates(self, exif_data):
        if 'GPS GPSLatitude' in exif_data and 'GPS GPSLongitude' in exif_data:
            lat = self.convert_to_degrees(exif_data['GPS GPSLatitude'].values)
            lon = self.convert_to_degrees(exif_data['GPS GPSLongitude'].values)
            if exif_data['GPS GPSLatitudeRef'].values[0] != 'N':
                lat = -lat
            if exif_data['GPS GPSLongitudeRef'].values[0] != 'E':
                lon = -lon
            return lat, lon
        return None

    def convert_to_degrees(self, value):
        d = float(value[0].num) / float(value[0].den)
        m = float(value[1].num) / float(value[1].den)
        s = float(value[2].num) / float(value[2].den)
        return d + (m / 60.0) + (s / 3600.0)

    def remove_metadata(self):
        self.list_common_paths()
        try:
            path_choice = int(input(self.CY + "\nEnter the number of the path (0 to enter custom path): " + self.W))
            if path_choice == 0:
                custom_path = input(self.CY + "Enter the custom path: " + self.W)
                self.list_photos(custom_path)
            else:
                selected_path = self.select_path(path_choice)
                if selected_path:
                    self.list_photos(selected_path)
                else:
                    print(self.R + "\nInvalid choice! Please try again.\n")
                    self.remove_metadata()
            choice = int(input(self.CY + "\nEnter the number of the image to remove metadata (0 to cancel): " + self.W))
            if choice == 0:
                return
            else:
                selected_image = self.select_image(choice)
                if selected_image:
                    try:
                        image = Image.open(selected_image)
                        data = list(image.getdata())
                        image_without_exif = Image.new(image.mode, image.size)
                        image_without_exif.putdata(data)
                        new_image_path = os.path.splitext(selected_image)[0] + "_no_metadata" + os.path.splitext(selected_image)[1]
                        image_without_exif.save(new_image_path)
                        print(self.G + "Metadata removed successfully. New image saved as " + new_image_path + self.W)
                    except Exception as e:
                        print(self.R + f"An error occurred: {str(e)}" + self.W)
                else:
                    print(self.R + "\nInvalid choice! Please try again.\n")
                    self.remove_metadata()
        except ValueError:
            print(self.R + "\nInvalid input! Please enter a number.\n")
            self.remove_metadata()

    def list_common_paths(self):
        print(self.Y + "\nCommon Paths:")
        for idx, path in enumerate(self.common_paths, start=1):
            print(f"{idx}) {os.path.expanduser(path)}")
        print("0) Enter custom path")

    def select_path(self, choice):
        if 1 <= choice <= len(self.common_paths):
            return os.path.expanduser(self.common_paths[choice - 1])
        else:
            return None

    def list_photos(self, directory):
        self.image_files = []
        print(self.Y + f"\nImages in {directory}:")
        try:
            files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
            for file in files:
                if file.lower().endswith(tuple(self.image_extensions)):
                    self.image_files.append(os.path.join(directory, file))
            if not self.image_files:
                print(self.R + "No images found in this directory.")
            else:
                for idx, file in enumerate(self.image_files, start=1):
                    print(f"{idx}) {file}")
        except Exception as e:
            print(self.R + f"An error occurred while listing photos: {str(e)}")

    def handle_exit_choice(self):
        print(self.G + "\nThank you for using MetaGhost. Goodbye!")
        sys.exit(0)

    def handle_no_save_choice(self):
        print(self.G + "Metadata not saved." + self.W)

if __name__ == "__main__":
    app = MetaDataFinder()
    app.start()
    app.menu()
