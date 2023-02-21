#!/bin/bash

for i in $(seq 1 10);
do
    python run_sim_MD1.py &
done