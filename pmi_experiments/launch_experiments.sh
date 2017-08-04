#!/bin/bash
cd $HOME/code/mcv_thesis/data_augmentation_experiments

pickle_folder="../pickle"
# pickle_folder="../pickle_small"
solr_sensembed_path="http://localhost:8983/solr/sensembed_vectors"
path_to_train_val_videodatainfo="/home/lpmayos/code/caption-guided-saliency/DATA/MSR-VTT/train_val_videodatainfo.json"
first=0  #  0,      0
last=7010  #    7010,   10
verbose='true'

python experiments_data_enhancement.py --experiment 'combine_subjects_and_predicates' --pickle_folder $pickle_folder --first $first --last $last -v $verbose --solr_sensembed_path $solr_sensembed_path --path_to_train_val_videodatainfo $path_to_train_val_videodatainfo
