#!/bin/bash
cd $HOME/code/mcv_thesis

pickle_folder="pickle_small"
solr_sensembed_path="http://localhost:8983/solr/sensembed_vectors"
path_to_train_val_videodatainfo="/home/lpmayos/code/caption-guided-saliency/DATA/MSR-VTT/train_val_videodatainfo.json"

# Create video captions and compute similarities
# python experiments.py --pickle_folder $pickle_folder --experiment create_video_captions --first 3000 --last 3010 -v true --solr_sensembed_path $solr_sensembed_path --path_to_train_val_videodatainfo $path_to_train_val_videodatainfo
# python experiments.py --pickle_folder $pickle_folder --experiment compute_similarities --first 3000 --last 3010 -v true --solr_sensembed_path $solr_sensembed_path --path_to_train_val_videodatainfo $path_to_train_val_videodatainfo

# experiments on videos 3000 to 3009, verbose
# python experiments.py --pickle_folder $pickle_folder --experiment experiment1 --first 3000 --last 3010 -v true --solr_sensembed_path $solr_sensembed_path --path_to_train_val_videodatainfo $path_to_train_val_videodatainfo > results/experiment1/experiment1_small.txt
# python experiments.py --pickle_folder $pickle_folder --experiment experiment2 --first 3000 --last 3010 -v true --solr_sensembed_path $solr_sensembed_path --path_to_train_val_videodatainfo $path_to_train_val_videodatainfo > results/experiment2/experiment2_small.txt
python experiments.py --pickle_folder $pickle_folder --experiment experiment3 --first 3000 --last 3010 -v true --solr_sensembed_path $solr_sensembed_path --path_to_train_val_videodatainfo $path_to_train_val_videodatainfo > results/experiment3/experiment3_small.txt
