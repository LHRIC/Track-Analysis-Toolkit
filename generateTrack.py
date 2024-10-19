# have a function to take in lat and long to generate a track
# have a function to take in wheel speed data to generate a velocity trait track
# have a function to take in IMU data to generate a GGV

import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np

class GenerateTrack:
    def __init__(self, filepath):
        self.filepath = filepath
        self.dataFrame = None

    # loads in data from .csv file
    def load_data(self):
        if os.path.exists(self.filepath) and os.path.getsize(self.filepath) > 0:
            self.dataFrame = pd.read_csv(self.filepath)
    
    # checks for correct data fields before plotting 
    def create_trackmap(self):
        if self.dataFrame is not None:
            try: 
                # using average front and average back wheel speed 
                
                f, axes = plt.subplots(nrows=2, ncols=1, sharex=True, sharey=True)  # Create 2 rows, 1 column
                norm = plt.Normalize(-1.5, 1.5)

                self.dataFrame['Average Front'] = (self.dataFrame['Front Left Wheel Speed'] + self.dataFrame['Front Right Wheel Speed'])/2
                self.dataFrame['Average Back'] = (self.dataFrame['Back Left Wheel Speed'] + self.dataFrame['Back Right Wheel Speed'])/2

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