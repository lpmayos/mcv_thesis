#!/bin/bash
cd $HOME/code/mcv_thesis

pickle_folder="pickle"  # pickle, pickle_small
solr_sensembed_path="http://localhost:8983/solr/sensembed_vectors"
path_to_train_val_videodatainfo="/home/lpmayos/code/caption-guided-saliency/DATA/MSR-VTT/train_val_videodatainfo.json"
create_new_training_sentences='false'
first=0  # 0, 3000
last=7010  # 7010, 3010
verbose='false'
experiment='create_boxplots_different_thresholds'  # create_video_captions, compute_similarities, experiment1, experiment2, experiment3, experiment4, experiment4, experiment5, create_boxplots_different_thresholds

python experiments.py --pickle_folder $pickle_folder --experiment $experiment --first $first --last $last -v $verbose --solr_sensembed_path $solr_sensembed_path --path_to_train_val_videodatainfo $path_to_train_val_videodatainfo --create_new_training_sentences $create_new_training_sentences
