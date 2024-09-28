# have a function to take in lat and long to generate a track
# have a function to take in wheel speed data to generate a velocity trait track
# have a function to take in IMU data to generate a GGV

import pandas as pd
import matplotlib.pyplot as plt

class GenerateTrack:
    def __init__(self, filepath):
        self.filepath = filepath
        self.df = None
    
    def load_data(self):
        self.df = pd.read_csv(self.filepath)
    
    def plot_coordinates(self):
        if self.df is not None:
            plt.figure(figsize=(10, 10))
            plt.scatter(x=self.df['Longitude'], y=self.df['Latitude'])
            plt.xlabel('Longitude')
            plt.ylabel('Latitude')
            plt.title('Track Map')
            plt.show()