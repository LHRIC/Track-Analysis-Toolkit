# Generate-Track

## Purpose 
This program can be used to parse drive day data and generate Track Maps from the GPS data (longitute and latitude).

## Requirements 
 Python 3.x

## Installation and Environment Setup
Install the required libraries into the virtual environment. On Windows
```
$ pip install -r ./requirements.txt
```
On UNIX/MacOS
```
$ pip3 install -r ./requirements.txt
```

## Configuration and Execution
```main.py``` handles the setup of Track Analysis. This is all you need to generate a Track Map from drive day data. 

```
def main(): 
    plotter = GenerateTrack("driveday.csv")
    GenerateTrack.load_data(plotter)
    GenerateTrack.plot_coordinates(plotter)
```

Track Analysis utilizes Matplotlib to plot the GPS data. 

<img src="https://cdn.discordapp.com/attachments/1291227255065804800/1291227261785083964/image.png?ex=66fffd59&is=66feabd9&hm=23bd6c6a1714fc74d97fd36b619937c7537664341b9c6424c3a55a294456d2ac&" alt="State Diagram " width="400"/>