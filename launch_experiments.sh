#!/bin/bash
cd $HOME/code/mcv_thesis

pickle_folder="pickle"
solr_sensembed_path="http://localhost:8983/solr/sensembed_vectors"
path_to_train_val_videodatainfo="/home/lpmayos/code/caption-guided-saliency/DATA/MSR-VTT/train_val_videodatainfo.json"
first=0
last=7010
verbose='true'
create_new_training_sentences='true'
experiment='experiment1'  # create_video_captions, display_tokens_similarity, experiment1, experiment3, experiment4, experiment5, find_tokens_similarity_threshold

python experiments.py --pickle_folder $pickle_folder --experiment $experiment --first $first --last $last -v $verbose --solr_sensembed_path $solr_sensembed_path --path_to_train_val_videodatainfo $path_to_train_val_videodatainfo --create_new_training_sentences $create_new_training_sentences
