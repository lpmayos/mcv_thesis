#!/bin/bash
cd $HOME/code/mcv_thesis

pickle_folder="pickle_small"
solr_sensembed_path="http://localhost:8983/solr/sensembed_vectors"
path_to_train_val_videodatainfo="/home/lpmayos/code/caption-guided-saliency/DATA/MSR-VTT/train_val_videodatainfo.json"

# Create video captions and compute similarities
# python experiments.py -p $pickle_folder -e create_video_captions -s 3000 -l 3010 -v true -sp $solr_sensembed_path -jp $path_to_train_val_videodatainfo
# python experiments.py -p $pickle_folder -e compute_similarities -s 3000 -l 3010 -v true -sp $solr_sensembed_path -jp $path_to_train_val_videodatainfo

# experiments on videos 3000 to 3009, verbose
# python experiments.py -p $pickle_folder -e experiment1 -s 3000 -l 3010 -v true -sp $solr_sensembed_path -jp $path_to_train_val_videodatainfo > results/experiment1/experiment1_small.txt
# python experiments.py -p $pickle_folder -e experiment2 -s 3000 -l 3010 -v true -sp $solr_sensembed_path -jp $path_to_train_val_videodatainfo > results/experiment2/experiment2_small.txt
python experiments.py -p $pickle_folder -e experiment3 -s 3000 -l 3010 -v true -x $solr_sensembed_path -y $path_to_train_val_videodatainfo > results/experiment3/experiment3_small.txt
