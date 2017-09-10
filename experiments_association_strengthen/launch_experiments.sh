#!/bin/bash
cd $HOME/code/mcv_thesis/experiments_association_strengthen

pickle_folder="../pickle"
# pickle_folder="../pickle_small"
solr_sensembed_path="http://localhost:8983/solr/sensembed_vectors"
# path_to_train_val_videodatainfo="/home/lpmayos/code/caption-guided-saliency/DATA/MSR-VTT/train_val_videodatainfo.json"
path_to_train_val_videodatainfo="/home/lpmayos/code/caption-guided-saliency/DATA/MSR-VTT/new_train_val_videodatainfo/train_val_videodatainfo_e4_th1_0.09_th2_0.506.json"
# path_to_new_train_val_videodatainfo="/home/lpmayos/code/caption-guided-saliency/DATA/MSR-VTT/new_train_val_videodatainfo/train_val_videodatainfo_el_th1_0.11_th2_0.435_pmi_subject_replacement.json"
path_to_new_train_val_videodatainfo="/home/lpmayos/code/caption-guided-saliency/DATA/MSR-VTT/new_train_val_videodatainfo/train_val_videodatainfo_e4_th1_0.09_th2_0.506_association_enhancement.json"
first=0  #  0,      0
last=7010  #    7010,   10
verbose='true'

python experiments_association_strengthen.py --experiment 'association_strengthen' --pickle_folder $pickle_folder --first $first --last $last -v $verbose --solr_sensembed_path $solr_sensembed_path --path_to_train_val_videodatainfo $path_to_train_val_videodatainfo --path_to_new_train_val_videodatainfo $path_to_new_train_val_videodatainfo
# 7008
# 7009
# creating new training sentences...
# done creating new training sentences! Added 84042 captions