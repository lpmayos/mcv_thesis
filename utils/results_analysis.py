import json


# training data for each experiment
experiments = ['original', 'exp1', 'exp4', 'exp4_symmetrical', 'subj_pred_combi', 'pmi_subj_replace', 'subj_pred_combi_pmi_subj_replace']

training_data = {'original': '/home/lpmayos/code/caption-guided-saliency/DATA/MSR-VTT/train_val_videodatainfo.json',
                 'exp1': '/home/lpmayos/code/caption-guided-saliency/DATA/MSR-VTT/new_train_val_videodatainfo/train_val_videodatainfo_e1_th2_0.785.json',
                 'exp4': '/home/lpmayos/code/caption-guided-saliency/DATA/MSR-VTT/new_train_val_videodatainfo/train_val_videodatainfo_e4_th1_0.09_th2_0.506.json',
                 'exp4_symmetrical': '/home/lpmayos/code/caption-guided-saliency/DATA/MSR-VTT/new_train_val_videodatainfo/train_val_videodatainfo_el_th1_0.11_th2_0.435.json',
                 'subj_pred_combi': '/home/lpmayos/code/caption-guided-saliency/DATA/MSR-VTT/new_train_val_videodatainfo/train_val_videodatainfo_el_th1_0.11_th2_0.435_subj_pred_combi_senses.json',
                 'pmi_subj_replace': '/home/lpmayos/code/caption-guided-saliency/DATA/MSR-VTT/new_train_val_videodatainfo/train_val_videodatainfo_el_th1_0.11_th2_0.435_pmi_subject_replacement.json',
                 'subj_pred_combi_pmi_subj_replace': '/home/lpmayos/code/caption-guided-saliency/DATA/MSR-VTT/new_train_val_videodatainfo/train_val_videodatainfo_el_th1_0.11_th2_0.435_pmi_subject_replacement_subj_pred_combi.json'}

# test results for each experiment
generated_captions = {'original': '/home/lpmayos/code/caption-guided-saliency/experiments/msr-vtt/model-99.json',
                      'exp1': '/home/lpmayos/code/caption-guided-saliency/experiments/msr-vtt-experiment1/model-99.json',
                      'exp4': '/home/lpmayos/code/caption-guided-saliency/experiments/msr-vtt-experiment4/model-99.json',
                      'exp4_symmetrical': '/home/lpmayos/code/caption-guided-saliency/experiments/msr-vtt-experiment4_symmetrical/model-99.json',
                      'subj_pred_combi': '/home/lpmayos/code/caption-guided-saliency/experiments/msr-vtt-el_th1_0.11_th2_0.435_subj_pred_combi_senses/model-99.json',
                      'pmi_subj_replace': '/home/lpmayos/code/caption-guided-saliency/experiments/msr-vtt-experiment_pmi_subject_replacement/model-99.json',
                      'subj_pred_combi_pmi_subj_replace': '/home/lpmayos/code/caption-guided-saliency/experiments/msr-vtt-experiment_pmi_subject_replacement_subj_pred_combi/model-99.json'}

video = 'video0'

for experiment in experiments:
    file = open(training_data[experiment])
    data = json.load(file)

    captions = [a['caption'] for a in data['sentences'] if a['video_id'] == video]
    print '\n' + experiment + ' ' + str(len(captions))
    for caption in captions:
        print '\t' + caption
