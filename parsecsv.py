# Implement a function to take in the driveday.csv and be able to get the corrdinates needed
from generateTrack import GenerateTrack

def main(): 
    # runs method to generate Track Map
    plotter = GenerateTrack("driveday.csv", "config.yaml")
    GenerateTrack.load_data(plotter)
    # plots trackmap 
    GenerateTrack.create_trackmap(plotter)
    # # plots trackmap with velocity overlay
    GenerateTrack.create_velocity_trackmap(plotter)
    # plots GGV 
    GenerateTrack.create_GGV(plotter)

if __name__ == "__main__":
    main()