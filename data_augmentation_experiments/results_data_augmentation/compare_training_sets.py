#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json


def print_table_head():
    print '\\begin{longtable}{'
    # print '\t>{\\raggedright\\arraybackslash}p{1.00\\textwidth}'
    print '\t>{\\raggedright\\arraybackslash}p{0.50\\textwidth}'
    print '\t>{\\raggedright\\arraybackslash}p{0.50\\textwidth}'
    print '\t}'
    print '\t\caption{Augmenting the training set sentences. Comparative of the results of the two different experiments on one of the videos of the MSR-VTT training set, showing for each experiment the newly generated captions.}'
    print '\t\label{table:augmenting_sample}\\\\'
    print '\t\hline'
    # print '\t\\textbf{Captions}\\\\'
    print '\t\\textbf{Exp. 1} & \\textbf{Exp. 2}\\\\'
    print '\t\hline'
    print '\t\endfirsthead'
    # print '\t\multicolumn{1}{c}%'
    print '\t\multicolumn{2}{c}%'
    print '\t{\\tablename\ \\thetable\ -- \\textit{Continued from previous page}} \\\\'
    print '\t\hline'
    # print '\t\\textbf{Captions}\\\\'
    print '\t\\textbf{Exp. 1} & \\textbf{Exp. 2}\\\\'
    print '\t\hline\\\\'
    print '\t\endhead'
    # print '\t\hline \multicolumn{1}{r}{\\textit{Continued on next page}} \\\\'
    print '\t\hline \multicolumn{2}{r}{\\textit{Continued on next page}} \\\\'
    print '\t\endfoot'
    print '\t\hline'
    print '\t\endlastfoot\\\\'


def print_table_tail():
    print '\\end{longtable}\n\n'


def generate_latex_tables():
    data_file_original = open('/home/lpmayos/code/caption-guided-saliency/DATA/MSR-VTT/train_val_videodatainfo.json')
    data_original = json.load(data_file_original)
    data_file1 = open('/home/lpmayos/code/caption-guided-saliency/DATA/MSR-VTT/new_train_val_videodatainfo/train_val_videodatainfo_sub_pred_combinations.json')
    data1 = json.load(data_file1)
    data_file2 = open('/home/lpmayos/code/caption-guided-saliency/DATA/MSR-VTT/new_train_val_videodatainfo/train_val_videodatainfo_sub_pred_combinations_with_subject_matching.json')
    data2 = json.load(data_file2)

    # videos_to_compare = ['video3742', 'video6000', 'video6001', 'video6002', 'video6003', 'video6004', 'video6005', 'video6006', 'video6007', 'video6008', 'video6009']
    videos_to_compare = ['video6009']

    for video_id in videos_to_compare:

        print_table_head()

        sentences1 = [a['caption'] for a in data1['sentences'] if a['video_id'] == video_id]
        sentences2 = [a['caption'] for a in data2['sentences'] if a['video_id'] == video_id]
        sentences_original = [a['caption'] for a in data_original['sentences'] if a['video_id'] == video_id]

        i = 0
        while i < len(sentences1):

            sentence_left = sentences1[i]
            if sentence_left not in sentences2:
                sentence_left = '\\ul{' + sentence_left + '}'
            if sentences1[i] in sentences_original:
                sentence_left = '\\textbf{' + sentence_left + '}'

            if i + 1 == len(sentences1):
                sentence_right = ' '
            else:
                sentence_right = sentences1[i + 1]
                if sentence_right not in sentences2:
                    sentence_right = '\\ul{' + sentence_right + '}'
                if sentences1[i + 1] in sentences_original:
                    sentence_right = '\\textbf{' + sentence_right + '}'

            print sentence_left + ' & ' + sentence_right + '\\\\'

            i += 2

        print_table_tail()


def print_deleted_sentences():
    data_file1 = open('/home/lpmayos/code/caption-guided-saliency/DATA/MSR-VTT/new_train_val_videodatainfo/train_val_videodatainfo_sub_pred_combinations.json')
    data1 = json.load(data_file1)
    data_file2 = open('/home/lpmayos/code/caption-guided-saliency/DATA/MSR-VTT/new_train_val_videodatainfo/train_val_videodatainfo_sub_pred_combinations_with_subject_matching.json')
    data2 = json.load(data_file2)

    videos_to_compare = ['video3742', 'video6000', 'video6001', 'video6002', 'video6003', 'video6004', 'video6005', 'video6006', 'video6007', 'video6008', 'video6009']

    for video_id in videos_to_compare:

        sentences1 = [a['caption'] for a in data1['sentences'] if a['video_id'] == video_id]
        sentences2 = [a['caption'] for a in data2['sentences'] if a['video_id'] == video_id]

        for sentence in sentences1:
            if sentence not in sentences2:
                print sentence


def num_captions_pre_training_set():
    data = open('/home/lpmayos/code/caption-guided-saliency/DATA/MSR-VTT/new_train_val_videodatainfo/train_val_videodatainfo.json')
    original = json.load(data)

    data = open('/home/lpmayos/code/caption-guided-saliency/DATA/MSR-VTT/new_train_val_videodatainfo/train_val_videodatainfo_subj_pred_combi.json')
    combi = json.load(data)

    data = open('/home/lpmayos/code/caption-guided-saliency/DATA/MSR-VTT/new_train_val_videodatainfo/train_val_videodatainfo_subj_pred_combi_subject_matching.json')
    combi_senses = json.load(data)

    data = open('/home/lpmayos/code/caption-guided-saliency/DATA/MSR-VTT/new_train_val_videodatainfo/train_val_videodatainfo_el_th1_0.11_th2_0.435.json')
    e4sym = json.load(data)

    data = open('/home/lpmayos/code/caption-guided-saliency/DATA/MSR-VTT/new_train_val_videodatainfo/train_val_videodatainfo_el_th1_0.11_th2_0.435_subj_pred_combi_senses.json')
    e4sym_combi_senses = json.load(data)

    print 'original: ' + str(len(original['sentences']))
    print 'combi: ' + str(len(combi['sentences']))
    print 'combi_senses: ' + str(len(combi_senses['sentences']))
    print 'e4sym: ' + str(len(e4sym['sentences']))
    print 'e4sym_combi_senses: ' + str(len(e4sym_combi_senses['sentences']))


def main():
    generate_latex_tables()


if __name__ == "__main__":
    main()
