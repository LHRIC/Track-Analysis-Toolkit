# have a function to take in lat and long to generate a track
# have a function to take in wheel speed data to generate a velocity trait track
# have a function to take in IMU data to generate a GGV

import pandas as pd
import matplotlib.pyplot as plt
import os

class GenerateTrack:
    def __init__(self, filepath):
        self.filepath = filepath
        self.dataFrame = None

    # loads in data from .csv file
    def load_data(self):
        if os.path.exists(self.filepath) and os.path.getsize(self.filepath) > 0:
            self.dataFrame = pd.read_csv(self.filepath)
    
    # checks if Long and Lat exist before plotting 
    def plot_coordinates(self):
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