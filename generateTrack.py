# have a function to take in lat and long to generate a track
# have a function to take in wheel speed data to generate a velocity trait track
# have a function to take in IMU data to generate a GGV

import pandas as pd
from matplotlib import pyplot as plt
import os
import numpy as np
import yaml

class GenerateTrack:
    def __init__(self, filepath, config_file):
        self.filepath = filepath
        self.cfg = None 
        try: 
            if not os.path.exists(config_file):
                raise FileNotFoundError(f"Configuration file not found: {config_file}")
            self.cfg = read_yaml(config_file)
        except FileNotFoundError as e:
            print(e)
        self.dataFrame = None
       

    # loads in data from .csv file
    def load_data(self):
        if os.path.exists(self.filepath) and os.path.getsize(self.filepath) > 0:
            self.dataFrame = pd.read_csv(self.filepath)

    # plots trackmap 
    def create_trackmap(self):
        if self.dataFrame is not None:
            plt.figure(figsize=(10, 10))
            try: 
                plt.scatter(x=self.dataFrame['Longitude'], y=self.dataFrame['Latitude'])
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
    def create_GGV(self):
        if self.dataFrame is not None:
            try: 
                columns = self.cfg.get('columns', {})
                if not columns:
                    raise ValueError("Missing 'columns' in configuration file.")

                # Calculate the average wheel speed
                self.dataFrame['Average'] = (
                    self.dataFrame[columns['front_left']] + 
                    self.dataFrame[columns['front_right']] + 
                    self.dataFrame[columns['back_left']] + 
                    self.dataFrame[columns['back_right']]
                ) / 4

                # Filter data based on range from YAML config
                filter_config = self.cfg.get('filter', {})
                min_avg = filter_config.get('min_average')
                max_avg = filter_config.get('max_average')

                if min_avg is None or max_avg is None:
                    raise ValueError("Missing 'min_average' or 'max_average' in 'filter' configuration.")

                filtered_df = self.dataFrame[(self.dataFrame['Average'] >= min_avg) & (self.dataFrame['Average'] <= max_avg)]

                # Plot the filtered data
                plt.scatter(
                    filtered_df[columns['accel_y']] / 9.81, 
                    filtered_df[columns['accel_x']] / 9.81, 
                    c=filtered_df['Average'], 
                    cmap='viridis'
                )
                plt.xlabel("Acceleration Y")
                plt.ylabel("Acceleration X")
                plt.colorbar(label="Average Wheel Speed")
                plt.show()
            except: 
                print("Invalid data fields.")
                
def read_yaml(config_file):
    with open(config_file, 'r') as file:
        return yaml.safe_load(file)