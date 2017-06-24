#!/bin/bash
cd $HOME/code/mcv_thesis

# python experiments.py -p pickle_small -e create_video_captions -s 3000 -l 3010 -v true
# python experiments.py -p pickle_small -e compute_similarities -s 3000 -l 3010 -v true

# experiments on videos 3000 to 3009, verbose
python experiments.py -p pickle_small -e experiment1 -s 3000 -l 3010 -v true > results/experiment1/experiment1_small.txt
python experiments.py -p pickle_small -e experiment2 -s 3000 -l 3010 -v true > results/experiment2/experiment2_small.txt
python experiments.py -p pickle_small -e experiment3 -s 3000 -l 3010 -v true > results/experiment3/experiment3_small.txt
