#!/bin/bash
cd $HOME/code/mcv_thesis/pmi_experiments

pickle_folder="../pickle"
# pickle_folder="../pickle_small"
solr_sensembed_path="http://localhost:8983/solr/sensembed_vectors"
# path_to_train_val_videodatainfo="/home/lpmayos/code/caption-guided-saliency/DATA/MSR-VTT/train_val_videodatainfo.json"
path_to_train_val_videodatainfo="/home/lpmayos/code/caption-guided-saliency/DATA/MSR-VTT/new_train_val_videodatainfo/train_val_videodatainfo_el_th1_0.11_th2_0.435.json"
path_to_new_train_val_videodatainfo="/home/lpmayos/code/caption-guided-saliency/DATA/MSR-VTT/new_train_val_videodatainfo/train_val_videodatainfo_el_th1_0.11_th2_0.435_pmi_subject_replacement_fixed.json"
first=0  #  0,      0
last=7010  #    7010,   10
verbose='true'

python experiments_pmi.py --experiment 'replace_best_pmi_subject' --pickle_folder $pickle_folder --first $first --last $last -v $verbose --solr_sensembed_path $solr_sensembed_path --path_to_train_val_videodatainfo $path_to_train_val_videodatainfo --path_to_new_train_val_videodatainfo $path_to_new_train_val_videodatainfo
# 7008
# 7009
# creating new training sentences...
# done creating new training sentences! Added 84042 captions