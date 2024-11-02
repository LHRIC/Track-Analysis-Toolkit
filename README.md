# Generate-Track

## Purpose 
This program can be used to parse drive day data and generate Track Maps from the GPS data (longitute and latitude). An additional Tack Map can be generated with the velocity overlay as well as the GGV. 

## Requirements 
 Python 3.x
 YAML==6.x

## Installation and Running 
Install the required libraries into the virtual environment. On Windows
```
pip install -r ./requirements.txt
```
On UNIX/MacOS
```
pip3 install -r ./requirements.txt
```
To run the program on Windows 
```
py parsecsv.py
```
On UNIX/MacOS
```
python3 parsecsv.py
```

## Configuration and Execution
```config.yaml``` the place to change the desired field for each parameter desired depending on the driveday file provided.
```main.py``` handles the setup of Track Analysis. This is all you need to generate a Track Map from drive day data. 

```
def main(): 
    plotter = GenerateTrack("driveday.csv")
    GenerateTrack.load_data(plotter)
    GenerateTrack.plot_coordinates(plotter)
```

Track Analysis utilizes Matplotlib to plot the GPS data, velocity overlay, and GGV. 

<img src="https://cdn.discordapp.com/attachments/1288636548442493028/1292194261416149092/generateTrackUML.png?ex=6702d92f&is=670187af&hm=92ec9fc60d7a2c540833e43dd00d2f9e581e484e9ea716aa1f639716ba72e789&" alt="State Diagram " width="400"/>