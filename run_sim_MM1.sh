#!/bin/bash

for i in $(seq 1 15);
do
    python run_sim_MM1.py &
done