# Improving the quality of video-to-language models by an optimized annotation of the training material 

* **Master in Computer Vision 2016-2017**
* **Student**: Laura Pérez Mayos
* **Supervisor**: Leo Wanner
* **Co-Supervisor**: Federico Sukno
* **University**: UPF
* **Course**: 2016-2017












## Abstract
 
Video has become omnipresent, and the analysis of the semantics of video has a large variety of applications, including scene understanding, accessibility improvement and information retrieval.  However, automatically describing  videos  in terms of natural  language  is  one  of  the  ultimate challenges of video understanding, given the difficulties of video interpretation and natural language generation. Many state-of-the-art models focus on the generation of captions of short-term videos. In this context, Microsoft has released Microsoft Research - Video to Text (MSR-VTT), a large-scale annotated video benchmark that contains 41.2 hours of recordings.The annotation consists of 20 Mechanical Turk captions per video, resulting in 200K captions-video pairs in total.

![alt text](https://raw.githubusercontent.com/lpmayos/mcv_thesis/master/samples/video_frames.png "MSR-VTT Examples: video frames and annotated sentences")

As the excerpts of the caption lists in Figure 1 show, the specificity and quality of the captions vary considerably. This is likely to have a negative influence on the quality of the trained models since all captions are taken into account equally. In the context of this Master Thesis, possible automatic strategies for optimizing the annotations of video material will be explored and the consequences of this optimization will be analyzed with a state-of-the-art deep learning video-to-language model.




















## Pre-processing

All experiments require the existence of a solr core containing the sensembeddings for each token, and the previous execution (once) of compute_similarities, which generates a pickle file for each video and a pickle file containing the tokens_set, variables which are necessary to launch the experiments.


### SenseEmbeds: Solr

SenseEmbed vectors should be downloaded from http://lcl.uniroma1.it/sensembed/, and extrated to vectors_sensembed_json/sensembed_vectors.

**Goal**: upload sensembeds to solr to use them faster in experiments.

**Results**: a solr core containing all sensembeds

**Execution**: after creating the solr core (see sample in samples/solr_core), execute $python upload_sensembeds_to_solr.py



### create_video_captions

**Goal**: Compute the similarity between all pairs of tokens extracted from the annotations and save it to tokens_set, creating videoCaption objects for videos and saving them as pickle if they don't exist.

**Method**: for each video in train_val_set try to load videoCaption object from pickle. If it dies not exist, create a VideoCaption object and save it as pickle, and add all its tokens to token_set, containing information of all the tokens of all sentences of all videos. It computes the similarity between all pairs of tokens extracted from the annotations and saves it to tokens_set.

**Results**: pickle files for each video and for tokens_set are saved to config.pickle_folder

**Execution**: see experiments_ranking/launch_experiments.sh, experiment "create_video_captions"





















## Experiments: outliers removal


### Display tokens similarity

**Goal**: for each token of each sentence, computes which of the tokens of every other sentence is closer and shows it on shell.

**Method**: in config.tokens_set we have computed the similarity of every pair of tokens, so we just loop over all of them and keep the most similar.

**Results**: a sample of the results can be seen at experiments_ranking/results_ranking/experiment2/, and results are shown on shell

**Execution**: see experiments_ranking/launch_experiments.sh, experiment "display_tokens_similarity"


### experiment1: remove outliers

**Goal**: detect those captions that are outliers: they are not semantically related to the others.

**Method**: for each video we get all the captions and we compute an embedding for all the sentences. Then, we project all the embeddings in common space, we compute its centroid and the distances to the centroid of each embedding, sorting the captions by distance. Then, discard the ones above threshold.

**Results**: a sample of the results (sentence ordering and image of the embedding space) is shown on shell if verbose=True and can be also seen at experiments_ranking/results_ranking/experiment1/, and a new train_val_videodatainfo.json is generated to train a new model on config.path_to_train_val_videodatainfo.

**Execution**: see experiments_ranking/launch_experiments.sh, experiment "experiment1"


### experiment2: remove outliers

**Goal**: detect those captions that are outliers: they are not semantically related to the others.

**Method**: for each pair of sentences, compute their similarity (non-symmetric) as the sum of the similarity of each token in one sentence to the closest one in the other sentence, dividing by the number of tokens added. Then, discard the ones below threshold.

**Results**: sentence ranking is shown on shell if verbose=True, a sample can be also seen at experiments_ranking/results_ranking/experiment2/, and a new train_val_videodatainfo.json is generated to train a new model on config.path_to_train_val_videodatainfo.

**Execution**: see experiments_ranking/launch_experiments.sh, experiment "experiment2"


### experiment3: remove outliers

**Goal**: detect those captions that are outliers: they are not semantically related to the others.

**Method**: for each pair of sentences, compute their similarity (non-symmetric) as the sum of the similarities of each token in one sentence to the closest one in the other sentence if similarity is ABOVE A THRESHOLD, dividing by the number of tokens added. Then, discard the ones below threshold.

**Results**: sentence ranking is shown on shell if verbose=True, a sample can be also seen at experiments_ranking/results_ranking/experiment3/, and a new train_val_videodatainfo.json is generated to train a new model on config.path_to_train_val_videodatainfo.

**Execution**: see experiments_ranking/launch_experiments.sh, experiment "experiment3"


### experiment4: remove outliers

**Goal**: detect those captions that are outliers: they are not semantically related to the others.

**Method**: for each pair of sentences, compute their similarity (non-symmetric) as the sum 1 for each token if similarity to the closest one in the other sentence if similarity is ABOVE A THRESHOLD, dividing by the total number of tokens. Then, discard the ones below threshold.

**Results**: sentence ranking is shown on shell if verbose=True, a sample can be also seen at experiments_ranking/results_ranking/experiment4/, and a new train_val_videodatainfo.json is generated to train a new model on config.path_to_train_val_videodatainfo.

**Execution**: see experiments_ranking/launch_experiments.sh, experiment "experiment4"


### experiment4symmetric: remove outliers

**Goal**: detect those captions that are outliers: they are not semantically related to the others.

**Method**: for each pair of sentences, compute their similarity as the sum 1 for each token if similarity to the closest one in the other sentence if similarity is ABOVE A THRESHOLD, dividing by the total number of tokens. For each pair of sentences, final simmilarity is computed as: (d(s1, s2) + d(s2, s1)) / 2. Then, discard the ones below threshold.

**Results**: sentence ranking is shown on shell if verbose=True, a sample can be also seen at experiments_ranking/results_ranking/experiment4symmetrical/, and a new train_val_videodatainfo.json is generated to train a new model on config.path_to_train_val_videodatainfo.

**Execution**: see experiments_ranking/launch_experiments.sh, experiment "experiment4symmetrical"


### experiment5: remove outliers using the bleu metric

**Goal**: detect those captions that are outliers: they are not semantically related to the others.

**Method**: for each pair of sentences, compute their similarity using the bleu metric. Then, discard the ones below threshold.

**Results**: sentence ranking is shown on shell if verbose=True, a sample can be also seen at experiments_ranking/results_ranking/experiment5/, and a new train_val_videodatainfo.json is generated to train a new model on config.path_to_train_val_videodatainfo.

**Execution**: see experiments_ranking/launch_experiments.sh, experiment "experiment5"



### find threshold

**Goal**: find right tokens similarity threshold for experiments 3 and 4

**Method**: iterate over different tokens similarity thresholds, generating boxplots and barcharts which will help us decide the most useful thresholds.

**Results**: images and logs are generated in experiments_ranking/results_ranking/experiment4 and experiments_ranking/results_ranking/experiment5

**Execution**: see experiments_ranking/launch_experiments.sh, experiment "all"
















## Experiments: data augmentation


**Goal**: generate an augmented training set.

**Method**: combine the subjects and predicates of the captions of each video, given that they are compatible in terms of number and semantics.

**Results**: experiments_data_augmentation/results_data_augmentation_compare_training_sets.py offers functions to compare different training sets and generate comparison tables in latex format.

**Execution**: see experiments_data_augmentation/launch_experiments.sh, experiment "combine_subjects_and_predicates"














## Experiments: robustness enhancement


**Goal**: generate a more robust training set in terms of vocabulary.

**Method**: replace the subjects roots of the captions of a video with the root with higher PMI (with respect to all the captions context), and replace all verbs with the synonym with higher PMI (with respect to each caption context).

**Results**: experiments_association_strengthen/results/demo_results.txt.

**Execution**: see experiments_association_strengthen/launch_experiments.sh, experiment "association_strengthen"
