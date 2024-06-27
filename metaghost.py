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

    def start(self):
        
        os.system('clear')
        print(self.CY + """
███╗   ███╗███████╗████████╗ █████╗      ██████╗ ██╗  ██╗ ██████╗ ███████╗████████╗
████╗ ████║██╔════╝╚══██╔══╝██╔══██╗    ██╔════╝ ██║  ██║██╔═══██╗██╔════╝╚══██╔══╝
██╔████╔██║█████╗     ██║   ███████║    ██║  ███╗███████║██║   ██║███████╗   ██║   
██║╚██╔╝██║██╔══╝     ██║   ██╔══██║    ██║   ██║██╔══██║██║   ██║╚════██║   ██║   
██║ ╚═╝ ██║███████╗   ██║   ██║  ██║    ╚██████╔╝██║  ██║╚██████╔╝███████║   ██║   
╚═╝     ╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝     ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝   ╚═╝                                                                                   
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
        self.list_photos()
        try:
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
        files = os.listdir('.')
        image_files = [f for f in files if os.path.isfile(f) and any(f.lower().endswith(ext) for ext in self.image_extensions)]

        if 1 <= choice <= len(image_files):
            return image_files[choice - 1]
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
            lat = exif_data['GPS GPSLatitude']
            lon = exif_data['GPS GPSLongitude']
            lat_ref = exif_data.get('GPS GPSLatitudeRef', {}).values
            lon_ref = exif_data.get('GPS GPSLongitudeRef', {}).values

            lat = self.convert_to_degrees(lat)
            lon = self.convert_to_degrees(lon)

            if lat_ref and lat_ref != "N":
                lat = -lat
            if lon_ref and lon_ref != "E":
                lon = -lon

            return lat, lon
        else:
            print(self.R + "GPS coordinates not found in metadata")
            return None

    def convert_to_degrees(self, value):
        d = float(value.values[0].num) / float(value.values[0].den)
        m = float(value.values[1].num) / float(value.values[1].den)
        s = float(value.values[2].num) / float(value.values[2].den)

        return d + (m / 60.0) + (s / 3600.0)

    def remove_metadata(self):
        self.list_photos()
        try:
            choice = int(input(self.CY + "\nEnter the number of the image to remove metadata (0 to cancel): " + self.W))
            if choice == 0:
                return
            else:
                selected_image = self.select_image(choice)
                if selected_image:
                    self.remove_exif_metadata(selected_image)
                else:
                    print(self.R + "\nInvalid choice! Please try again.\n")
                    self.remove_metadata()
        except ValueError:
            print(self.R + "\nInvalid input! Please enter a number.\n")
            self.remove_metadata()

    def remove_exif_metadata(self, image_path):
        try:
            image = Image.open(image_path)
            image_without_exif = Image.new(image.mode, image.size)
            image_without_exif.paste(image)

            new_file_name = input(self.G + "\n>>> " + self.Y + "Enter new file name for the image without metadata:" + self.W + " ")
            image_without_exif.save(new_file_name + image_path[-4:])
            print(self.G + "Metadata removed and saved as " + new_file_name + image_path[-4:] + self.W)
        except Exception as e:
            print(self.R + f"Error: {e}")

    def list_photos(self):
        files = os.listdir('.')
        image_files = [f for f in files if os.path.isfile(f) and any(f.lower().endswith(ext) for ext in self.image_extensions)]

        print(self.R + "\n==============================================================")
        print(self.Y + '\n>>> ' + self.CY + 'List of Photos in Your Device\n')
        for idx, image in enumerate(image_files):
            print(self.G + f"{idx + 1}) " + self.Y + image)
        print(self.R + "\n==============================================================")

    def run(self):
        try:
            self.start()
            self.menu()
        except KeyboardInterrupt:
            print(self.Y + "\nInterrupted! Have a nice day :)" + self.W)

    def handle_exit_choice(self):
        try:
            print(self.Y + """
                                                                                           +@+ .       ..*@+                                         
                                                                                           -@*-@@.  .  .@@:#@.                                        
                                                                                           *@-%@- -@@@: +@* @-                                        
                                                                                           =@=#@+ :%@%. *@**@:                                        
                                                                                            #@+%#  *@* .@*+@#                                         
             ..      ...      ...       .......      ..       ..        .:--:.   ..        ..=+    *@*   .#*.       ..      .:-+++-:                  
             @@    .#@*.     +@@@.      @@%###@%+   =@*       @@-    -#@%#####+  @@*       @@      *@*    *@@-      #@-   -+%*. *.=%++.               
             @@   =@%-      .@@+@#      @@=    *@+  =@*       @@-   #@*.         @@*       @@      *@*    *@%@+     *@- .#*+#--+%--#%+@=              
             @@ -@@-        #@: %@-     @@=    :@*  =@*       @@-  @@=           @@*       @@      *@*    *@-+@%.   *@-.%. #    *   :* ==             
             @@#@@#        +@+   %@     @@*---*@@.  =@*       @@- -@@            @@@@@@@@@@@@      *@*    *@- :@@=  *@--#+#%++++%++++@++@             
             @@=.=@#      :@@*+++%@#    @@#+++=.    =@*       @@- :@@.           @@+       @@      *@*    *@-  .%@+ *@--* -*   :*    #  %             
             @@   -@@-    %@*-----@@=   @@=         .@#      .@@   #@*           @@*       @@      *@*    *@-    #@+*@- #-.#...-#...+*.#-             
             @@    :%@+  *@%      -@@.  @@=          +@*.   :%@+    +@%+:    ..  @@*      :@@      *@*    *@-     *@@@-  +#+@--+#..+#-#:              
             **      +*+:**        =*+  **-           -+#%%#*=       .=**%%%#*-  **-       #*      =*=    =*:      -**:    =*#+*#=##=-                
                                                                                             
            """ + self.W)
            sys.exit(0)
        except KeyboardInterrupt:
            print(self.Y + "\nInterrupted! Have a nice day :)" + self.W)

    def handle_no_save_choice(self):
        try:
            print(self.Y + "\nDo you want to:")
            print(self.G + "1) Open GPS on Google Maps")
            print(self.G + "2) Exit")
            choice = int(input(self.CY + "Enter Your choice: " + self.W))
            if choice == 1:
                self.open_gps_on_maps()
            elif choice == 2:
                self.handle_exit_choice()
            else:
                print(self.R + "\nInvalid choice! Please try again\n")
                self.handle_no_save_choice()
        except ValueError:
            print(self.R + "\nInvalid choice! Please try again\n")
            self.handle_no_save_choice()

    def open_gps_on_maps(self):
        try:
            self.list_photos()
            choice = int(input(self.CY + "\nEnter the number of the image to open GPS coordinates on Google Maps (0 to cancel): " + self.W))
            if choice == 0:
                return
            else:
                selected_image = self.select_image(choice)
                if selected_image:
                    exif_data = self.get_exif_data(selected_image)
                    if not exif_data:
                        print(self.R + "No EXIF data found")
                        return

                    gps_coordinates = self.get_gps_coordinates(exif_data)
                    if gps_coordinates:
                        lat, lon = gps_coordinates
                        google_maps_url = f"https://www.google.com/maps?q={lat},{lon}"
                        print(self.G + f"Opening GPS Coordinates : {lat}, {lon}")
                        print(self.Y + f"Opening Google Maps Link : {google_maps_url}")
                        webbrowser.open(google_maps_url, new=2)
                    else:
                        print(self.R + "No GPS coordinates found in metadata")
                else:
                    print(self.R + "\nInvalid choice! Please try again.\n")
                    self.open_gps_on_maps()
        except ValueError:
            print(self.R + "\nInvalid input! Please enter a number.\n")
            self.open_gps_on_maps()

if __name__ == "__main__":
    metadata_finder = MetaDataFinder()
    metadata_finder.run()
