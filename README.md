# A GUI for olfactometer testing using Photoionization (PID) detector output 

## Overview
This is a simple GUI designed for easy plotting of PID sensor output. Olfactometer control is accomplished using two arduinos. 
Arduino 1 controls olfactometer pinouts, while Arduino 2 reads PID signal. Output is plotted PID voltage over time for each 
olfactometer valve. 

## Features
- uses the everywhereml package for storage and upload of arduino control scripts to appropriate arduinos
- multithreaded gui for continuous signal measurement and plotting
- ability to customize testing parameters through GUI controls

## Installation
- Clone the repository:
- git clone https://github.com/rmblazing/Photoionization-device-testing.git
- Install dependencies:
- pip install -r requirements.txt
- run the notebook PID_GUI.ipynb

## Hardware requirements
- GUI requires an Arduino Mega to run the olfactometer and an arduino uno to collect PID signal
- Specified for control of custom Franks lab olfactometers and Perkin Elmer PID 
