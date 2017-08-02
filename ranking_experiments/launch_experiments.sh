#!/bin/bash
cd $HOME/code/mcv_thesis/ranking_experiments

pickle_folder="../pickle"
# pickle_folder="../pickle_small"
solr_sensembed_path="http://localhost:8983/solr/sensembed_vectors"
path_to_train_val_videodatainfo="/home/lpmayos/code/caption-guided-saliency/DATA/MSR-VTT/train_val_videodatainfo.json"
first=0
last=7010
# last=10
verbose='true'
create_new_training_sentences='true'

python experiments_ranking.py --experiment 'all' --pickle_folder $pickle_folder --first $first --last $last -v $verbose --solr_sensembed_path $solr_sensembed_path --path_to_train_val_videodatainfo $path_to_train_val_videodatainfo --create_new_training_sentences $create_new_training_sentences
