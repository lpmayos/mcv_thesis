#!/bin/bash
cd $HOME/code/mcv_thesis

python experiments.py -p pickle -e compute_similarities -s 0 -l 7010 -v true
# python experiments.py -p pickle -e create_video_captions -s 3000 -l 3001 -v true
# python experiments.py -p pickle -e experiment1 -s 3000 -l 3001 -v true
# python experiments.py -p pickle -e experiment2 -s 3000 -l 3001 -v true
# python experiments.py -p pickle -e experiment3 -s 3000 -l 3001 -v true

python experiments.py -p pickle -e experiment1 -s 3000 -l 3010 -v true > results/experiment1/experiment1_all.txt
python experiments.py -p pickle -e experiment2 -s 3000 -l 3010 -v true > results/experiment2/experiment2_all.txt
python experiments.py -p pickle -e experiment3 -s 3000 -l 3010 -v true > results/experiment3/experiment3_all.txt