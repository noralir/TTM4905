# TTM4905 - Master project
## Model-Based Estimation for Latency Guarantee
### By Nora Lien Røneid

This project provides the code used for creating the results of this Master's thesis. It consists of a simulator, files for input generation, some files for finding statistics and for plotting the results. It also has many files and folders for specific use cases investigated for the thesis. 

## Running the simulator

The file `run_sim_generic.py` is used to run the simulator and it calls `generic_simulator.py` as many times as it is asked to run it. The inputs decide what type of simulation should be run and what information should be saved. The files that looks something like `NN_XX1.py` are used to run the specific ivestigated cases with data being saved to the folder `NN_XX1`. 

## Plotting the results
The results are plotted using the wanted function from `plot_generic.py`. Again, the `NN_XX1.py`-looking files are used for the specific use cases.

## Requirements
The following libraries are needed to run this project:
    pip install simpy
    pip install numpy
    pip install matplotlib