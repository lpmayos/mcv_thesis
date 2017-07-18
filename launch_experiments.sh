#!/bin/bash
cd $HOME/code/mcv_thesis

pickle_folder="pickle"
solr_sensembed_path="http://localhost:8983/solr/sensembed_vectors"
path_to_train_val_videodatainfo="/home/lpmayos/code/caption-guided-saliency/DATA/MSR-VTT/train_val_videodatainfo.json"
first=0
last=7010
verbose='true'


# experiment_name: create_video_captions, display_tokens_similarity, experiment1, experiment2, experiment3, experiment4
# th2: {'experiment1': 0.785, 'experiment3': 4.0, 'experiment4': 4.0, 'experiment5': 16.0}


# # experiment1: through the boxplot we observe that the right threshold th2 is 0.785
# python experiments.py --experiment 'experiment1' --th2 0.785 --pickle_folder $pickle_folder --first $first --last $last -v $verbose --solr_sensembed_path $solr_sensembed_path --path_to_train_val_videodatainfo $path_to_train_val_videodatainfo --create_new_training_sentences 'true'

# # experiment2: through the boxplot we observe that the right threshold th2 is around 0.18
# # TODO change create_new_training_sentences to true once we are done testing it
# python experiments.py --experiment 'experiment2' --th2 0.20 --pickle_folder $pickle_folder --first $first --last $last -v $verbose --solr_sensembed_path $solr_sensembed_path --path_to_train_val_videodatainfo $path_to_train_val_videodatainfo --create_new_training_sentences 'false'

# experiments 3 and 4: we need to find the right th1
# python experiments.py --experiment 'find_th1' --th2 0.14 --pickle_folder $pickle_folder --first $first --last $last -v $verbose --solr_sensembed_path $solr_sensembed_path --path_to_train_val_videodatainfo $path_to_train_val_videodatainfo --create_new_training_sentences 'false'

python experiments.py --experiment 'experiment5' --th2 0.14 --pickle_folder $pickle_folder --first $first --last $last -v $verbose --solr_sensembed_path $solr_sensembed_path --path_to_train_val_videodatainfo $path_to_train_val_videodatainfo --create_new_training_sentences 'false'
