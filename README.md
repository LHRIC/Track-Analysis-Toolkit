# Generate-Track

## Purpose 
This program can be used to parse drive day data and generate Track Maps from the GPS data (longitute and latitude).

## Requirements 
 Python 3.x

## Installation and Environment Setup
Install the required libraries into the virtual environment
```$ pip install -r ./requirements.txt```

## Configuration and Execution
```main.py``` handles the setup of Track Analysis. This is all you need to generate a Track Map from drive day data. 

```
def main(): 
    plotter = GenerateTrack("driveday.csv")
    GenerateTrack.load_data(plotter)
    GenerateTrack.plot_coordinates(plotter)
```

Track Analysis utilizes Matplotlib to plot the GPS data. 