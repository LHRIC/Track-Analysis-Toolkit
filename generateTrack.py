# have a function to take in lat and long to generate a track
# have a function to take in wheel speed data to generate a velocity trait track
# have a function to take in IMU data to generate a GGV

import pandas as pd
from matplotlib import pyplot as plt
import os
import numpy as np
import csv  
from scipy.signal import butter, filtfilt
import json

class GenerateTrack:
    def __init__(self, filepath):
        self.filepath = filepath
        self.dataFrame = None

    # loads in data from .csv file
    def load_data(self):
        if os.path.exists(self.filepath) and os.path.getsize(self.filepath) > 0:
               with open(self.filepath, 'r') as file, open("output_data.csv", 'w', newline='') as csvfile:
                # Prepare to collect all unique field names from the JSON data
                all_fieldnames = set()

                # First pass: Gather all keys across all JSON entries
                for line in file:
                    timestamp, data = line.split(':', 1)
                    first_number = int(timestamp.split(",")[0])
                    data_dict = json.loads(data)
                    all_fieldnames.update(data_dict.keys())

                # Convert to a sorted list for consistent CSV header order
                all_fieldnames.add("timestamp")  # Add 'timestamp' explicitly
                all_fieldnames = sorted(all_fieldnames)
                writer = csv.DictWriter(csvfile, fieldnames=all_fieldnames)
                writer.writeheader()

                # Second pass: Write the data rows
                file.seek(0)  # Reset file pointer to the beginning
                for line in file:
                    timestamp, data = line.split(':', 1)
                    first_number = int(timestamp.split(",")[0])
                    data_dict = json.loads(data)

                    # Add the extracted timestamp
                    data_dict['timestamp'] = first_number

                    # Convert latitude and longitude for human readability if present
                    if 'lat' in data_dict:
                        # data_dict['lat'] = data_dict['lat'] - 303863204
                        data_dict['lat'] = GenerateTrack.convert_geo(data_dict['lat'])
                    if 'lon' in data_dict:
                        data_dict['lon'] = GenerateTrack.convert_geo(data_dict['lon'])

                    # Write the row
                    writer.writerow(data_dict)
                return all_fieldnames

    def butter_lowpass_filter(dataFrame, data, cutoff, fs, order=5):
        nyq = 0.5 * fs
        normal_cutoff = cutoff / nyq
        # Design the filter
        b, a = butter(order, normal_cutoff, btype='low', analog=False)
        # Apply the filter
        filtered = filtfilt(b, a, dataFrame[data])
        return pd.Series(filtered, index= dataFrame.index)
    

  
    def convert_geo(geo_int):
        geo_str = str(geo_int)
        if geo_int < 0:
            return -float(geo_str[:3] + '.' + geo_str[3:])
        return float(geo_str[:2] + '.' + geo_str[2:])

    # plots trackmap 
    def create_trackmap():
        dataFrame = pd.read_csv("output_data.csv")

        if dataFrame is not None:
            plt.figure(figsize=(10, 10))
            try: 
                plt.scatter(dataFrame['timestamp'], y = dataFrame['lat'])
                plt.xlabel('Longitude')
                plt.ylabel('Latitude')
                plt.title('Track Map')
                plt.show()
            except: 
                print("Longitude and Latitude does not exist")
    
    # plots trackmap with velocity overlay
    def create_velocity_trackmap(self):
        if self.dataFrame is not None:
            try: 
                # using average front and average back wheel speed 
                f, axes = plt.subplots(nrows=2, ncols=1, sharex=True, sharey=True)  
                norm = plt.Normalize(-1.5, 1.5)

                self.dataFrame['Average Front'] = (self.dataFrame[self.cfg['columns']['front_left']] + self.dataFrame[self.cfg['columns']['front_right']]) / 2
                self.dataFrame['Average Back'] = (self.dataFrame[self.cfg['columns']['back_left']] + self.dataFrame[self.cfg['columns']['back_right']]) / 2

                # First plot with the average of the front 2 wheel speeds 
                sc1 = axes[0].scatter(self.dataFrame['Longitude'], self.dataFrame['Latitude'], c=self.dataFrame['Average Front'], marker='o', norm=norm)
                axes[0].set_title('Front')
                axes[0].set_ylabel('Longitude')

                # Second plot with the average of the back 2 wheel speeds 
                sc3 = axes[1].scatter(self.dataFrame['Longitude'], self.dataFrame['Latitude'], c=self.dataFrame['Average Front'], marker='o', norm=norm)
                axes[1].set_title('Back')
                axes[1].set_xlabel('Latitude')
                axes[1].set_ylabel('Longitude')

                # Create a colorbar
                cbar_ax = f.add_axes([0.85, 0.15, 0.05, 0.7])  # Adjust position as needed
                f.colorbar(sc1, cax=cbar_ax)

                plt.show()

                # using average VCU acceleration 
                # self.dataFrame['Average Acceleration'] = np.sqrt(self.dataFrame['VCU Acceleration X']**2 + self.dataFrame['VCU Acceleration Y']**2 + self.dataFrame['VCU Acceleration Z']**2)
                # plt.scatter(x = self.dataFrame['Longitude'], y = self.dataFrame['Latitude'], c = self.dataFrame['Average Acceleration'])
                # plt.xlabel('Longitude')
                # plt.ylabel('Latitude')
                # plt.title('Track Map')
                # plt.colorbar(label= "Wheel Speed Average", orientation= "horizontal")
                # plt.show()


            except: 
                print("Invalid data fields.")

    # plots the GGV 
    def create_GGV():
        fs = 20.0
        cutoff = 0.75
        
        dataFrame = pd.read_csv("output_data.csv")

        if dataFrame is not None:
            try: 
                dataFrame["lateral_accel"] = np.int16(dataFrame['cg_accel_x']) / 256.0 / 9.8
                dataFrame["long_accel"] = np.int16(dataFrame['cg_accel_y']) / 256.0 / 9.8 
                dataFrame["yaw_accel"] = np.int16(dataFrame['cg_accel_z']) / 256.0 / 9.8 
                dataFrame['filtered_pressures_lateral'] = GenerateTrack.butter_lowpass_filter(dataFrame, "lateral_accel", cutoff, fs)
                dataFrame['filtered_pressures_long'] = GenerateTrack.butter_lowpass_filter(dataFrame, "long_accel", cutoff, fs)
                dataFrame['filtered_pressures_yaw'] = GenerateTrack.butter_lowpass_filter(dataFrame, "yaw_accel", cutoff, fs)
                dataFrame.to_csv("output_data.csv", index=False)
                # Plot the filtered data
                plt.plot(
                    dataFrame['epoch'] - 1731130989,
                    # dataFrame['filtered_pressures_lateral']
                    dataFrame['filtered_pressures_long']
                    )
                plt.plot(dataFrame['epoch'] - 1731130989,
                    # dataFrame['filtered_pressures_lateral']
                    dataFrame['filtered_pressures_yaw'])
                plt.plot(dataFrame['epoch'] - 1731130989,
                    # dataFrame['filtered_pressures_lateral']
                    dataFrame['filtered_pressures_lateral'])
                plt.xlabel('Time (g)')
                plt.ylabel('Lateral Acceleration (g)')
                # plt.xlabel("Acceleration Y")
                # plt.ylabel("Acceleration X")
                plt.show()
            except: 
                print("Invalid data fields.")