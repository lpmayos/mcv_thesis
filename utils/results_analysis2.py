import json

original = '/home/lpmayos/code/caption-guided-saliency/DATA/MSR-VTT/train_val_videodatainfo.json'
exp1 = '/home/lpmayos/code/caption-guided-saliency/DATA/MSR-VTT/new_train_val_videodatainfo/train_val_videodatainfo_e1_th2_0.785.json'
exp4 = '/home/lpmayos/code/caption-guided-saliency/DATA/MSR-VTT/new_train_val_videodatainfo/train_val_videodatainfo_e4_th1_0.09_th2_0.506.json'
exp4_symmetrical = '/home/lpmayos/code/caption-guided-saliency/DATA/MSR-VTT/new_train_val_videodatainfo/train_val_videodatainfo_el_th1_0.11_th2_0.435.json'

original_json = json.load(open(original))
exp1_json = json.load(open(exp1))
exp4_json = json.load(open(exp4))
exp4_symmetrical_json = json.load(open(exp4_symmetrical))

original_num_sentences = len(original_json['sentences'])
original_num_videos = len(original_json['videos'])
exp1_num_sentences = len(exp1_json['sentences'])
exp1_num_videos = len(exp1_json['videos'])
exp4_num_sentences = len(exp4_json['sentences'])
exp4_num_videos = len(exp4_json['videos'])
exp4_symmetrical_num_sentences = len(exp4_symmetrical_json['sentences'])
exp4_symmetrical_num_videos = len(exp4_symmetrical_json['videos'])


print 'Original training set. %i videos and %i training sentences: %f sentences/video' %(original_num_videos, original_num_sentences, float(original_num_sentences)/original_num_videos)
print 'Exp1 training set. %i videos and %i training sentences: %f sentences/video, %i sentences removed' %(exp1_num_videos, exp1_num_sentences, float(exp1_num_sentences)/exp1_num_videos, original_num_sentences - exp1_num_sentences)
print 'Exp4 training set. %i videos and %i training sentences: %f sentences/video, %i sentences removed' %(exp4_num_videos, exp4_num_sentences, float(exp4_num_sentences)/exp4_num_videos, original_num_sentences - exp4_num_sentences)
print 'Exp4_symmetrical training set. %i videos and %i training sentences: %f sentences/video, %i sentences removed' %(exp4_symmetrical_num_videos, exp4_symmetrical_num_sentences, float(exp4_symmetrical_num_sentences)/exp4_symmetrical_num_videos, original_num_sentences - exp4_symmetrical_num_sentences)
