# Improving the quality of video-to-language models by an optimized annotation of the training material 

* **Master in Computer Vision 2016-2017**
* **Student**: Laura Pérez Mayos
* **Supervisor**: Leo Wanner
* **Co-Supervisor**: Federico Sukno
* **University**: UPF
* **Course**: 2016-2017

## Abstract
 
Video has become omnipresent, and the analysis of the semantics of video has a large variety of applications, including scene understanding, accessibility improvement and information retrieval.  However, automatically describing  videos  in terms of natural  language  is  one  of  the  ultimate challenges of video understanding, given the difficulties of video interpretation and natural language generation. Many state-of-the-art models focus on the generation of captions of short-term videos. In this context, Microsoft has released Microsoft Research - Video to Text (MSR-VTT), a large-scale annotated video benchmark that contains 41.2 hours of recordings.The annotation consists of 20 Mechanical Turk captions per video, resulting in 200K captions-video pairs in total.

![alt text](https://github.com/lpmayos/mcv_thesis/samples/video_frames.png "MSR-VTT Examples: video frames and annotated sentences")

As the excerpts of the caption lists in Figure 1 show, the specificity and quality of the captions vary considerably. This is likely to have a negative influence on the quality of the trained models since all captions are taken into account equally. In the context of this Master Thesis, possible automatic strategies for optimizing the annotations of video material will be explored and the consequences of this optimization will be analyzed with a state-of-the-art deep learning video-to-language model.


## Experiment 1

**Goal**: detect those annotations that are wrong: they have typos or are
not descriptive.

**Method**: for each video we get all the annotations and we compute an
embedding for all the sentences. Then, we project all the embeddings
in common space, we compute its centroid and the distances to the
centroid of each embedding, sorting the annotations by distance.
Then, we can discard the highest percentage (i.e. 10%) or the ones that
are above a certain threshold.

**Results**: a sample of the results (sentence ordering and image of the
embedding space) can be seen at results/experiment1/