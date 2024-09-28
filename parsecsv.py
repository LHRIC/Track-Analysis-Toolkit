# Implement a function to take in the driveday.csv and be able to get the corrdinates needed
from generateTrack import GenerateTrack

def main(): 
    plotter = GenerateTrack("driveday.csv")
    GenerateTrack.load_data(plotter)
    GenerateTrack.plot_coordinates(plotter)

if __name__ == "__main__":
    main()