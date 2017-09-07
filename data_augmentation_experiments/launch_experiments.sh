#!/bin/bash
cd $HOME/code/mcv_thesis/data_augmentation_experiments

pickle_folder="../pickle"
# pickle_folder="../pickle_small"
solr_sensembed_path="http://localhost:8983/solr/sensembed_vectors"

# path_to_train_val_videodatainfo="/home/lpmayos/code/caption-guided-saliency/DATA/MSR-VTT/train_val_videodatainfo.json"

# path_to_train_val_videodatainfo="/home/lpmayos/code/caption-guided-saliency/DATA/MSR-VTT/new_train_val_videodatainfo/train_val_videodatainfo_el_th1_0.11_th2_0.435.json"
# path_to_new_train_val_videodatainfo="/home/lpmayos/code/caption-guided-saliency/DATA/MSR-VTT/new_train_val_videodatainfo/train_val_videodatainfo_el_th1_0.11_th2_0.435_subj_pred_combi.json"

path_to_train_val_videodatainfo="/home/lpmayos/code/caption-guided-saliency/DATA/MSR-VTT/new_train_val_videodatainfo/train_val_videodatainfo_el_th1_0.11_th2_0.435_pmi_subject_replacement.json"
path_to_new_train_val_videodatainfo="/home/lpmayos/code/caption-guided-saliency/DATA/MSR-VTT/new_train_val_videodatainfo/train_val_videodatainfo_el_th1_0.11_th2_0.435_pmi_subject_replacement_subj_pred_combi_fixed.json"


first=0  #  0,      0
last=7010  #    7010,   10
verbose='true'

python experiments_data_augmentation.py --experiment 'combine_subjects_and_predicates' --pickle_folder $pickle_folder --first $first --last $last -v $verbose --solr_sensembed_path $solr_sensembed_path --path_to_train_val_videodatainfo $path_to_train_val_videodatainfo --path_to_new_train_val_videodatainfo $path_to_new_train_val_videodatainfo
