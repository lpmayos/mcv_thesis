#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json


def main():
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


if __name__ == "__main__":
    main()
